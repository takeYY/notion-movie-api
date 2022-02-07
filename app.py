from flask import Flask, Blueprint, render_template, request, session, redirect, url_for
import os
from datetime import timedelta
import pandas as pd
from notion_client import Client
import json
from models.movie_class import Movie
from src.get_movie import get_genres_dict, tmdb2notion_genres, tmdb_poster_path_uri
from src.create_movie import create_movie
from src.update_movie import update_movie
from src.search_movies import search_a_movie_by_tmdb, search_movies
from src.dataframe import json2df, processing_tmdb_df
from src.json import update_json
from src.mylist.search_movies import title_limitation, rating_limitation, genres_limitation

app = Flask(__name__)
# SECRET_KEYを設定
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
# sessionの設定
app.permanent_session_lifetime = timedelta(minutes=30)
# notionの設定
notion = Client(auth=os.environ['NOTION_TOKEN'])
index_page = Blueprint('index', __name__, url_prefix='/')
mylist_page = Blueprint('mylist', __name__, url_prefix='/mylist')


@index_page.route('')
def home():
    basic_data = dict(title='ホーム', active_url='home')

    movies = json2df()

    return render_template('index.html',
                           basic_data=basic_data,
                           movies=movies)


@index_page.route('/edit/<string:page_id>')
def edit(page_id: str):
    basic_data = dict(title='編集画面', active_url='edit_movie')

    result = notion.pages.retrieve(page_id=page_id)
    movie = Movie(result=result)

    # session登録
    session.clear()
    session['page_id'] = movie.id
    session['cover_url'] = movie.cover_url

    return render_template('edit.html',
                           basic_data=basic_data,
                           page_id=page_id,
                           movie=movie.__dict__,
                           genres=get_genres_dict())


@index_page.route('/updated/<string:page_id>', methods=['POST'])
def update(page_id: str):
    # session切れの場合
    if not session.get('page_id'):
        redirect(url_for('index.home'))

    basic_data = dict(title='更新完了', active_url='updated_movie')
    movie = Movie(form=request.form, session=session)
    update_information = update_movie(page_id, movie)
    result = notion.pages.update(**update_information)

    movie = Movie(result=result)

    # jsonを更新
    update_json()

    return render_template('updated.html',
                           basic_data=basic_data,
                           movie=movie.__dict__,
                           genres=get_genres_dict())


@index_page.route('/search', methods=['POST'])
def search():
    basic_data = dict(title='検索結果', active_url='search_movies')

    title = request.form.get('title')
    # TMDb APIで映画検索し、DataFrameで格納
    tmdb_df: pd.DataFrame = search_movies(title)
    # 結果がない場合
    if tmdb_df.empty:
        return render_template('search.html',
                               basic_data=basic_data,
                               searched_title=title,
                               movies=tmdb_df)

    # 必要な情報のみに絞る
    tmdb_df = processing_tmdb_df(tmdb_df)

    # Notionに登録されている情報を取得
    notion_df = json2df()
    # TMDbのDFとnotionのDFを連結
    movies = pd.merge(tmdb_df, notion_df, how='left', on='tmdb_id')
    # 欠損値補完
    movies = movies.fillna({
        'cover_url': '',
        'genres': ''
    })

    return render_template('search.html',
                           basic_data=basic_data,
                           searched_title=title,
                           movies=movies)


@index_page.route('/new/<string:tmdb_id>')
def new(tmdb_id: str):
    basic_data = dict(title='マイリストに追加', active_url='new_movie')

    movie = search_a_movie_by_tmdb(tmdb_id)
    movie['title'] = movie.get('title').replace(' ', '：').replace('／', '：')
    movie['poster_path'] = tmdb_poster_path_uri() + movie.get('poster_path')
    if movie.get('genres'):
        movie['genres'] = [tmdb2notion_genres().get(str(genre.get('id')))
                           for genre in movie.get('genres', {'a': 'b'})]

    # session登録
    session.clear()
    session['tmdb_id'] = tmdb_id
    session['cover_url'] = movie.get('poster_path')

    return render_template('new.html',
                           basic_data=basic_data,
                           tmdb_id=tmdb_id,
                           movie=movie,
                           genres=get_genres_dict())


@index_page.route('/created/<string:tmdb_id>', methods=['POST'])
def create(tmdb_id: str):
    basic_data = dict(title='追加完了', active_url='created_movie')

    movie = Movie(form=request.form, session=session)
    create_information = create_movie(movie)
    result = notion.pages.create(**create_information)

    movie = Movie(result=result)

    # jsonを更新
    update_json()

    return render_template('created.html',
                           basic_data=basic_data,
                           movie=movie.__dict__)


@mylist_page.route('/watched', methods=['GET', 'POST'])
def show_watched():
    basic_data = dict(title='Watched', active_url='watched')

    movies = json2df()
    # 観た映画のみに絞る
    movies = movies.query(' has_watched ').reset_index(drop=True)

    if request.method == 'GET':
        return render_template('mylist/watched.html',
                               basic_data=basic_data,
                               movies=movies,
                               genres=get_genres_dict())

    form = request.form
    title = form.get('title')
    genres = form.getlist('genres')
    rating = list(map(int, form.getlist('rating')))
    and_search = True if int(form.get('genres_and_search'))\
        else False
    if rating:
        movies = rating_limitation(movies, rating)
    if genres:
        movies = genres_limitation(movies, genres, and_search)
    if title:
        movies = title_limitation(movies, title)
    queries = dict(title=title,
                   rating=rating,
                   genres=genres,
                   genres_and_search=and_search)
    return render_template('mylist/watched.html',
                           basic_data=basic_data,
                           movies=movies,
                           genres=get_genres_dict(),
                           queries=queries)


@mylist_page.route('/to-watch', methods=['GET'])
def show_to_watch():
    basic_data = dict(title='To Watch', active_url='to_watched')

    movies = json2df()
    # 観た映画のみに絞る
    movies = movies.query(' not has_watched ').reset_index(drop=True)

    return render_template('mylist/to-watch.html',
                           basic_data=basic_data,
                           movies=movies)


app.register_blueprint(index_page)
app.register_blueprint(mylist_page)

# おまじない
if __name__ == "__main__":
    app.debug = True  # デバッグモード有効化
    app.run(host='0.0.0.0', port=8080)  # どこからでもアクセス可能に
