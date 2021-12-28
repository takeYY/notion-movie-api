from flask import Flask, Blueprint, render_template
import os
from notion_client import Client


app = Flask(__name__)
notion = Client(auth=os.environ['NOTION_TOKEN'])
index_page = Blueprint('index', __name__, url_prefix='/')


@index_page.route('')
def home():
    basic_data = dict(title='ホーム', active_url='home')

    db = notion.databases.query(
        **{
            'database_id': 'eec47c6bfc2744678a918e9a7a00e78c'  # データベースID
        }
    )

    return render_template('index.html', basic_data=basic_data, db=db)


app.register_blueprint(index_page)


# おまじない
if __name__ == "__main__":
    app.debug = True  # デバッグモード有効化
    app.run(host='0.0.0.0', port=8080)  # どこからでもアクセス可能に
