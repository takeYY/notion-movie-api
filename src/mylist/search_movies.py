import pandas as pd
from src.mecab_token import tokenize
from src.calculate import calc_movie_similarity


def and_or_search(data: list, target: list, is_and: bool) -> bool:
    if is_and:
        if set(data) & set(target) == set(target):
            return True
    else:
        if set(data) & set(target):
            return True

    return False


def title_limitation(movies: pd.DataFrame, title: list) -> pd.DataFrame:
    # 類似度計算
    movies['point'] = movies['title'].map(lambda tmdb_title: calc_movie_similarity(tokenize(title),
                                                                                   tokenize(tmdb_title)))
    return movies.query(' 0.0 < point ').sort_values('point', ascending=False)


def rating_limitation(movies: pd.DataFrame, rating: list) -> pd.DataFrame:
    tmdb_ids = [movie.tmdb_id for movie in movies.itertuples()
                if movie.rating == movie.rating and and_or_search([int(movie.rating)], rating, False)]
    return movies.query(' tmdb_id in @tmdb_ids ').reset_index(drop=True)


def genres_limitation(movies: pd.DataFrame, genres: list, and_search: bool) -> pd.DataFrame:
    tmdb_ids = [movie.tmdb_id for movie in movies.itertuples()
                if movie.genres and and_or_search(movie.genres, genres, and_search)]
    return movies.query(' tmdb_id in @tmdb_ids ').reset_index(drop=True)
