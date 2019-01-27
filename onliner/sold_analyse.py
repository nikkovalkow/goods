import pymongo
from catalog_classifier import *
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np




def getMeanAndStdPrice(model):

    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["kufar"]
    mycol = mydb["data_sold"]

    
    result=mycol.find({"classificator":model})
    price=[]
    
    if mycol.count_documents({"classificator":model})<10:
        return []
    for phone in result:
        if phone.get('price')!=None:
            price.append(phone.get('price')/100)
            
    price=np.array(price)
    
    price_std=price.std()
    price_mean=price.mean()

    return [price_mean,price_std]

def getMeanAndStdDays(model):

    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["kufar"]
    mycol = mydb["data_sold"]

    
    result=mycol.find({"classificator":model})
    days=[]
    if mycol.count_documents({"classificator":model})<10:
        return []
    
    for phone in result:
        if phone.get('days_for_sale')!=None:
            days.append(phone.get('days_for_sale'))
            
    days=np.array(days)
    
    days_std=days.std()
    days_mean=days.mean()

    return [days_mean,days_std]



def printTopSoldModels():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["kufar"]
    mycol = mydb["data_sold"]
    
    
    days_stat={}

    result=mycol.find({"classificator": {'$ne' : None}})
    print ('To analyse:',mycol.count_documents({"classificator": {'$ne' : None}}))
    model_stat={}
    # clear from yandex phone
    #mycol.delete_many({"classificator":'яндекс телефон'})
    x=0
    for o in result:
      
        
        try:
            model=o['classificator'][2]
        except:
            print (o['id'])
            mycol.delete_one({"_id":o['_id']})
            x=x+1 
        if model_stat.get(model)==None:
            
            model_stat[model]=1
        else:
            model_stat[model]=model_stat[model]+1


               
    k=list(model_stat.keys())
    v=list(model_stat.values())
    print (k[0])
    model_stat=pd.DataFrame({"Model":k,"Q":v})    
    model_stat=model_stat.sort_values(by=['Q'],ascending=False).reset_index()
        
    for ind in model_stat.index:
        Q=model_stat['Q'][ind]
        model=model_stat['Model'][ind]
        print (model_stat['Model'][ind], model_stat['Q'][ind])
        print(getMeanAndStdPrice(model_stat['Model'][ind]))
        #result=mycol.find({"classificator": model})
        if Q<15: break




'''

print (getMeanAndStdPrice('apple iphone 7 32gb rose gold'))
print (getMeanAndStdDays('apple iphone 7 32gb rose gold'))


myclient = pymongo.MongoClient("mongodb://192.168.100.104:27017/")
mydb = myclient["kufar"]
mycol = mydb["data_sold"]
    
result=mycol.find({"classificator":'apple iphone 7 32gb rose gold'})
price=[]
days=[]
for phone in result:
    if phone.get('price')!=None:
        price.append(phone.get('price')/100)
        days.append(phone['days_for_sale'])
        #if phone['days_for_sale']<2:
        #    print(phone['cust_name'],phone['phone'],phone['description'],phone['release_timestamp'],phone['price'])
       # if phone['days_for_sale']>20:
       #     print('BAD',phone['days_for_sale'],phone['cust_name'],phone['phone'],phone['description'],phone['release_timestamp'],phone['price'])

price=np.array(price)
days=np.array(days)

print(price)
print(days)

plt.scatter(price,days)
plt.show()
price_std=price.std()
price_mean=price.mean()

days_std=days.std()
days_mean=days.mean()

print("MEAN: ",price_mean)
print('STD:', price_std)

'''


    
    

  
    




