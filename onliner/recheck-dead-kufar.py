# -*- coding: utf-8 -*-
from functions_kufar import *

try:
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["kufar"]
    mycol_dead = mydb["data_dead"]
    mycol=mydb["data"]
    mycol_sold=mydb["data_sold"]
except:
    ExceptionMessage("recheck_dead.py - DB OPEN ERROR")
    exit


countSold=0
countDisappeared=0
countReturn=0
countClassifyError=0
DBPutLogMessage({'status':'dead recheck start'})
timestamp=datetime.datetime.now()
print("Dead recheck start: ",timestamp)
for i in mycol_dead.find():
    
    try:
        
        text=GetPageText(quote(i.get("href"),safe="%/:=&?~#+!$,;'@()*[]"))
        if text.find('Объявление не найдено')!=-1: # if deleted or expired
            mycol_sold.insert_many(mycol_dead.find({'href':i.get("href")}))
            mycol_dead.delete_many({'href':i.get("href")})
            print("SOLD:",i.get("href"))
            countSold=countSold+1
                    
        else: # if no AD page displayed
            text=text[text.find('function pulseTrackPhoneNumberDisplayed(event)'):text.find('function pulseTrackAdReplySubmitted')]
            if len(text)==0:
                print("DISAPIERD:",i.get("href"))
                countDisappeared=countDisappeared+1
                
                    
            else: # if AD in normal state exist
                del i['dead_timestamp']
                if mycol.count_documents({'href':i['href']})==0:
                    mycol.insert_many(mycol_dead.find({'href':i.get("href")}))
                mycol_dead.delete_many({'href':i.get("href")})
                countReturn=countReturn+1
                        
                print("RETURN:",i.get("href"))
    except:
        print('Error clasify',i.get('href'))
        countClassifyError=countClassifyError+1
print("Dead recheck finish: ",timestamp)                
DBPutLogMessage({'status':'dead recheck finish','Sold':countSold,'Disappeard':countDisappeared,'Return':countReturn,'ClassifyError':countClassifyError})            
            
        



        

        
