from models.movie_class import Movie
import os


def _create_tmdb_id(movie: Movie):
    return {
        'number': int(movie.tmdb_id)
    }


def _create_cover(movie: Movie):
    return {
        'files': [{
            'name': movie.cover_url,
            'type': 'external',
            'external': {
                'url': movie.cover_url
            }
        }]
    }


def _create_title(movie: Movie):
    return {
        'title': [{
            'text': {
                'content': movie.title
            }
        }]
    }


def _create_status(movie: Movie):
    return {
        'select': {
            'name': 'Watched' if movie.has_watched else 'To Watch'
        }
    }


def _create_rating(movie: Movie):
    return {
        'select': {
            'name': '★'*movie.rating
        }
    }


def _create_genres(movie: Movie):
    return {
        'multi_select': [{'name': genre} for genre in movie.genres]
    }


def _create_views(movie: Movie):
    return {
        'number': movie.views
    }


def _create_first_watched_at(movie: Movie):
    return {
        'date': {
            'start': str(movie.first_watched_at)
        }
    }


def _create_last_watched_at(movie: Movie):
    return {
        'date': {
            'start': str(movie.last_watched_at)
        }
    }


def _create_feeling(movie: Movie):
    return {
        'rich_text': [{
            'text': {
                'content': movie.feeling
            }
        }]
    }


def create_movie(movie: Movie):
    properties = dict(Title=_create_title(movie),
                      Cover=_create_cover(movie),
                      Status=_create_status(movie),
                      Views=_create_views(movie),
                      Feeling=_create_feeling(movie))

    if movie.tmdb_id:
        properties['TMDb ID'] = _create_tmdb_id(movie)
    if movie.rating:
        properties['Rating'] = _create_rating(movie)
    if movie.genres:
        properties['Genres'] = _create_genres(movie)
    if movie.first_watched_at and movie.has_watched:
        properties['First Watched at'] = _create_first_watched_at(movie)
    if movie.last_watched_at and movie.has_watched:
        properties['Last Watched at'] = _create_last_watched_at(movie)

    create_information = {
        'parent': {
            'database_id': os.environ.get('DB_ID')
        },
        'properties': properties
    }

    return create_information
