def get_genres_dict():
    return dict(action='アクション', sf='SF', crime='クライム', suspense='サスペンス',
                war='戦争', drama='人間ドラマ', documentary='史実・歴史', love='ラブストーリー',
                musical='ミュージカル', comedy='コメディ', animation='アニメーション',
                horror='ホラー', fantasy='ファンタジー', adventure='アドベンチャー')


def tmdb_genres():
    return {
        '28': 'アクション', '12': 'アドベンチャー', '16': 'アニメーション', '35': 'コメディ', '80': 'クライム',
        '99': 'ドキュメンタリー', '18': 'ドラマ', '10751': 'ファミリー', '14': 'ファンタジー',
        '36': 'ヒストリー', '27': 'ホラー', '10402': '音楽', '9648': 'ミステリー',
        '10749': 'ロマンス', '878': 'SF', '10770': 'テレビ映画', '53': 'スリラー',
        '10752': '戦争', '37': '西部劇'
    }


def tmdb_poster_path_uri():
    return 'https://www.themoviedb.org/t/p/w600_and_h900_bestv2'
