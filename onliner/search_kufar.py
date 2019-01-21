# -*- coding: utf-8 -*-

from functions_kufar import *


myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["kufar"]
mycol = mydb["data"]

mycol.create_index([("description","text"),("title","text")])
result=mycol.find({'$text': {'$search': "Redmi 4x -note -3 -5 -6 -8 -7 -5C -6s -5s -8s -7s -SE -X -XS -3G -3gs"}}, {'score': {'$meta': "textScore"}})
#result=result.collection.find({'$text': {'$search': "4"}}, {'score': {'$meta': "textScore"}})
#.sort({'score':{'$meta':"textScore"}})

for i in result:
    try:
        price=int(i.get('price'))
    except:
        price=0
        
    print(price/100 )


