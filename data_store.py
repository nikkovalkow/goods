import pymongo
import datetime

def DBOpen():
    #open DB and return collection pointer
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["realt"]
    mycol = mydb["rent_long"]
    
    return mycol
    
def DBAdd(db_col,advert):
    #add advert. to collection + add timestamp
    #print(datetime.datetime.strptime(str(datetime.datetime.now()).split(),'%Y-%m-%d %H:%M:%S'))
    advert['timestamp']=datetime.datetime.now()
    return db_col.insert_one(advert)

def CheckDBAdverChange(db_col,advert):
    return db_col.count_documents(advert)
    
    

col=DBOpen()
x=col.count_documents({"URL":"https://realt.by/rent/flat-for-long/object/1389652/"})
a=col.find({"URL":"https://realt.by/rent/flat-for-long/object/1389652/"},{"_id":0})
print (x)
