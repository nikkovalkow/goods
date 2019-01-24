import pymongo
from catalog_classifier import *
'''
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["kufar"]
mycol = mydb["data_sold"]

days_stat={}

result=mycol.find()

for o in mycol.find():
    days=(o['dead_timestamp']-o['release_timestamp']).days
    if days==1:
        classify=ClassifyAD(o['title'])    
        if classify[0]>1:
            print(ClassifyAD(o['title']),o['title'])
            print('---------------------------------------------------')
    if days_stat.get(days)!=None:
        days_stat[days]=days_stat[days]+1
    else:
        days_stat[days]=1

pprint.pprint(days_stat)

        
'''
title='apple iphone 3g s 32gb'
title1 ='apple iphone 3g s 32gb'
title3='Meizu m3s'
title4='IPhone 6s 16GB Gold'
title5='Apple iPhone 6s 16Gb Space Gray Новый'
title6='Apple Iphone 6 Space Gray НЕ РЕФ'
title7 ='IPhone 8 gold 64Gb'
title8='Iphone 6s 64gb'

#print(tanimotok('apple iphone 6s 16gb space gray новый','apple iphone 6s'))
#print(tanimotok('apple iphone 6s 16gb space gray новый','apple iphone 6s plus'))

cat1=ClassifyAdCat(title5,'catalog')
cat2=ClassifyAdCat(title6,'catalog')
print(cat1)
