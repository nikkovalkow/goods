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
              
    del Data['']
    print(Data)
def ClearRealtAdData(Data):
    
    
    
        
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
            AdList.append(i.find('a').get("href"))
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

GetRealtAdInfo('https://realt.by/rent/flat-for-long/object/1136747/')



