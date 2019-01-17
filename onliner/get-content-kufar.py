# -*- coding: utf-8 -*-
import datetime
from urllib.request import Request, urlopen
import urllib.error
import lxml.html as html
import pymongo
from urllib.parse   import quote

from random import randint
import time
import pprint

import demjson
import time
import sys


def DBPutLogMessage(message):
    try:
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["kufar"]
        mycol = mydb["log"]
        
        msg={"time":datetime.datetime.now(),"msg":message}
        mycol.insert_one(msg)
    except:
        print("DBPutLogMessage() DB open error  "+str(datetime.datetime.now()))

def DBPutObject(db_client,db_name, collection_name, dict_obj):

    try:
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient[db_name]
        mycol = mydb[collection_name]
        mycol.insert_one(dict_obj)
    except:
        print("DBPutObject() DB open error " + str(datetime.datetime.now()))
        
    
    


def GetPageText(url):

# Gets URL as text, return URL contenet as text,
# in case of HTML error returns Error code
# in case of non-HTML error retuens None
    ErrorCount=0
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    
    for i in range (0,3):
        
        try:
            response=urlopen(req)
        except urllib.error.HTTPError as e:  
            ExceptionMessage("HTTP ERROR: "+str(e.code)+" "+url)
            time.sleep(5)
            ErrorCount=ErrorCount+1
            pass
        except:
            ExceptionMessage("HTTP ERROR: NO TYPE")
            time.sleep(5)
            ErrorCount=ErrorCount+1
            pass
    if ErrorCount==3:
        return None
    else:
        response.encoding='UTF-8'
        data = response.read()
        encoding = response.headers.get_content_charset('utf-8')
        
        return data.decode(encoding)

def ExceptionMessage(command):
    DBPutLogMessage(command)
    
    

def GetKufarAdList(page_text):
    #puts information from one of the kufar googs list page into DICT
    #input - text of listing page
    #outpout - list of dicts, each dict is one AD on listing page
    page=html.document_fromstring(page_text)
    
    AdList=page.find_class("list_ads__title")
    x=0
    resultList=[]
    for i in AdList:
        try:         
            #extracting JajaScriptObject from page
            text=GetPageText(quote(i.get("href"),safe="%/:=&?~#+!$,;'@()*[]"))
            text=text[text.find('function pulseTrackPhoneNumberDisplayed(event)'):text.find('function pulseTrackAdReplySubmitted')]
            text=text[text.find('object'):text.find('});')+1]              
            
            #Converting JS object to DICT
            ADdict=demjson.decode("{"+text)
            
            #restructurizing DICT to one level
            del ADdict['origin']
            del ADdict['name']
            del ADdict['provider']
            del ADdict['type']
            del ADdict['deployStage']
            del ADdict['deployTag']
            ADdict['object']['inReplyTo']['cust_name']=ADdict['object']['name']
            ADdict['object']['inReplyTo']['phone']=ADdict['object']['telephone']
            ADdict=ADdict['object']['inReplyTo']
            ADdict['Region']=ADdict['location']['addressRegion']
            ADdict['Subarea']=ADdict['location']['addressSubarea']
            ADdict['href']=i.get("href")
            ADdict['title']=i.text_content()
            del ADdict['location']
            resultList.append(ADdict)
        except:
            DBPutLogMessage("GetKufarADList() AD add failed link:" - i.get("href"))
            
            
    return resultList    
            
def PutDictListToDB(adList,timestamp):
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["kufar"]
    mycol = mydb["data"]
    NewADCount=0
    ExistADCount=0
    UpdatedADCount=0
    for Ad in adList:
        if mycol.count_documents(Ad)==0:                #if NOT exists EXACT the same

            if mycol.count_documents({'href':Ad['href']})==0: #if not exists with the same URL
                Ad['timestamp']=timestamp
                Ad['first_timestamp']=timestamp
                DBPutObject(myclient,'kufar','data',Ad)
                NewADCount=NewADCount+1
            else:
                newvalues = { "$set": { "timestamp": timestamp } } # if exists with the same URL
                mycol.update_many({'href':Ad['href']},newvalues)
                print(Ad['href'])
                Ad['timestamp']=timestamp
                Ad['first_timestamp']=timestamp
                DBPutObject(myclient,'kufar','data',Ad)
                UpdatedADCount=UpdatedADCount+1
                
        else:                                           #if exist
            ExistADCount=ExistADCount+1
            newvalues = { "$set": { "timestamp": timestamp } }
            mycol.update_many(Ad,newvalues)
            
            
    return [NewADCount,ExistADCount,UpdatedADCount]
            
def FindDead(timestamp):
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["kufar"]
    mycol = mydb["data"]
    mycol_dead=mydb['data_dead']
    { "carrier.state": { '$ne': "NY" } }

    newvalues = { "$set": { "dead_timestamp": timestamp } }
    
    mycol.update_many({ "timestamp": { '$ne':timestamp } },newvalues)
    mycol_dead.insert_many(mycol.find({ "timestamp": { '$ne':timestamp } }))
    mycol.delete_many({ "timestamp": { '$ne':timestamp } })
            
        
        

timestamp=datetime.datetime.now()



for pageNum in range (0,1):
    
    page=GetPageText("https://www.kufar.by/"+quote('минск_город/Телефоны')+'?cu=BYR&phce=1&o='+str(pageNum))

    if page.find('поиск расширен на всю страну')==-1:
        t1 = time.perf_counter()

        resultList=GetKufarAdList(page)

        t2 = time.perf_counter()
        
        print(t2-t1)
        print((t2-t1)/len(resultList))
        print(PutDictListToDB(resultList,timestamp))
        
        
    else:
        result={''}
       
        break

FindDead(timestamp)






