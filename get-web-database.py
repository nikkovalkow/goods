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
     

    
i=69
result=True

while result!=False:
    result=AnalyzeRealtPage('https://realt.by/rent/flat-for-long/?search=all&page='+str(i))
    print(i,result)
       
    i=i+1
       



