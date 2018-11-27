#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
アプリケーションの初期化
    ・Elasticsearchの初期化
        既存のINDEXの削除
        setting.json, mapping.json を読み込んでINDEXを設定
''' 
from ElasticsearchWrapper import ElasticsearchWrapper
import json

if __name__ == '__main__':
    # 
    es = ElasticsearchWrapper("opendb", "opendb-index")

    # すでに存在するインデックスを削除する
    # 存在しないインデックスに対して呼び出すとExceptionなのでpassさせておく
    try:
        es.delete_index()
    except:
        pass

    # INDEX作成用情報の読み込み
    setting_file = 'setting.json'
    mapping_file = 'mapping.json'

    with open(setting_file, 'r', encoding='utf-8') as f:
        setting = json.load(f)
    
    with open(mapping_file, 'r', encoding='utf-8') as f:
        mapping = json.load(f)

    # インデックスを作成
    es.make_index(setting, mapping)
