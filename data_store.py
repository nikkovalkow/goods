import pymongo
import datetime


    
    
def DBPutLogMessage(message):
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["realt"]
    mycol = mydb["log"]
    
    msg={"time":datetime.datetime.now(),"msg":message}
    mycol.insert_one(msg)
    
 

def DBOpen():
    #open DB and return collection pointer
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["realt"]
    mycol = mydb["rent_long"]
    
    return mycol
    
def DBAdd(db_col,advert):
    #add advert. to collection + add timestamp
    #print(datetime.datetime.strptime(str(datetime.datetime.now()).split(),'%Y-%m-%d %H:%M:%S'))
    #advert['timestamp']=datetime.datetime.now()
    return db_col.insert_one(advert)

def CheckDBAdverChange(db_col,advert):
    return db_col.count_documents(advert)

def DBChangeSetAdverTimeStamp(db_col,advert,timestamp):
    myquery = { "address": "Valley 345" }
    newvalues = { "$set": { "timestamp": timestamp } }
    db_col.update_one(advert, newvalues)
    
    
    
'''
col=DBOpen()
x=col.count_documents({"URL":"https://realt.by/rent/flat-for-long/object/1389652/"})
a=col.find({"URL":"https://realt.by/rent/flat-for-long/object/1389652/"},{"_id":0})
print (x)
'''
