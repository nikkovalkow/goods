import pymongo
from catalog_classifier import *

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["kufar"]
mycol = mydb["data"]


result=mycol.find({"classificator":None},no_cursor_timeout=True)
x=0
print ('To clasify:',mycol.count_documents({"classificator":None}))

for o in result:
    
    
    classify=ClassifyAd(o)
       
    newvalues = { "$set": { "classificator": classify } } 
    mycol.update_many({'href':o['href']},newvalues)
    
    x=x+1
    print('item: ',x)
    print(classify)
    print(clearString(o.get('title')))
result.close()
    
    



        

