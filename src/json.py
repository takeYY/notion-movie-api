import pandas as pd
from src.dataframe import date2str
from src.notion_api import get_all_movies


def df2json(df: pd.DataFrame):
    df.to_json('json/notion_movies.json',
               force_ascii=False, orient='records')


def update_json():
    movies = get_all_movies()

    # 日付をstrへ変換
    columns = ['first_watched_at',
               'last_watched_at']
    movies = date2str(movies, columns)

    df2json(movies)
