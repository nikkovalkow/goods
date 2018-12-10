from urllib.request import Request, urlopen
import urllib.error

def GetPageText(url):

# Gets URL as text, return [Text,Info],
# in case of HTML error returns [Ecode,Ecode]
# in case of non-HTML error retuens [None,None] 

    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})

    try:
        response=urlopen(req)
    except urllib.error.HTTPError as e:  
        return [e.code,e.code]
    except:
        return [None,None]
    
    
    data = response.read()
    info=response.info()
    
    return [data,info]
    
    
        
    
print (GetPageText('https://by.ebay.com/b/Cell-Phones-Smartphones/9355/bn_320094')[0])



