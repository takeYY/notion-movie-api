import os
import requests
import urllib.parse
import pandas as pd
from src.dataframe import tmdb2df
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


def search_movies(title: str, page: int = 1):
    results = search_movies_by_tmdb(title, page)

    # 結果がない場合
    if not results:
        return pd.DataFrame()

    tmdb_df = tmdb2df(results)
    title_tokenized = tokenize(title)
    # 類似度計算
    tmdb_df['point'] = tmdb_df['title'].map(lambda tmdb_title: calc_movie_similarity(title_tokenized,
                                                                                     tokenize(tmdb_title)))
    # 類似度で降順ソート
    tmdb_df = tmdb_df.sort_values('point', ascending=False)\
                     .reset_index(drop=True)
    return tmdb_df
