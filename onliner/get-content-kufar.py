# -*- coding: utf-8 -*-

from functions_kufar import *
from catalog_classifier import *
from random import random
import threading
from time import sleep



class AdScraper:
    def __init__(self,dbname,FunctionsSetDict):
        self.HrefsList=[]
        self.db_name=dbname
        self.GetAdHrefs=FunctionsSetDict['GetAdHrefsFunc']
        self.GetAdFromHref=FunctionsSetDict['GetAdFromHrefFunc']
        self.Classify=FunctionsSetDict['ClassificatorFunc']
        self.timestamp=datetime.datetime.now()

    def GetAdsFromPage(self,page_num,threads_quantity=1):
        threadsList=[]

        hrefs=self.GetAdHrefs(page_num)

        if hrefs==[]:
            return None

        for href in hrefs:

            threadsList.append(threading.Thread(target=self.GetAdFromHref,args=(href['href'])))


        return True





    def GetAllHrefs(self):

        page_counter=0
        for page in range (0,1000):
            hrefs=self.GetAdHrefs(page_num)
            if hrefs==[]:
                break
            else:
                page_counter=page_counter+1
                self.HrefsList.extend(hrefs)
        return page_counter







def GetAdHrefsKufar(page_num):

    page_text=GetPageText("https://www.kufar.by/" + quote('минск_город/Телефоны') + '?cu=BYR&phce=1&o=' + str(page_num))

    if page_text.find('Ничего не найдено, поиск расширен')==-1 :
        page = html.document_fromstring(page_text)
        AdList = page.find_class("list_ads__title")
        ResultList=[]
        for Ad in AdList:
            try:
                ResultList.append({'href':quote(Ad.get('href'),safe="%/:=&?~#+!$,;'@()*[]"),'title':clearString(Ad.text_content())})
            except:
                continue
        return ResultList
    else:
        return []


def GetAdFromHrefKufar(href,title):

    try:

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
    except Exception as e:
        DBPutLogMessage("GetAdFromHrefKufar(href,title) AD add failed link:" + href + ' ' + str(e))
        return []





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

#page = GetPageText("https://www.kufar.by/" + quote('минск_город/Телефоны') + '?cu=BYR&phce=1&o=' + str(2))
#ListOfHref=GetPageAdLinkListKufar(page)
#Ad=GetAdFromHrefKufar(ListOfHref[0][0],ListOfHref[1][0])

test=AdScraper('test',{'GetAdHrefsFunc':GetAdHrefsKufar,'GetAdFromHrefFunc':GetAdFromHrefKufar,'ClassificatorFunc':ClassifyAd})
print(test.GetAdsFromPage(1))
#pprint.pprint(ListOfHref)
'''
def test():
    num=int(random()*10)+1
    print('start ',num)
    sleep(num)
    print('end ',num)
    return num

th_list=[]
for i in range (0,10):
    th_list.append(threading.Thread(target=test))

for i in range (0,10):
    th_list[i].start()

old_count=0
while True:

    count=threading.activeCount()
    if count!=old_count:
        print('Threads:',count)
        old_count=count
    if count==1:
        print('Finsih all')
        break

'''






