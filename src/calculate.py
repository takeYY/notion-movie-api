from models.movie_class import Movie
from src.mecab_token import tokenize


def sim_dice(subject: set, target: set):
    return 2*len(subject & target) / \
        (len(subject)+len(target))


def calc_movie_similarity(title_tokenized: list, result: dict):
    result_tokenized = tokenize(result.get('title'))
    point = sim_dice(set(title_tokenized),
                     set(result_tokenized))

    return Movie(search=result, point=point)
