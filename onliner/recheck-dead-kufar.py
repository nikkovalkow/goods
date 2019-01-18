import pymongo
from urllib.parse   import quote
from urllib.request import Request, urlopen

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
            ErrorCount=ErrorCount+1
            pass
        except:
            ExceptionMessage("HTTP ERROR: NO TYPE")
            time.sleep(5)
            ErrorCount=ErrorCount+1
            pass
    if ErrorCount==3:
        return None
    else:
        response.encoding='UTF-8'
        data = response.read()
        encoding = response.headers.get_content_charset('utf-8')
        
        return data.decode(encoding)


try:
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["kufar"]
    mycol_dead = mydb["data_dead"]
    mycol=mydb["data"]
    mycol_sold=mydb["data_sold"]
except:
    print('ERROR OPEN DB in RECHECK DEAD')
    exit 

for i in mycol_dead.find():
    
    try:
        
        text=GetPageText(quote(i.get("href"),safe="%/:=&?~#+!$,;'@()*[]"))
        if text.find('Объявление не найдено')!=-1:
            mycol_sold.insert_many(mycol_dead.find({'href':i.get("href")}))
            mycol_dead.delete_many({'href':i.get("href")})
            print("SOLD:",i.get("href"))
                
        else:
            text=text[text.find('function pulseTrackPhoneNumberDisplayed(event)'):text.find('function pulseTrackAdReplySubmitted')]
            if len(text)==0:
                print("DISAPIERD:",i.get("href"))
                
            else:
                del i['dead_timestamp']
                if mycol.count_documents({'href':i['href']})==0:
                    mycol.insert_many(mycol_dead.find({'href':i.get("href")}))
                mycol_dead.delete_many({'href':i.get("href")})
                    
                print("RETURN:",i.get("href"))
    except:
        print('Error clasify',i.get('href'))
                
            
            
        



        

        
