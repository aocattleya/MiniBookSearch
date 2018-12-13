![booksearch](https://user-images.githubusercontent.com/39142850/49347869-33b14780-f6e5-11e8-9e8b-7e9a270c58c8.png)

- [やったこと](#アンカー1)
- [全体的な仕組み](#アンカー5)
- [動作環境](#アンカー9)
- [APIとは](#アンカーa)
- [開発環境](#アンカー2)
- [アプリの機能](#アンカー3)
- [新しく実装した機能](#アンカー4)
- [基本的な修正箇所](#アンカー6)
- [苦戦した事](#アンカー7)
- [全体を通して学べた事](#アンカー8)

<h2 id="アンカー1">:green_book: やったこと</h2>

[@michihosokawa](https://github.com/michihosokawa)さんの『 [書籍管理システム(GitHub) ](https://github.com/michihosokawa/MiniBookManagementSystem)』  
- 使用されているAPIを「**GoogleBooksAPI**」から「**openBD**」へ書き換える  
- 新機能の『一覧表示』機能を追加する  

<h2 id="アンカー5">:green_book: 全体的な仕組み</h2>

![minibooksearch](https://user-images.githubusercontent.com/39142850/49472249-4b5a0e80-f852-11e8-9022-4596ca655e19.png)

<h2 id="アンカー9">:green_book: 環境</h2>

Flask ＋ Elasticsearchで動作しています。

- Java1.8
	- JREではなくJDK
- Elasticsearch6.3
	- 2つのプラグインをインストール  
		- ICU Analysis（プラグイン）  
		- Japanese (Kuromoji) Analysis（プラグイン）
	- http://localhost:9200 でアクセスできることを確認する
- pip install elasticsearch
- pip install Flask

<h2 id="アンカーa">:globe_with_meridians: APIとは</h2>

>Application Programming Interfaceの略  
>何かしらのサービス提供者が、そのサービスを利用するために提供するインタフェースのこと  


openBDの場合は、書誌情報や書影をだれでも自由に使える  
例：https://api.openbd.jp/v1/get?isbn=9784822292270

![2018-12-04 17 09 05](https://user-images.githubusercontent.com/39142850/49427693-5461c600-f7e7-11e8-8cd6-fffb9737f73e.png)

そしてJSON整形サイトなどを利用して取得したい項目を選ぶ、今回アプリの結果として表示させる物となる

![2018-12-04 17 12 19](https://user-images.githubusercontent.com/39142850/49427857-c76b3c80-f7e7-11e8-90e2-e752ef1b906d.png)


<h2 id="アンカー2">:green_book: 開発環境</h2>

- **Python**  
プログラミング言語
- **Flask**  
Python用の軽量なウェブアプリケーションフレームワーク
- **Elasticsearch**  
Elastic社が開発しているオープンソースの全文検索エンジン  
大量にあるドキュメントデータの中から目的のワードを含むデータを検索することが出来る
- **Vue.js**  
オープンソースのJavaScriptフレームワーク

<h2 id="アンカー3">:green_book: アプリの機能</h2>

- **ISBNコードを入力して書籍の登録**  
![isbn](https://user-images.githubusercontent.com/39142850/49414130-9d008b80-f7b5-11e8-8684-37599a3fbc9c.png)

ISBNコードとは（**I**nternational **S**tandard **B**ook **N**umberの略）

<img src="https://user-images.githubusercontent.com/39142850/49381027-5e87b400-f756-11e8-9952-7e23301dfb19.png" width="400px">

世界共通で図書（書籍）を認識する為に記載されるコード  
どこの国のどこの出版社・印刷会社で制作された本の、何というタイトルなのかが分かるように番号をが設定され  
大体、書籍の裏に書かれています。

- **検索機能**  
登録した書籍とマッチする検索結果が表示される

![knsk](https://user-images.githubusercontent.com/39142850/49414266-2021e180-f7b6-11e8-9afc-0fbed0b580d3.png)

- **詳細画面**  
結果をクリックすると「open」から受け取ったAPIの書籍情報が表示される

![knskkk](https://user-images.githubusercontent.com/39142850/49414765-d6d29180-f7b7-11e8-91f5-91308a8f732e.png)

<h2 id="アンカー4">:green_book: 新しく実装した機能</h2>

- **一覧表示機能**
![knskk](https://user-images.githubusercontent.com/39142850/49415597-9de7ec00-f7ba-11e8-8ae6-c9a7c8277400.png)

これまでに登録した書籍をすべて表示させる機能です。



<h2 id="アンカー6">:green_book: 基本的な修正箇所</h2>

### ■ Elasticsearchの定義ファイルの変更  
- mapping.json  
どちらも書籍データなのでisbn,titleなどいくつか名前が同じ

```javascript
{
    "googlebooks": {
        "properties": {
            "isbn" : {
                "type": "text",
                "index": true
            },
            "title": {
                "type": "text",
                "index": true,
                "analyzer": "my_analyzer"
            },
            "authors": {
                "type": "text",
                "index": true,
                "analyzer": "my_analyzer"
            },
            ・
            ・
            ・
```
↓
```javascript
{
    "openbd": {
        "properties": {
            "isbn" : {
                "type": "text",
                "index": true
            },
            "title": {
                "type": "text",
                "index": true,
                "analyzer": "my_analyzer"
            },
            "publisher": {
                "type": "text",
                "index": true,
                "analyzer": "my_analyzer"
            },
            ・
            ・
            ・
```

### ■ Elasticsystem関連の定義名をopenbdに変更  
 - initialaize.py
 - app.py

```python
# Elasticsearch
 es = ElasticsearchWrapper('googlebooks', 'googlebooks-index')
```
↓
```python
# Elasticsearch
 es = ElasticsearchWrapper('openbd', 'openbd-index')
```

### ■ WebAPIの呼び出しを変更  
- APIGoogleBooks.py
```
# WebAPIのURLに引数文字列を追加
    url = 'https://www.googleapis.com/books/v1/volumes?q=isbn:' + isbn
```
↓
```
# WebAPIのURLに引数文字列を追加
    url = 'https://api.openbd.jp/v1/get?isbn=' + isbn
```

### ■ 「WebAPIのJSON」を「自分のJSON」に詰め替える  
- APIGoogleBooks.py
```python
json_data = {}
        json_data['title'] = json_api_data['items'][0]['volumeInfo']['title']
        json_data['authors'] = json_api_data['items'][0]['volumeInfo']['authors']
        json_data['publisher'] = json_api_data['items'][0]['volumeInfo']['publisher']
        json_data['publishedDate'] = json_api_data['items'][0]['volumeInfo']['publishedDate']
        json_data['description'] = json_api_data['items'][0]['volumeInfo']['description']
        json_data['thumbnail'] = json_api_data['items'][0]['volumeInfo']['imageLinks']['thumbnail']
```
↓
```python
json_data = {}
        json_data['isbn'] = json_api_data[0]['summary']['isbn']
        json_data['title'] = json_api_data[0]['summary']['title']
        json_data['publisher'] = json_api_data[0]['summary']['publisher']
        json_data['pubdate'] = json_api_data[0]['summary']['pubdate']
        json_data['cover'] = json_api_data[0]['summary']['cover']
        json_data['author'] = json_api_data[0]['summary']['author']
```

### ■ 検索画面で指定された項目を検索用dictionaryに詰め替える
- app.py

```python
 # 本家77行目前後
isbn = request.args.get('isbn', default=None)
	title = request.args.get('title', default=None)
	author = request.args.get('author', default=None)
   ・
   ・

	items = {}
	if isbn != None:
		items['isbn'] = isbn
	if title != None:
		items['title'] = title
	if author != None:
		items['authors'] = author
   ・
   ・
```
↓
```python
# 90行目前後
isbn = request.args.get('isbn', default=None)
	title = request.args.get('title', default=None)
	publisher = request.args.get('publisher', default=None)
   ・
   ・

	items = {}
	if isbn != None:
		items['isbn'] = isbn
	if title != None:
		items['title'] = title
	if publisher != None:
		items['publisher'] = publisher
   ・
   ・
```


<h2 id="アンカー7">:green_book: 苦戦した事</h2>

### １、戻ってくるJSONデータの型が「GoogleBooksAPI」と「openBD」で違う」  
- GoogleBooksAPIの場合、「 { 」から始まる  
> ![2018-12-04 14 31 40](https://user-images.githubusercontent.com/39142850/49421013-72243080-f7d1-11e8-8ac4-f66918d83010.png)
- openBDの場合、「 [ 」から始まる  
>![2018-12-04 14 31 13](https://user-images.githubusercontent.com/39142850/49421014-72243080-f7d1-11e8-844a-8f64c612dbf2.png)

@michisohokawaさんのGoogleBooksAPIの場合は、Vue.js用に「 {} 」をfor文を使い「 [] 」へ変換している  
つまり不要コードを探し削除して関連してくるエラーを消していく

- main.js(109行あたり)
```javascript
        let results_old = this.results;
        this.results = [];
        for (let value of response.data) {
          this.results.push(value);
        }
```

#### 必ずこの問題が出る訳ではない
openBD以前に試しで「YouTubeチャンネル情報API」に書き換えて作ってみたことがある。  
こちらの場合は同じGoogleのおかげか「 { 」で始まっている  
> ![2018-12-04 15 16 15](https://user-images.githubusercontent.com/39142850/49422629-f7aadf00-f7d7-11e8-8202-853c3a32e79d.png)

なのでYouTubeAPIの場合は、michihosokawaさんとほぼ同じ処理のまま  
JSONのマッピングや定義部分をYouTube用に書き換えればいい


### ２、一覧表示機能の実装

![itiran](https://user-images.githubusercontent.com/39142850/49508986-877b8680-f8c7-11e8-9c8e-9f338c1e923e.png)


## 仕組み

書籍を登録する時に 1 というダミーの値をそれぞれに忍ばせる。  
一覧表示ボタンで呼び出した時に 1 という値が付いている書籍情報を呼び出す。  
つまりすべてが表示される。

- mapping.json

```python
            },
            "author": {
                "type": "text",
                "index": true,
                "analyzer": "my_analyzer"
            },
            "dummy": {
                "type": "text",
                "index": true
            }
        }
    }
}
```

- app.py

登録時にダミーの値 1 を忍ばせる

```python
def regist():
	'''
	ISBNに対応する書籍情報を取得して、Elasticsearchに登録
	'''
	# パラメータからISBNコードを取得
	isbn = request.args.get('isbn', default=None)
	# logging.debug(isbn)



	# 必要な情報を取得する
	json_data = openBD().get_json(isbn) if isbn else {}

	if json_data == None:
		json_data = {}
	
	if len(json_data) > 0:
		# Elasticsearch
		es = ElasticsearchWrapper('openbd', 'openbd-index')
		
		json_data["dummy"] = "1"　　 # ここに 1 を忍ばせる
    
		# 追加
		es.insert_one(json_data)

	# dict型をJSON型のレスポンスに変換
	response = jsonify(json_data)

	return response
```

- app.py

1 という値のある書籍すべてを表示させる

```python
@app.route("/list")
def list():
	'''
	検索
	'''
	# 検索の項目名、項目値のDictionary
	items = {}
	items["dummy"] = "1"

	# Elasticsearch
	es = ElasticsearchWrapper('openbd', 'openbd-index')
	# 検索
	json_data = es.search_and(items)

	# dict型をJSON型のレスポンスに変換
	response = jsonify(json_data)

	return response
```

#### @michihosokawaさんから一言「設計として美しくない」

書籍すべてを表示させる為に本来あるべきでない情報を登録時に混ぜているので、  
あまり設計として好ましくないらしい、本来はElasticsearchの全検索search_allを使えば良さそうです。([先輩のapp.py](https://github.com/asuetomi/BookDB/blob/master/app.py) 一番下あたり)

<h2 id="アンカー8">:thought_balloon: 全体を通して学べた事</h2>
内容
