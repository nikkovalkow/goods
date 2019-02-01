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

    page=html.document_fromstring(page_text)
    
    AdList=page.find_class("list_ads__title")
    x=0
    resultList=[]
    for i in AdList:
        try:         
            if mycol.count_documents({'href':quote(i.get("href"),safe="%/:=&?~#+!$,;'@()*[]")})==0:
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
                Ad['classificator']=ClassifyAd(clearString(Ad['title']))
                DBPutObject(myclient,'kufar','data',Ad)
                NewADCount=NewADCount+1
            else:
                newvalues = { "$set": { "timestamp": timestamp } } # if exists with the same URL
                mycol.update_many({'href':Ad['href']},newvalues)
                Ad['timestamp']=timestamp
                Ad['first_timestamp']=timestamp
                DBPutObject(myclient,'kufar','data',Ad)
                UpdatedADCount=UpdatedADCount+1
                
        else:                                           #if exist
            ExistADCount=ExistADCount+1
            newvalues = { "$set": { "timestamp": timestamp } }
            mycol.update_many(Ad,newvalues)
            
            
    return [NewADCount,ExistADCount,UpdatedADCount]
            

            
        
        

timestamp=datetime.datetime.now()

pageNum=0
print("Start:  "+str(timestamp))

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["kufar"]
mycol = mydb["data"]

for pageNum in range (0,1000):
    
    page=GetPageText("https://www.kufar.by/"+quote('минск_город/Телефоны')+'?cu=BYR&phce=1&o='+str(pageNum))

    if page.find('Ничего не найдено, поиск расширен')==-1:
    
        pageNum=pageNum+1
        print('page ',pageNum)    

        resultList=GetKufarNewAdList(page)
        for ad in resultList:
            
            print ("NEW",ad['title'])
            

              
        
        
                
        
    else:
        print("Finish: "+str(datetime.datetime.now()))
        
        
       
        break











