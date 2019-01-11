# -*- coding: utf-8 -*-
import datetime
from urllib.request import Request, urlopen
import urllib.error
import lxml.html as html
import pymongo
from urllib.parse   import quote

from random import randint
import time

def DBPutLogMessage(message):
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["onliner"]
    mycol = mydb["log"]
    
    msg={"time":datetime.datetime.now(),"msg":message}
    mycol.insert_one(msg)


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
    page=html.document_fromstring(page_text)
    AdList=page.find_class("list_ads__title")
   
    for i in AdList:
        print(i.text_content())
        print(i.get("href"))
        print(GetPageText(quote(i.get("href"),safe="%/:=&?~#+!$,;'@()*[]")))
        

page=GetPageText("https://www.kufar.by/"+quote('минск_город/Телефоны')+'?cu=BYR&phce=1&o=100')
GetKufarAdList(page)




#print(quote('минск_город/Телефоны?cu=BYR&phce=1&o=100'))
