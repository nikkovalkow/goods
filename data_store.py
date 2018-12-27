# -*- coding: utf-8 -*-


import pymongo
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as sp


    
    
def DBPutLogMessage(message):
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["realt"]
    mycol = mydb["log"]
    
    msg={"time":datetime.datetime.now(),"msg":message}
    mycol.insert_one(msg)
    
 

def DBOpen():
    #open DB and return collection pointer
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["realt"]
    mycol = mydb["rent_long"]
    
    return mycol
    
def DBAdd(db_col,advert):
    #add advert. to collection + add timestamp
    #print(datetime.datetime.strptime(str(datetime.datetime.now()).split(),'%Y-%m-%d %H:%M:%S'))
    #advert['timestamp']=datetime.datetime.now()
    return db_col.insert_one(advert)

def CheckDBAdverChange(db_col,advert):
    return db_col.count_documents(advert)

def DBChangeSetAdverTimeStamp(db_col,advert,timestamp):
 
    newvalues = { "$set": { "timestamp": timestamp } }
    db_col.update_one(advert, newvalues)
    
    
    
'''
col=DBOpen()
x=col.count_documents({"URL":"https://realt.by/rent/flat-for-long/object/1389652/"})
a=col.find({"URL":"https://realt.by/rent/flat-for-long/object/1389652/"},{"_id":0})
print (x)
'''

col=DBOpen()
cursor=col.find({"Населенный пункт":"Минск","Район города":{"$regex" :".*Первомайский.*"}},{"Ориентировочная стоимость эквивалентна":1,'Площадь общая/жилая/кухня':1})
'''
for i in cursor:
    r=col.find({"_id":i.get("_id")},{"Ориентировочная стоимость эквивалентна":1})
    
    try:
        x=int(r[0]['Ориентировочная стоимость эквивалентна'])
    except:
        col.remove({"_id":i.get("_id")})
 

       
for i in cursor:
    r=col.find({"_id":i.get("_id")},{"Площадь общая/жилая/кухня":1})
    
    try:
        s=str(r[0]['Площадь общая/жилая/кухня']).split('.')[0].replace(" ","")
        
        x=int(s)
    except:
        #print (s)
        col.remove({"_id":i.get("_id")})
               

'''
#print (cursor[100])

df =  pd.DataFrame(list(cursor))

del df["_id"]
#print(np.percentile(df["Ориентировочная стоимость эквивалентна"],50))
a=[int(float(x)) for x in df["Площадь общая/жилая/кухня"]]
b=[int(float(x)) for x in df["Ориентировочная стоимость эквивалентна"]]
#print (b)
#plt.scatter(a, b)
a=np.array(a)
b=np.array(b)
print(np.corrcoef(a,b))
am =a.mean()
bm=b.mean()
astd=a.std()
bstd=b.std()
print ("Before ",len(a))

k=0
for i in b:
    if (i>(bm+bstd)) or i<(bm-3*bstd) or a[k]>(am+3*astd) or a[k]<(am-3*astd):
        a=np.delete(a,k)
        b=np.delete(b,k)
print(np.corrcoef(a,b))
print ("After ",len(a))
        
    

plt.scatter(a,b)
plt.show()





