import datetime
from urllib.request import Request, urlopen
import urllib.error
import lxml.html as html
from data_store import * 

def ExceptionMessage(command):
    print(command)
    
def GetPageText(url):

# Gets URL as text, return URL contenet as text,
# in case of HTML error returns Error code
# in case of non-HTML error retuens None

    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    
    try:
        response=urlopen(req)
    except urllib.error.HTTPError as e:  
        ExceptionMessage("HTTP ERROR: "+str(e.code)+" "+url) 
        return e.code
    except:
        return None
    
    
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
#delete unnecessary data from dict
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
            ExceptionMessage("ClearRealtAdData() STO ERROR: ")
            ExceptionMessage(Data['Ориентировочная стоимость эквивалентна'])
            pass
            

    if 'Телефоны' in Data:
        try:
            Data['Телефоны']=Data['Телефоны'][Data['Телефоны'].find('+'):]
        except:
            ExceptionMessage("ClearRealtAdData() ERROR: ")
            ExceptionMessage(Data)
            pass
    if 'E-mail' in Data:
        try:
            Data['E-mail']=Data['E-mail'].replace('(собачка)','@')
        except:
            ExceptionMessage("ClearRealtAdData() ERROR: ")
            ExceptionMessage(Data)
            pass
    if 'Площадь общая/жилая/кухня' in Data:
        try: 
            Data['Площадь общая/жилая/кухня']=Data['Площадь общая/жилая/кухня'].split('/')[0]
        except:
            ExceptionMessage("ClearRealtAdData() ERROR: ")
            ExceptionMessage(Data)
            pass

    if 'Дата обновления' in Data:
        try:
            Data['Дата обновления']=datetime.datetime.strptime(Data['Дата обновления'],'%Y-%m-%d')
        except:
            ExceptionMessage("ClearRealtAdData() ERROR: ")
            ExceptionMessage(Data)
            pass
     
    
    return Data
    
    
    
        
def AnalyzeRealtPage(PageURL):
    #get list of links to flat advert on realt.by
    
    page=GetPageText(PageURL)
    
    
    if len(page)<4 :
        return False
    
    Collection=DBOpen()
    #extracting links, addding to DB
    page=html.document_fromstring(page)
    page=page.find_class("bd-table")
    if len(page)!=0:
            
        page=page[0].find_class('ad')
    
        for i in page:
            
            ad_info=GetRealtAdInfo(i.find('a').get("href"))

            if CheckDBAdverChange(Collection,ad_info)==0:
                print ("ADD",i.find('a').get("href"))
                DBAdd(Collection,ad_info)
            else:
                print("Exist")

            
    else:
        return False
    return True
     


result=True
i=0
while result!=False:
    result=AnalyzeRealtPage('http://realt.by/rent/flat-for-long/?search=all&page='+str(i))
    print("Page ",i)
    i=i+1   
  


#print(GetRealtAdInfo('https://realt.by/rent/flat-for-long/object/1136747/'))

#AnalyzeRealtPage('https://realt.by/rent/flat-for-long/?search=all&page=20')
#print(GetPageText("http://learnin.ru"))



