from models.movie_class import Movie


def _update_title(movie: Movie):
    return {
        'title': [{
            'text': {
                'content': movie.title
            }
        }]
    }


def _update_status(movie: Movie):
    return {
        'select': {
            'name': 'Watched' if movie.has_watched else 'To Watch'
        }
    }


def _update_rating(movie: Movie):
    return {
        'select': {
            'name': '★'*movie.rating
        }
    }


def _update_genres(movie: Movie):
    return {
        'multi_select': [{'name': genre} for genre in movie.genres]
    }


def _update_views(movie: Movie):
    return {
        'number': movie.views
    }


def _update_first_watched_at(movie: Movie):
    return {
        'date': {
            'start': str(movie.first_watched_at)
        }
    }


def _update_last_watched_at(movie: Movie):
    return {
        'date': {
            'start': str(movie.last_watched_at)
        }
    }


def _update_feeling(movie: Movie):
    return {
        'rich_text': [{
            'text': {
                'content': movie.feeling
            }
        }]
    }


def update_movie(page_id: str, movie: Movie):
    properties = dict(Title=_update_title(movie),
                      Status=_update_status(movie),
                      Views=_update_views(movie),
                      Feeling=_update_feeling(movie))

    if movie.rating:
        properties['Rating'] = _update_rating(movie)
    if movie.genres:
        properties['Genres'] = _update_genres(movie)
    if movie.first_watched_at:
        properties['First Watched at'] = _update_first_watched_at(movie)
    if movie.last_watched_at:
        properties['Last Watched at'] = _update_last_watched_at(movie)

    update_information = {
        'page_id': page_id,
        'properties': properties
    }

    return update_information


def get_genres_dict():
    return dict(action='アクション', sf='SF', crime='クライム', suspense='サスペンス',
                war='戦争', drama='人間ドラマ', documentary='史実・歴史', love='ラブストーリー',
                musical='ミュージカル', comedy='コメディ', animation='アニメーション',
                horror='ホラー', fantasy='ファンタジー', adventure='アドベンチャー')
