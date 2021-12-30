from datetime import date


class Movie:
    """
    映画情報を保持する

    Attributes
    ----------
    id: str
      データID
    tmdb_id: str
      TMDbのID
    title: str
      映画タイトル
    cover_url: str
      映画ポスターのURL
    rating: int
      映画の評価、Noneは未鑑賞
    views: int
      映画の視聴回数、Noneは未鑑賞
    has_watched: bool
      映画を観たかどうか
    genres: list of str
      映画ジャンル
    first_watched_at: date
      最初に映画を観た日付（記憶にない場合、2021-12-25）、Noneは未鑑賞
    last_watched_at: date
      最後に映画を観た日付、Noneは未鑑賞
    feeling: str
      感想、所感など

    """

    def __init__(self, result: dict = {}, form: dict = {}, session: dict = {}, search: dict = {}, point: float = 0.00):
        if result:
            self.set_params_by_result(result)
        elif form:
            self.set_params_by_form(form, session)
        elif search:
            self.set_params_by_search(search, point)
        else:
            pass

    def set_params_by_result(self, result: dict):
        self.id: str = result.get('id')
        properties = result['properties']
        self.tmdb_id: str = str(properties['TMDb ID']['number'])
        self.title: str = properties['Title']['title'][0]['text']['content']
        self.cover_url: str = properties['Cover']['files'][0]['external']['url']
        self.rating: int = len(properties['Rating']['select']['name'])\
            if properties['Rating']['select']\
            else None
        self.views: int = properties['Views']['number']
        self.has_watched: bool = True\
            if properties['Status']['select'] and properties['Status']['select']['name'] == 'Watched'\
            else False
        self.genres: list = [genre['name'] for genre in properties['Genres']['multi_select']]\
            if properties['Genres']['multi_select']\
            else []
        self.first_watched_at: date = date.fromisoformat(properties['First Watched at']['date']['start'])\
            if properties['First Watched at']['date']\
            else None
        self.last_watched_at: date = date.fromisoformat(properties['Last Watched at']['date']['start'])\
            if properties['Last Watched at']['date']\
            else None
        self.feeling: str = properties['Feeling']['rich_text'][0]['text']['content']\
            if properties['Feeling']['rich_text']\
            else None

    def set_params_by_form(self, form: dict, session: dict):
        self.id: str = session.get('page_id')
        self.title: str = form.get('title')
        self.cover_url: str = session.get('cover_url')
        self.rating: int = int(form.get('rating', 0))
        self.views: int = int(form.get('views'))\
            if form.get('views')\
            else 0
        self.has_watched: bool = True\
            if form.get('status') == 'Watched'\
            else False
        self.genres: list = form.getlist('genres')\
            if form.getlist('genres')\
            else None
        self.first_watched_at: date = date.fromisoformat(form.get('first-watched-at'))\
            if form.get('first-watched-at')\
            else None
        self.last_watched_at: date = date.fromisoformat(form.get('last-watched-at'))\
            if form.get('last-watched-at')\
            else None
        self.feeling: str = form.get('feeling')\
            if form.get('feeling')\
            else ''

    def set_params_by_search(self, search: dict, point: float):
        self.tmdb_id: str = str(search.get('id'))
        self.title: str = search.get('title')
        self.poster_path: str = f"https://www.themoviedb.org/t/p/w600_and_h900_bestv2/{search.get('poster_path')}"\
            if search.get('poster_path')\
            else None
        self.release_date: date = date.fromisoformat(search.get('release_date'))\
            if search.get('release_date')\
            else 'N/A'
        self.overview: str = search.get('overview')\
            if search.get('overview')\
            else 'N/A'
        self.point: float = point
