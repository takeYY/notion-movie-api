from flask import Flask, Blueprint, render_template, request, session, redirect, url_for
import os
from datetime import timedelta
import pandas as pd
from notion_client import Client
from models.movie_class import Movie
from src.get_movie import get_genres_dict
from src.update_movie import update_movie
from src.search_movies import search_movies
from src.dataframe import notion2df, processing_tmdb_df

app = Flask(__name__)
# SECRET_KEYを設定
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
# sessionの設定
app.permanent_session_lifetime = timedelta(minutes=30)
# notionの設定
notion = Client(auth=os.environ['NOTION_TOKEN'])
index_page = Blueprint('index', __name__, url_prefix='/')


@index_page.route('')
def home():
    basic_data = dict(title='ホーム', active_url='home')

    db = notion.databases.query(
        **{
            'database_id': os.environ.get('DB_ID')
        }
    )

    movies = [Movie(result=result) for result in db['results']]

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

    db = notion.databases.query(
        **{
            'database_id': os.environ.get('DB_ID')
        }
    )

    notion_df: pd.DataFrame = notion2df(db.get('results'))
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


app.register_blueprint(index_page)


# おまじない
if __name__ == "__main__":
    app.debug = True  # デバッグモード有効化
    app.run(host='0.0.0.0', port=8080)  # どこからでもアクセス可能に
