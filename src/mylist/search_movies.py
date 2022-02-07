import pandas as pd


def and_or_search(data: list, target: list, is_and: bool) -> bool:
    if is_and:
        if set(data) & set(target) == set(target):
            return True
    else:
        if set(data) & set(target):
            return True

    return False


def genres_limitation(movies: pd.DataFrame, genres: list, and_search: bool) -> pd.DataFrame:
    tmdb_ids = [movie.tmdb_id for movie in movies.itertuples()
                if and_or_search(movie.genres, genres, and_search)]
    movies = movies.query(' tmdb_id in @tmdb_ids ').reset_index(drop=True)
    return movies
