# -*- coding: utf-8 -*-
import datetime
from urllib.request import Request, urlopen
import urllib.error
import lxml.html as html
from data_store import *
from random import randint
import time


NewAdvertize=0
ChangedAdvertize=0
NotChangedAdvertize=0

def SpecialDelay():
    rnd=randint(0,100)
    if rnd<5:
        time.sleep(randint(0,5))
        
        
    elif rnd<50:
        time.sleep(randint(0,2))
        
        
    elif rnd<80:
        time.sleep(randint(0,1))
        
    else:
        return         
        
        

def ExceptionMessage(command):
    DBPutLogMessage(command)
    
    
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
            ErrorCount=ErroprCount+1
            pass
        except:
            ExceptionMessage("HTTP ERROR: NO TYPE")
            time.sleep(5)
            ErrorCount=ErroprCount+1
            pass
    if ErrorCount==3:
        return None
    else:
        data = response.read()
        return data
    
def GetRealtAdInfo(AdURL):
    #Gets info about flat to dict

    page=GetPageText(AdURL)
    if len(page)<4 :
        ExceprionMessage("HTTP ERROR: No data on page "+AdURL)
        return False

    #extracting table and put to Dict
    
    page=html.document_fromstring(page)
    LeftRow=page.find_class("table-row-left")
    RightRow=page.find_class("table-row-right")
    LeftRow=[i.text_content().replace(".","") for i in LeftRow]
    RightRow=[i.text_content() for i in RightRow]
    Data=dict(zip(LeftRow,RightRow))
    Data["URL"]=AdURL          
      
    return ClearRealtAdData(Data)

def ClearRealtAdData(Data):
#delete unnecessary data from dict/ format the data
    try:
        del Data['']
    except:
        pass
    
    if 'Ориентировочная стоимость эквивалентна' in Data:
        try:
            Data['Ориентировочная стоимость эквивалентна']=Data['Ориентировочная стоимость эквивалентна'].replace(u'\xa0','')
            Data['Ориентировочная стоимость эквивалентна']=Data['Ориентировочная стоимость эквивалентна'][:Data['Ориентировочная стоимость эквивалентна'].find('р')]
            Data['Ориентировочная стоимость эквивалентна']=int(Data['Ориентировочная стоимость эквивалентна'])
        except:
            Data['Ориентировочная стоимость эквивалентна']=0
            ExceptionMessage("ClearRealtAdData() ERROR: 1")
            ExceptionMessage(Data['Ориентировочная стоимость эквивалентна'])
            pass
            

    if 'Телефоны' in Data:
        try:
            Data['Телефоны']=Data['Телефоны'][Data['Телефоны'].find('+'):]
        except:
            ExceptionMessage("ClearRealtAdData() ERROR: 2 ")
            ExceptionMessage(Data)
            pass
    if 'E-mail' in Data:
        try:
            Data['E-mail']=Data['E-mail'].replace('(собачка)','@')
        except:
            ExceptionMessage("ClearRealtAdData() ERROR: 3 ")
            ExceptionMessage(Data)
            pass
    if 'Площадь общая/жилая/кухня' in Data:
        try: 
            Data['Площадь общая/жилая/кухня']=int(float(Data['Площадь общая/жилая/кухня'].split('/')[0]))
        except:
            ExceptionMessage("ClearRealtAdData() ERROR: 4 ")
            ExceptionMessage(Data)
            pass

    if 'Дата обновления' in Data:
        try:
            Data['Дата обновления']=datetime.datetime.strptime(Data['Дата обновления'],'%Y-%m-%d')
        except:
            ExceptionMessage("ClearRealtAdData() ERROR: 5 ")
            ExceptionMessage(Data)
            pass
     
    
    return Data
    
    
    
        
def AnalyzeRealtPage(PageURL,TimeStamp):
    #get list of links to flat advert on realt.by
    

    page=GetPageText(PageURL)

    global NewAdvertize
    global ChangedAdvertize
    global NotChangedAdvertize
    
    
    try:
        if len(page)<4 :
            ExceptionMessage("ERROR PAGE LEN<4: "+str(page))
            return False
    except:
            ExceptionMessage("ERROR PAGE LEN<4: "+str(page))
            return False
    
    Collection=DBOpen()

    #extracting links, addding to DB
    page=html.document_fromstring(page)
    page=page.find_class("bd-table")
            
    page=page[0].find_class('ad')
    
    for i in page:
            


        SpecialDelay()

        
        ad_info=GetRealtAdInfo(i.find('a').get("href"))


        if CheckDBAdverChange(Collection,ad_info)==0:                #if exact the same NOT exists

            if CheckDBAdverChange(Collection, {'URL':ad_info['URL']})==0: # if with the same URL NOT exists
                NewAdvertize=NewAdvertize+1
                ad_info['timestamp']=TimeStamp
                DBAdd(Collection,ad_info)              
            else:                                                                   # if with the same URL exists
                ChangedAdvertize=ChangedAdvertize+1
                ad_info['timestamp']=TimeStamp
                DBAdd(Collection,ad_info)
                    
        else:
            NotChangedAdvertize=NotChangedAdvertize+1               #if exact the same exists
            DBChangeSetAdverTimeStamp(Collection,ad_info,TimeStamp)

    
        
    return True
     


result=True
i=0

ExceptionMessage("Start scan")

while result!=False:
    result=AnalyzeRealtPage('http://realt.by/rent/flat-for-long/?search=all&page='+str(i),datetime.datetime.now())
    print("Page ",i)
    i=i+1

ExceptionMessage("Scan complete - New: "+ str(NewAdvertize)+" Changed: "+str(ChangedAdvertize)+ " Unchanged: "+str(NotChangedAdvertize))



  




