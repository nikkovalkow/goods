import pymongo
from catalog_classifier import *

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["kufar"]
mycol = mydb["data_sold"]

days_stat={}

result=mycol.find({"days_for_sale":None},no_cursor_timeout=True)
x=0
print ('To clasify:',mycol.count_documents({"days_for_sale":None}))

for o in result:
    
    
    days=(o['dead_timestamp']-o['release_timestamp']).days

    if (o.get('classificator')==None) or o.get('classificator')==[]:
        classify=ClassifyAd(o['title'])
        newvalues = { "$set": { "classificator": classify } } 
        mycol.update_many({'href':o['href']},newvalues)
    else:
        classify=o.get('classificator')
        
       
    
    newvalues = { "$set": { "days_for_sale": days } } 
    mycol.update_many({'href':o['href']},newvalues)
    x=x+1
    print('item: ',x)
    print(classify)
    print(clearString(o.get('title')))
result.close()    
    



        

