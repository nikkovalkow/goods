# -*- coding: utf-8 -*-

from functions_kufar import *
from catalog_classifier import *
from random import random
import threading
from time import sleep



class AdScraper:


    def __init__(self,dbname,dbserver,FunctionsSetDict):

        self.NewADCount=0
        self.ExistADCount=0
        self.UpdatedADCount=0
        self.DeadCount=0

        self.TempAdList=[]
        self.db_name=dbname
        self.db_server=dbserver
        self.GetAdHrefs=FunctionsSetDict['GetAdHrefsFunc']
        self.GetAdFromHref=FunctionsSetDict['GetAdFromHrefFunc']
        self.Classify=FunctionsSetDict['ClassificatorFunc']
        self.timestamp=datetime.datetime.now()


    def PutAdToTempList(self,href):
        self.TempAdList.append(self.GetAdFromHref(href['href'],href['title']))



    def GetAdsFromPage(self,page_num,threads_quantity=1):
        threadsList=[]

        hrefs=self.GetAdHrefs(page_num)

        if hrefs==[]:
            return None

        for href in hrefs:
            threadsList.append(threading.Thread(target=self.PutAdToTempList,args=(href,)))

        for thr in threadsList:
            thr.start()
            while threading.active_count() >= threads_quantity:
                pass
        while threading.active_count() > 1:
            pass
        self.PutTempAdsToDB()


        return True

    def PutTempAdsToDB(self):
        myclient = pymongo.MongoClient(self.db_server)
        mydb = myclient[self.db_name]
        mycol = mydb["data"]
        NewADCount = 0
        ExistADCount = 0
        UpdatedADCount = 0

        for Ad in self.TempAdList:
            if mycol.count_documents(Ad) == 0:  # if NOT exists EXACT the same

                if mycol.count_documents({'href': Ad['href']}) == 0:  # if not exists with the same URL
                    Ad['timestamp'] = self.timestamp
                    Ad['first_timestamp'] = self.timestamp
                    Ad['classificator'] = self.Classify(clearString(Ad['title']))
                    DBPutObject(myclient, self.db_name, 'data', Ad)
                    self.NewADCount = self.NewADCount + 1
                else:
                    newvalues = {"$set": {"timestamp": self.timestamp}}  # if exists with the same URL
                    mycol.update_many({'href': Ad['href']}, newvalues)
                    Ad['timestamp'] = self.timestamp
                    Ad['first_timestamp'] = self.timestamp
                    DBPutObject(myclient, self.db_name, 'data', Ad)
                    self.UpdatedADCount = self.UpdatedADCount + 1

            else:  # if exist
                self.ExistADCount = self.ExistADCount + 1
                newvalues = {"$set": {"timestamp": self.timestamp}}
                mycol.update_many(Ad, newvalues)
        self.TempAdList=[]

    def FindDead(self):
        myclient = pymongo.MongoClient(self.db_server)
        mydb = myclient[self.db_name]
        mycol = mydb["data"]
        mycol_dead = mydb['data_dead']
        newvalues = {"$set": {"dead_timestamp": self.timestamp}}
        mycol.update_many({"timestamp": {'$ne': self.timestamp}}, newvalues)
        self.DeadCount = mycol.count_documents({"timestamp": {'$ne': self.timestamp}})
        mycol_dead.insert_many(mycol.find({"timestamp": {'$ne': self.timestamp}}))
        mycol.delete_many({"timestamp": {'$ne': self.timestamp}})




            


test=AdScraper('test',"mongodb://localhost:27017/",{'GetAdHrefsFunc':GetAdHrefsKufar,'GetAdFromHrefFunc':GetAdFromHrefKufar,'ClassificatorFunc':ClassifyAd})
print(test.GetAdsFromPage(1,5))
print("New: ",test.NewADCount)
test.FindDead()
print("Dead:",test.DeadCount)



