import pymongo
from catalog_classifier import *
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np




def getMeanAndStdPrice(model,std_cut=0):
    #model - model string from catalog
    #std_cut - how many values std*std_cut must be excluded from mean and std calculation

    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["kufar"]
    mycol = mydb["data_sold"]
    price_mean=0
    price_std=0
    
    result=mycol.find({"classificator":model})
    price=[]

    if mycol.count_documents({"classificator":model})<10:
        return []
    
    for phone in result:
        if phone.get('price')!=None and phone.get('days_for_sale')!=60:
            
            price.append(phone.get('price')/100)
            
    price=np.array(price)
    
    
    price_std=price.std()
    price_mean=price.mean()
    
    if std_cut!=0:
        price=price[price>(price_mean-(price_std*std_cut))]
        price=price[price<(price_mean+(price_std*std_cut))]
        price_std=price.std()
        price_mean=price.mean()
        
    

    return [price_mean,price_std]

def getMeanAndStdDays(model,std_cut=0):

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

    
    if std_cut!=0:
        days=days[days>(days_mean-(days_std*std_cut))]
        days=days[days<(days_mean+(days_std*std_cut))]
        days_std=days.std()
        days_mean=days.mean()
        

    return [days_mean,days_std]



def getTopSoldModels(list_length=15):

    
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["kufar"]
    mycol = mydb["data_sold"]
    
    top_models={}
    days_stat={}

    result=mycol.find({"classificator": {'$ne' : None}})
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
 
    model_stat=pd.DataFrame({"Model":k,"Q":v})    
    model_stat=model_stat.sort_values(by=['Q'],ascending=False).reset_index()
    model_stat=model_stat.drop(columns="index")
    model_stat = model_stat[model_stat.Model !='яндекс телефон']

    return model_stat.head(list_length)    
    
'''
print (getMeanAndStdPrice(clearString('samsung sm n9002 galaxy note 3 dual sim 16gb')))


print(getTopSoldModels(50))







print (getMeanAndStdPrice(clearString('apple iphone 6 16gb gold'),2))




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


    
    

  
    




