import os
import requests
import urllib.parse
from src.mecab_token import tokenize
from src.calculate import calc_movie_similarity


def search_movies_by_tmdb(title: str = '', page: int = 1):
    search_uri = 'https://api.themoviedb.org/3/search/movie'
    query_data = {
        'language': 'ja-JP',
        'query': title,
        'page': page
    }
    query = urllib.parse.urlencode(query_data)

    return requests.get(f'{search_uri}?api_key={os.environ.get("TMDB_KEY")}&{query}').json().get('results')


def search_movies(title: str):
    results = search_movies_by_tmdb(title)
    title_tokenized = tokenize(title)
    movies = [calc_movie_similarity(title_tokenized, result)
              for result in results]
    # 類似度で降順ソート
    movies = sorted(movies, key=lambda x: x.point, reverse=True)
    return movies
