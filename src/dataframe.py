import pandas as pd
import json
from datetime import date
from src.get_movie import tmdb_genres, tmdb_poster_path_uri


def tmdb2df(results: dict):
    return pd.DataFrame(results)


def notion2df(results: list):
    contents = []
    for result in results:
        properties = result.get('properties')
        contents.append({
            'id': result.get('id'),
            'tmdb_id': properties['TMDb ID']['number'],
            'title': properties['Title']['title'][0]['text']['content'],
            'cover_url': properties['Cover']['files'][0]['external']['url'],
            'rating': len(properties['Rating']['select']['name'])
            if properties['Rating']['select']
            else None,
            'views': properties['Views']['number'],
            'has_watched': True
            if properties['Status']['select'] and properties['Status']['select']['name'] == 'Watched'
            else False,
            'genres': [genre['name'] for genre in properties['Genres']['multi_select']]
            if properties['Genres']['multi_select']
            else None,
            'first_watched_at': date.fromisoformat(properties['First Watched at']['date']['start'])
            if properties['First Watched at']['date']
            else None,
            'last_watched_at': date.fromisoformat(properties['Last Watched at']['date']['start'])
            if properties['Last Watched at']['date']
            else None,
            'feeling': properties['Feeling']['rich_text'][0]['text']['content']
            if properties['Feeling']['rich_text']
            else None
        })
    return pd.DataFrame(contents)


def json2df():
    with open('json/notion_movies.json') as f:
        contents = json.load(f)

    return pd.DataFrame(contents)


def ids2genres(genre_ids: list):
    return [tmdb_genres().get(str(genre_id)) for genre_id in genre_ids]


def processing_tmdb_df(df: pd):
    # 必要な情報のリスト
    target_columns = ['id', 'title', 'release_date', 'genre_ids', 'point',
                      'vote_average', 'poster_path', 'overview']
    # ジャンルをIDから名称に変更
    df['genre_ids'] = df['genre_ids'].map(ids2genres)
    # ポスターパスに接頭辞追加
    df['poster_path'] = df['poster_path'].map(
        lambda p: f'{tmdb_poster_path_uri()}{p.split(".jpg")[0]}.jpg'
        if p
        else '')
    # 必要な情報のみに絞り、idをtmdb_idに変更
    return df[target_columns].rename(columns={'id': 'tmdb_id'})


def date2str(df: pd.DataFrame, columns: list):
    for column in columns:
        df[column] = pd.to_datetime(df[column], errors='coerce')\
                       .dt.strftime('%Y-%m-%d')

    return df
