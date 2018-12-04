import json
import requests

class openBD:
    '''
    openBD API
    '''
    def __init__(self):
        '''
        初期化
        '''
        pass

    def get_json(self, isbn:str) -> dict:
        '''
        openBD API の呼び出しで戻ってきた書籍データから、必要な情報を抜き出して整形する

        Parameters
        ----------
        isbn : str
            登録する書籍のISBNコード
            '-'を除いた英数字の文字列
        Returns
        -------
        json : dic
            書籍データ
            呼び出しに失敗した場合はNone
        '''
        # WebAPIを呼び出してJSONを取得する
        json_api_data = self.__call_web_api(isbn)

        # 呼び出しが失敗した場合
        if json_api_data == None:
            return None
        
        # 検索結果が0だった場合
        if json_api_data[0] == None:
            return None
        # 呼び出しが成功した場合
        # 必要な情報だけを抜き出して新しいJSONを作成する
        # Elasticsearchの項目（'mapping.json'で定義）と項目を揃えること
        json_data = {}
        json_data['isbn'] = json_api_data[0]['summary']['isbn']
        json_data['title'] = json_api_data[0]['summary']['title']
        json_data['publisher'] = json_api_data[0]['summary']['publisher']
        json_data['pubdate'] = json_api_data[0]['summary']['pubdate']
        json_data['cover'] = json_api_data[0]['summary']['cover']
        json_data['author'] = json_api_data[0]['summary']['author']
        # json_data['cover'] = json_api_data['items'][0]['volumeInfo']['imageLinks']['cover']

        # isbnコードが込み入った形で格納されている
        # industryIdentifiers = json_api_data['items'][0]['volumeInfo']['industryIdentifiers']
        # for item in industryIdentifiers:
        #     if item['type'] == 'ISBN_13':
        #         json_data['isbn'] = item['identifier']
        #         break

        return json_data
        
    def __call_web_api(self, isbn:str) -> dict:
        '''
        openBD API を呼び出して、ISBNに対応するJSONデータを受け取る

        Parameters
        ----------
        isbn : str
            書籍のISBNコード
        Returns
        -------
        json_data : dic
            書籍のJSONデータ
            呼び出しに失敗した場合はNone
        '''
        # WebAPIのURLに引数文字列を追加
        url = 'https://api.openbd.jp/v1/get?isbn=' + isbn

        # WebAPIの呼び出し
        response = requests.get(url)

        # 呼び出しの成否をチェック
        status_code = response.status_code
        if status_code != 200:
            # 失敗した場合
            return None

        # 呼び出し成功した場合
        # 返ってきたJSON文字列を取得する
        json_text = response.text      

        # JSON文字列を辞書型に変換する
        json_data = json.loads(json_text)

        return json_data

if __name__ == "__main__":
    api = openBD()
    data = api.get_json('9784797389463')
    print(data)
