import pymongo
import datetime

def DBOpen():
    #open DB and return collection pointer
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["realt"]
    mycol = mydb["rent_long"]
    
    return mycol
    
def DBAdd(db_col,advert):
    #add advert. to collection
    #print(datetime.datetime.strptime(str(datetime.datetime.now()).split(),'%Y-%m-%d %H:%M:%S'))
    advert['timestamp']=datetime.datetime.now()
    return db_col.insert_one(advert)
    

def AddAd(ad_dict):
   for i in ad_dict:
       i=0
    
