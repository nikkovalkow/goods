# -*- coding: utf-8 -*-

from functions_kufar import *
from catalog_classifier import *
    

def GetKufarNewAdList(page_text):
    #puts information from one of the kufar googs list page into DICT
    #input - text of listing page
    #outpout - list of dicts, each dict is one AD on listing page
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["kufar"]
    mycol = mydb["data"]
    mycol_operational=mydb["data_operational"]

    page=html.document_fromstring(page_text)
    
    AdList=page.find_class("list_ads__title")
    x=0
    resultList=[]
    for i in AdList:
        try:         
            if mycol.count_documents({'href':i.get("href")})==0 and mycol_operational.count_documents({'href':i.get("href")})==0:
                #extracting JajaScriptObject from page
                text=GetPageText(quote(i.get("href"),safe="%/:=&?~#+!$,;'@()*[]"))
                releaseDate=text[text.find('releaseDate'):text.find('releaseDate')+50]
                releaseDate=releaseDate[releaseDate.find('=')+2:releaseDate.find('/')-1]
                releaseDate=datetime.datetime.strptime(releaseDate,"%Y-%m-%d %H:%M:%S")
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
                ADdict['release_timestamp']=releaseDate
                del ADdict['location']
                resultList.append(ADdict)
        except Exception as e:
            
            DBPutLogMessage("GetKufarADList() AD add failed link:" + i.get("href")+' '+str(e))
            
            
    return resultList    
            

def AnalyseNewList(new_list):
    return 0
            
        
        

timestamp=datetime.datetime.now()

pageNum=0
print("Start:  "+str(timestamp))

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["kufar"]
mycol = mydb["data"]


newCount=0
for pageNum in range (0,1000):
    
    page=GetPageText("https://www.kufar.by/"+quote('минск_город/Телефоны')+'?cu=BYR&phce=1&o='+str(pageNum))

    if page.find('Ничего не найдено, поиск расширен')==-1:
    
        pageNum=pageNum+1
        print('page ',pageNum)    

        resultList=GetKufarNewAdList(page)
        for ad in resultList:
            newCount=newCount+1

        print ("NEW",newCount)
        newCount=0
            

              
        
        
                
        
    else:
        print("Finish: "+str(datetime.datetime.now()))
        
        
       
        break











