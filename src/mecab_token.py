import MeCab


def tokenize(text, target_pos=['名詞']):
    text = text.replace('・', ' ')
    tokens = []
    try:
        mecab = MeCab.Tagger('-d /usr/lib/x86_64-linux-gnu/mecab/dic/mecab-ipadic-neologd')
    except:
        mecab = MeCab.Tagger('')
    mecab.parse('')  # 文字列のGC防止
    node = mecab.parseToNode(text)
    while node:
        # 単語を取得
        word = node.surface
        # 品詞を取得
        pos = node.feature.split(',')[0]
        # 名詞の場合のみ抽出
        if pos in target_pos:
            tokens.append(word)
        # 次の単語に進める
        node = node.next
    return tokens
