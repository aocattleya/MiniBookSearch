from elasticsearch import Elasticsearch
import copy

class ElasticsearchWrapper:
    '''
    Elasticsearch 呼び出し ラッパー
        ・Elasticsearch自身はすでにサービスとして稼働しているものとする
        ・pythonの「elasticsearch」モジュールは事前にインストールすること
    '''
    def __init__(self, doc_type:str, index:str):
        '''
        初期化

        Parameters
        ----------
        doc_type : str
            ドキュメントタイプの名前
        index : str
            インデックスの名前
        '''
        self.es=Elasticsearch("localhost:9200")
        self.doc_type=doc_type
        self.index=index
    
    def delete_index(self):
        '''
        すでに存在するINDEXを削除する
        '''
        try:
            self.es.indices.delete(index=self.index)
        except:
            pass

    def make_index(self, setting:dict, mapping:dict):
        '''
        ElasticsearchのINDEX登録処理

        Parameters
        ----------
        setting : dict
            setting指定のJSONデータ
        mapping : dict
            mapping指定のJSONデータ
        '''
        # settingsを指定してインデックスを作成
        self.es.indices.create(index=self.index, body=setting)
        
        # 作成したインデックスのマッピングを指定
        self.es.indices.put_mapping(index=self.index, doc_type=self.doc_type, body=mapping)

    def insert_one(self, doc:dict):
        '''
        1データを登録する

        Parameters
        ----------
        doc : dict
            登録するJSONデータ
        '''
        self.es.index(index=self.index, doc_type=self.doc_type, body=doc)
        # id で連番を振っておくと、idでgetできるようになる
        # id を指定しないと、内部で任意のユニークな文字列が割り当てられる
        # ここでは、登録順の番号での取得はしないし、検索にはdoc内の項目を用いるので
        # id無しの登録でよい
        #self.es.index(index=self.index, doc_type=self.doc_type, body=doc, id=idx)

    def insert_array(self, docs:list):
        '''
        配列データを登録する

        Parameters
        ----------
        docs : list of dict
            登録するJSONデータの配列
        '''
        for doc in docs:
            self.es.index(index=self.index, doc_type=self.doc_type, body=doc)

    def search_and(self, items:dict, count:int = 10):
        '''
        ディクショナリで定義された項目（名前、値）のAND条件での検索を行う

        Parameters
        ----------
        items : dict
            項目（名前、値）の一覧
        count : int
            検索結果の上限数、無指定の場合の初期値10
        '''
        query = {
            "query": {
                "bool" : {
                    "must":[{"match":{key : val}} for key, val in items.items()]
                }
            }
        }

        return self.__search(query, count)

    def __search(self, query:dict, count:int):
        '''
        queryで指定された検索式で、Elasticsearchを検索する

        Parameters
        ----------
        query : dict
            Elasticsearchの検索Query
        count : int
            検索結果の上限数
        '''
        results = []
        params = {
            'size':count
        }
        for i in self.es.search(index=self.index, doc_type=self.doc_type, body=query, params=params)["hits"]["hits"]:
            body = copy.deepcopy(i["_source"])
            score = i['_score']
            result = {'body':body, 'score':score}
            results.append(result)
        return results
 