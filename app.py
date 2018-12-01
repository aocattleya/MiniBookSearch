from APIGoogleBooks import APIGoogleBooks
from ElasticsearchWrapper import ElasticsearchWrapper
from flask import Flask, render_template, request, jsonify
import json
import logging

class CustomFlask(Flask):
    '''
    テンプレートのデリミタがVue.jsと競合するので、Flask側でデリミタを別の文字に変更する
	参照：https://muunyblue.github.io/0b7acbba52fb92b2e9c818f7f56bac99.html
    '''
    jinja_options = Flask.jinja_options.copy()
    jinja_options.update(dict(
		block_start_string='(%',
		block_end_string='%)',
		variable_start_string='((',
		variable_end_string='))',
		comment_start_string='(#',
		comment_end_string='#)',
    ))

app = CustomFlask(__name__)
#app = Flask(__name__)

app.config['JSON_AS_ASCII'] = False    # jsonifyで日本語が文字化けする場合の対処

# ロギング
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)-8s %(module)-18s %(funcName)-10s %(lineno)4s: %(message)s'
)

@app.route("/")
def index():
	'''
	画面
	'''
	return render_template("index.html")

@app.route("/get")
def get():
	'''
	ISBNに対応する書籍情報の取得
	'''
	# パラメータからISBNコードを取得
	isbn = request.args.get('isbn', default=None)
	# 必要な情報を取得する
	json_data = APIGoogleBooks().get_json(isbn) if isbn else {}
	# dict型をJSON型のレスポンスに変換
	response = jsonify(json_data)

	return response

@app.route("/regist")
def regist():
	'''
	ISBNに対応する書籍情報を取得して、Elasticsearchに登録
	'''
	# パラメータからISBNコードを取得
	isbn = request.args.get('isbn', default=None)
	logging.debug(isbn)



	# 必要な情報を取得する
	json_data = APIGoogleBooks().get_json(isbn) if isbn else {}

	if json_data == None:
		json_data = {}
	
	if len(json_data) > 0:
		# Elasticsearch
		es = ElasticsearchWrapper('openbd', 'openbd-index')
		# 追加
		es.insert_one(json_data)

	# dict型をJSON型のレスポンスに変換
	response = jsonify(json_data)

	return response

@app.route("/search")
def search():
	'''
	検索
	'''
	# パラメータからISBNコードを取得
	isbn = request.args.get('isbn', default=None)
	title = request.args.get('title', default=None)
	publisher = request.args.get('publisher', default=None)
	author = request.args.get('author', default=None)
	pubdate = request.args.get('pubdate', default=None)
	cover = request.args.get('cover', default=None)

	# 検索の項目名、項目値のDictionary
	items = {}
	if isbn != None:
		items['isbn'] = isbn
	if title != None:
		items['title'] = title
	if publisher != None:
		items['publisher'] = publisher
	if author != None:
		items['author'] = author
	if pubdate != None:
		items['pubdate'] = pubdate
	if cover != None:
		items['cover'] = cover

	# Elasticsearch
	es = ElasticsearchWrapper('openbd', 'openbd-index')
	# 検索
	json_data = es.search_and(items)

	# dict型をJSON型のレスポンスに変換
	response = jsonify(json_data)

	return response

if __name__ == "__main__":
	app.run(debug=True, host='0.0.0.0', port=8080)
