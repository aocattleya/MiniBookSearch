![booksearch](https://user-images.githubusercontent.com/39142850/49347869-33b14780-f6e5-11e8-9e8b-7e9a270c58c8.png)

## :green_book: 詳しい内容：Qiita

#### [【Python+Flask】WebAPIを使った簡易書籍管理アプリ【Elasticsearch、Vue.js】](https://qiita.com/aocattleya/items/c374e87b42a14a01e77c)

こちらに簡易書籍管理システムについての内容をまとめています。

## :green_book: 開発環境

- Python  
- Flask  
- Elasticsearch  
- Vue.js  
- VSCode（Visual Studio Code）  

## :green_book: アプリ機能

### 1、書籍の登録  

世界共通で図書を認識する為に記載される書籍の裏に書かれている番号です。

![booksearch](https://user-images.githubusercontent.com/39142850/49347869-33b14780-f6e5-11e8-9e8b-7e9a270c58c8.png)

### 2、書籍の検索  

登録した書籍とマッチする検索結果が表示される

![knsk](https://user-images.githubusercontent.com/39142850/49414266-2021e180-f7b6-11e8-9afc-0fbed0b580d3.png)

### 3、書籍の詳細表示  

検索結果をクリックすると「openBD」から受け取った書籍情報が表示される

![knskkk](https://user-images.githubusercontent.com/39142850/49414765-d6d29180-f7b7-11e8-91f5-91308a8f732e.png)

### 4、一覧表示機能

これまでに登録した書籍をすべて表示させる機能です。

![knskk](https://user-images.githubusercontent.com/39142850/49415597-9de7ec00-f7ba-11e8-8ae6-c9a7c8277400.png)

## :green_book: 全体的な仕組み

![minibooksearch](https://user-images.githubusercontent.com/39142850/49472249-4b5a0e80-f852-11e8-9022-4596ca655e19.png)

## :green_book: 動作環境

Python（Flask） ＋ Elasticsearch　内部で『openBD』を呼び出して動作しています。

- Java1.8
	- Elasticsearchを動作させるのに必要（JREではなくJDK）
- Elasticsearch6.3
	- 2つのプラグインをインストール  
		- ICU Analysis
		- Japanese (Kuromoji) Analysis
	- http://localhost:9200 でアクセスできることを確認する
- pip install elasticsearch
- pip install Flask

## :green_book: 使用方法
**1、python initialize.py**  
Elasticseachの初期化、「setting.json」「mapping.json」を参照しています。  
すでに、当該INDEXが作成されていた場合には、そのINDEXは削除されます。

**2、python app.py**  
Flask＋アプリの実行、次のような画面が出れば成功  
![Screenshot_20181219-214044.jpg](https://qiita-image-store.s3.amazonaws.com/0/307359/9a02ff2e-5b57-f4d0-43f8-f4e9921c6473.jpeg)

**3、ブラウザでアクセス**  
http://localhost:8080
