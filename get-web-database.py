from urllib.request import Request, urlopen
import urllib.error
import lxml.html as html

def GetPageText(url):

# Gets URL as text, return URL contenet as text,
# in case of HTML error returns Error code
# in case of non-HTML error retuens None

    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})

    try:
        response=urlopen(req)
    except urllib.error.HTTPError as e:  
        return e.code
    except:
        return None
    
    
    data = response.read()
    
    
    return data
    
def GetRealtAdInfo(AdURL):
    #Gets info about flat to dict

    page=GetPageText(AdURL)
    if len(page)<4 :
        return False

    #extracting table and put to Dict
    
    page=html.document_fromstring(page)
    LeftRow=page.find_class("table-row-left")
    RightRow=page.find_class("table-row-right")
    LeftRow=[i.text_content() for i in LeftRow]
    RightRow=[i.text_content() for i in RightRow]
    Data=dict(zip(LeftRow,RightRow))
              
      
    return ClearRealtAdData(Data)

def ClearRealtAdData(Data):
#delete unnecessary data from dict
    try:
        del Data['']
    except:
        print("Clean error")
    if 'Ориентировочная стоимость эквивалентна' in Data:
       Data['Ориентировочная стоимость эквивалентна']=Data['Ориентировочная стоимость эквивалентна'].replace(u'\xa0','')
       Data['Ориентировочная стоимость эквивалентна']=Data['Ориентировочная стоимость эквивалентна'][:Data['Ориентировочная стоимость эквивалентна'].find('р')]
    if 'Телефоны' in Data:
        Data['Телефоны']=Data['Телефоны'][Data['Телефоны'].find('+'):]
    if 'E-mail' in Data:
        Data['E-mail']=Data['E-mail'].replace('(собачка)','@')
    if 'Площадь общая/жилая/кухня' in Data:   
        Data['Площадь общая/жилая/кухня']=Data['Площадь общая/жилая/кухня'].split('/')[0]
    
    return Data
    
    
    
        
def AnalyzeRealtPage(PageURL):
    #get list of links to flat advert on realt.by
    
    page=GetPageText(PageURL)
    AdList=[]
    
    if len(page)<4 :
        return False

    #extracting links
    page=html.document_fromstring(page)
    page=page.find_class("bd-table")
    if len(page)!=0:
            
        page=page[0].find_class('ad')
        for i in page:
            print(i.find('a').get("href"))
            print(GetRealtAdInfo(i.find('a').get("href")))
    else:
        return False
    return True
     

'''    
i=69
result=True

while result!=False:
    result=AnalyzeRealtPage('https://realt.by/rent/flat-for-long/?search=all&page='+str(i))
    print(i,result)
       
    i=i+1
'''

#print(GetRealtAdInfo('https://realt.by/rent/flat-for-long/object/1136747/'))

AnalyzeRealtPage('https://realt.by/rent/flat-for-long/?search=all&page=70')



