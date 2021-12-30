def sim_dice(subject: set, target: set):
    return 2*len(subject & target) / \
        (len(subject)+len(target))


def calc_movie_similarity(title_tokenized: list, tmdb_title_tokenized: list):
    return sim_dice(set(title_tokenized),
                    set(tmdb_title_tokenized))
