import os
import pandas as pd
from notion_client import Client
from src.dataframe import notion2df


# notionの設定
notion = Client(auth=os.environ['NOTION_TOKEN'])


def get_all_movies() -> pd.DataFrame:
    """
    映画情報を全件取得するNotion API

    Returns
    -------
    movies: pd.DataFrame
      映画情報のDataFrame
    """
    all_db = []
    has_more = True
    query = {
        'database_id': os.environ.get('DB_ID')
    }

    while(has_more):
        db = notion.databases.query(
            **query
        )
        all_db.extend(db.get('results'))
        has_more = db.get('has_more', False)
        query['start_cursor'] = db.get('next_cursor')

    return notion2df(all_db)
