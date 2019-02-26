# -*- coding: utf-8 -*-

from functions_kufar import *


myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["kufar"]
mycol = mydb["catalog"]

mycol.create_index([("manufacture","text"),("model","text")])
search_str=clearString("Xiaomi Redmi 6. Чёрный. Гарант 12 мес.3/32ГБ")
result=mycol.find({'$text': {'$search':search_str }}, {'score': {'$meta': "textScore"}})
#result=result.collection.find({'$text': {'$search': "4"}}, {'score': {'$meta': "textScore"}})
#.sort({'score':{'$meta':"textScore"}})
print('new search------------------------------')
print(result.count())
for i in result:
    print(i.get('model'))


        



