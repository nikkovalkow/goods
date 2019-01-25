import pymongo
from catalog_classifier import *

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["kufar"]
mycol = mydb["data_sold"]

days_stat={}

result=mycol.find({"classificator":None})
x=0
print ('To clasify:',mycol.count_documents({"classificator":None}))
for o in result:
    days=(o['dead_timestamp']-o['release_timestamp']).days
    classify=ClassifyAd(o['title'])    
       
    newvalues = { "$set": { "classificator": classify } } 
    mycol.update_many({'href':o['href']},newvalues)
    newvalues = { "$set": { "days_for_sale": days } } 
    mycol.update_many({'href':o['href']},newvalues)
    x=x+1
    print('item: ',x)
    print(classify)
    print(clearString(o.get('title')))
    
    



        
'''
title='Iphone 7-32gb бу оригинал все работает'
title='Iphone 6s gold 64'


#print(tanimotok('apple iphone 6s 16gb space gray новый','apple iphone 6s'))
#print(tanimotok('apple iphone 6s 16gb space gray новый','apple iphone 6s plus'))

cat1=ClassifyAdCat(title5,'catalog')
#cat2=ClassifyAdCat(title6,'catalog')

print(cat1)
#print(cat2)

'''
