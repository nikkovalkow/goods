# -*- coding: utf-8 -*-

import functions_kufar

try:
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["kufar"]
    mycol_dead = mydb["data_dead"]
    mycol=mydb["data"]
    mycol_sold=mydb["data_sold"]
except:
    print('ERROR OPEN DB in RECHECK DEAD')
    exit 

for i in mycol_dead.find():
    
    try:
        
        text=GetPageText(quote(i.get("href"),safe="%/:=&?~#+!$,;'@()*[]"))
        if text.find('Объявление не найдено')!=-1:
            mycol_sold.insert_many(mycol_dead.find({'href':i.get("href")}))
            mycol_dead.delete_many({'href':i.get("href")})
            print("SOLD:",i.get("href"))
                
        else:
            text=text[text.find('function pulseTrackPhoneNumberDisplayed(event)'):text.find('function pulseTrackAdReplySubmitted')]
            if len(text)==0:
                print("DISAPIERD:",i.get("href"))
                
            else:
                del i['dead_timestamp']
                if mycol.count_documents({'href':i['href']})==0:
                    mycol.insert_many(mycol_dead.find({'href':i.get("href")}))
                mycol_dead.delete_many({'href':i.get("href")})
                    
                print("RETURN:",i.get("href"))
    except:
        print('Error clasify',i.get('href'))
                
            
            
        



        

        
