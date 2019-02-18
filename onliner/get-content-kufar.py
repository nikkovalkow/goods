# -*- coding: utf-8 -*-

from functions_kufar import *
from catalog_classifier import *

def GetPageAdLinkListKufar(page_text):

    page = html.document_fromstring(page_text)
    AdList = page.find_class("list_ads__title")
    ResultHrefList=[quote(Ad.get('href'),safe="%/:=&?~#+!$,;'@()*[]") for Ad in AdList]
    ResultTitleList=[Ad.text_content() for Ad in AdList]
    return [ResultHrefList,ResultTitleList]

def GetAdFromHrefKufar(href,title):

    text = GetPageText(quote(href, safe="%/:=&?~#+!$,;'@()*[]"))
    releaseDate = text[text.find('releaseDate'):text.find('releaseDate') + 50]
    releaseDate = releaseDate[releaseDate.find('=') + 2:releaseDate.find('/') - 1]
    releaseDate = datetime.datetime.strptime(releaseDate, "%Y-%m-%d %H:%M:%S")
    text = text[
           text.find('function pulseTrackPhoneNumberDisplayed(event)'):text.find('function pulseTrackAdReplySubmitted')]
    text = text[text.find('object'):text.find('});') + 1]

    # Converting JS object to DICT
    ADdict = demjson.decode("{" + text)

    # restructurizing DICT to one level
    del ADdict['origin']
    del ADdict['name']
    del ADdict['provider']
    del ADdict['type']
    del ADdict['deployStage']
    del ADdict['deployTag']
    ADdict['object']['inReplyTo']['cust_name'] = ADdict['object']['name']
    ADdict['object']['inReplyTo']['phone'] = ADdict['object']['telephone']
    ADdict = ADdict['object']['inReplyTo']
    ADdict['Region'] = ADdict['location']['addressRegion']
    ADdict['Subarea'] = ADdict['location']['addressSubarea']
    ADdict['href'] = href
    ADdict['title'] = title
    ADdict['release_timestamp'] = releaseDate
    del ADdict['location']
    return ADdict





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
            
def FindDead(timestamp):
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["kufar"]
    mycol = mydb["data"]
    mycol_dead=mydb['data_dead']
    newvalues = { "$set": { "dead_timestamp": timestamp } }
    mycol.update_many({ "timestamp": { '$ne':timestamp } },newvalues)
    deadCount=mycol.count_documents({ "timestamp": { '$ne':timestamp } })
    mycol_dead.insert_many(mycol.find({ "timestamp": { '$ne':timestamp } }))
    
    mycol.delete_many({ "timestamp": { '$ne':timestamp } })
    return deadCount
            
'''        
        

timestamp=datetime.datetime.now()
totalNew=0
totalEdited=0
totalExist=0
pageNum=0
print("Start:  "+str(timestamp))
DBPutLogMessage({'status':'start','timestamp':timestamp})

for pageNum in range (0,1000):
    
    page=GetPageText("https://www.kufar.by/"+quote('минск_город/Телефоны')+'?cu=BYR&phce=1&o='+str(pageNum))

    if page.find('Ничего не найдено, поиск расширен')==-1:
        pageNum=pageNum+1
        t1 = time.perf_counter()

        resultList=GetKufarAdList(page)

        t2 = time.perf_counter()
        
        
        
        totalData=PutDictListToDB(resultList,timestamp)
        print(t2-t1,'sec.  ',totalData,'  ',timestamp)
       
        totalNew=totalNew+int(totalData[0])
        totalEdited=totalEdited+int(totalData[2])
        totalExist=totalExist+int(totalData[1])
        print("Page: ",pageNum," ",totalData)
        DBPutLogMessage({'page':pageNum,'data':totalData})
        
        
    else:
        print("Finish: "+str(datetime.datetime.now()))
        
        
       
        break
totalDead=FindDead(timestamp)
print("Dead: "+str(totalDead))

DBPutLogMessage({'status':'end','timestamp':timestamp,'New':totalNew,'Exist':totalExist,'Edited':totalEdited,'Dead':totalDead})


#db.data.createIndex({"description":"text","title":"text"})
#db.data.find({$text: {$search: "iphone"}}, {score: {$meta: "textScore"}}).sort({score:{$meta:"textScore"}})

'''
print('Hi')
page = GetPageText("https://www.kufar.by/" + quote('минск_город/Телефоны') + '?cu=BYR&phce=1&o=' + str(2))
ListOfHref=GetPageAdLinkListKufar(page)
Ad=GetAdFromHrefKufar(ListOfHref[0][0],ListOfHref[1][0])
pprint.pprint(Ad)




