# -*- coding: utf-8 -*-
import datetime
from urllib.request import Request, urlopen
import urllib.error
import pymongo
from urllib.parse   import quote
import time
import demjson
import time



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
    print(command)
    
