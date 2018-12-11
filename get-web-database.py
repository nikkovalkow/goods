from urllib.request import Request, urlopen
import urllib.error

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
    info=response.info()
    
    return data
    
    
        
#def RealtGetRentList():
    
    
test=GetPageText('https://realt.by/rent/flat-for-long/?search=all')
test=GetPageText('https://realt.by/rent/flat-for-long/?search=all&page=78')
print(test)


