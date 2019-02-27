# -*- coding: utf-8 -*-

from functions_kufar import *
from catalog_classifier import *
from random import random
import threading
from time import sleep



class AdScraper:


    def __init__(self,dbname,dbserver,FunctionsSetDict):
        self.database=ScraperDB(dbserver,dbname)
        self.NewADCount=0
        self.ExistADCount=0
        self.UpdatedADCount=0
        self.DeadCount=0
        self.AdSold=0
        self.AdReturn=0
        self.AdDisappeared=0

        self.TempAdList=[]
        self.TempStatusCheck=[]
        self.db_name=dbname
        self.db_server=dbserver
        self.GetAdHrefs=FunctionsSetDict['GetAdHrefsFunc']
        self.GetAdFromHref=FunctionsSetDict['GetAdFromHrefFunc']
        self.Classify=FunctionsSetDict['ClassificatorFunc']
        self.CheckAdState=FunctionsSetDict['CheckAdStateFunc']
        self.timestamp=datetime.datetime.now()


    def PutAdToTempList(self,href):
        Data=self.GetAdFromHref(href['href'],href['title'])
        if Data!=[]:
            self.TempAdList.append(Data)

    def GetDeadStatusList(self,href):
        self.TempStatusCheck.append(self.CheckAdState(href))



    def GetAdsFromPage(self,page_num,threads_quantity=1):
        threadsList=[]

        hrefs=self.GetAdHrefs(page_num)


        if hrefs==[]:
            return None

        for href in hrefs:
            threadsList.append(threading.Thread(target=self.PutAdToTempList,args=(href,)))

        active_before=threading.active_count()
        for thr in threadsList:
            thr.start()

            while threading.active_count() >= threads_quantity + active_before:
                pass
        last=0
        while threading.active_count() > active_before:
            pass

        if len(self.TempAdList)>0:
            self.PutTempAdsToDB()
        else:
            DBPutLogMessage("GetAdsFromPage() no ads to add, page num:" + str(page_num)+ ' DB: ' + self.db_name)



        return True

    def PutTempAdsToDB(self):




        for Ad in self.TempAdList:
            try:

                if self.database.Collection('data').count_documents(Ad) == 0:  # if NOT exists EXACT the same

                    if self.database.Collection('data').count_documents({'href': Ad['href']}) == 0:  # if not exists with the same URL
                        Ad['timestamp'] = self.timestamp
                        Ad['first_timestamp'] = self.timestamp
                        Ad['classificator'] = self.Classify(clearString(Ad['title']))
                        self.database.DBPutObject('data', Ad)
                        #DBPutObject(myclient,self.db_name, 'data', Ad)
                        self.NewADCount = self.NewADCount + 1
                    else:
                        newvalues = {"$set": {"timestamp": self.timestamp}}  # if exists with the same URL
                        self.database.Collection('data').update_many({'href': Ad['href']}, newvalues)
                        Ad['timestamp'] = self.timestamp
                        Ad['first_timestamp'] = self.timestamp
                        #DBPutObject(myclient,self.db_name, 'data', Ad)
                        self.database.DBPutObject('data', Ad)
                        self.UpdatedADCount = self.UpdatedADCount + 1

                else:  # if exist
                    self.ExistADCount = self.ExistADCount + 1
                    newvalues = {"$set": {"timestamp": self.timestamp}}
                    self.database.Collection('data').update_many({'href': Ad['href']}, newvalues)
            except Exception as e:
                DBPutLogMessage("PutTempAdsToDB: " + str(e))

        self.TempAdList=[]

    def FindDead(self):

        newvalues = {"$set": {"dead_timestamp": self.timestamp}}
        self.database.Collection('data').update_many({"timestamp": {'$ne': self.timestamp}}, newvalues)
        self.DeadCount = self.database.Collection('data').count_documents({"timestamp": {'$ne': self.timestamp}})
        if self.DeadCount!=0:
            DeadAd=self.database.Collection('data').find({"timestamp": {'$ne': self.timestamp}})
            self.database.Collection('data_dead').insert_many(DeadAd)
            self.database.Collection('data').delete_many({"timestamp": {'$ne': self.timestamp}})


    def RecheckDead(self,threads_quantity=1):

        self.AdReturn = 0
        self.AdSold = 0
        self.AdDisappeared = 0
        threadsList=[]
        self.TempStatusCheck=[]
        DeadList=self.database.Collection('data_dead').find({})


        for Ad in DeadList:
            threadsList.append(threading.Thread(target=self.GetDeadStatusList,args=(Ad['href'],)))

        active_before=threading.active_count()


        for thr in threadsList:

            thr.start()

            while threading.active_count() >= active_before+threads_quantity:
                pass

        while threading.active_count() > active_before:
            pass


        for ad in self.TempStatusCheck:
            href=ad[0]
            status=ad[1]
            print(ad)
            if status=='exists':

                if self.database.Collection('data').count_documents({'href': href}) == 0:
                    self.database.Collection('data').insert_many(self.database.Collection('data_dead').find({'href': href}))
                self.database.Collection('data_dead').delete_many({'href': href})
                print('delete ',href)
                self.AdReturn = self.AdReturn + 1


            elif status=='sold':
                self.database.Collection('data_sold').insert_many(self.database.Collection('data_dead').find({'href': href}))
                self.database.Collection('data_dead').delete_many({'href': href})
                print("SOLD:", href)
                self.AdSold = self.AdSold + 1
            else:
                self.AdDisappeared = self.AdDisappeared + 1

        self.TempStatusCheck=[]










            

test=AdScraper('kufar',"mongodb://localhost:27017/",
               {'GetAdHrefsFunc':GetAdHrefsKufar,'GetAdFromHrefFunc':GetAdFromHrefKufar,'ClassificatorFunc':ClassifyAd,'CheckAdStateFunc':CheckAdStateKufar})

DBPutLogMessage("START - kufar DEAD RECHECK")


test.RecheckDead(5)

DBPutLogMessage("FINISH - kufar DEAD RECHECK: return = "+str(test.AdReturn)+' sold = '+str(test.AdSold)+' disappered='+str(test.AdDisappeared))


DBPutLogMessage("START - kufar FULL SCAN")
x=0
for i in range(0,1000):
    x=x+1
    if test.GetAdsFromPage(i,5)!=True:
        break

test.FindDead()
DBPutLogMessage("FINISH - kufar FULL SCAN: New = " +
                str(test.NewADCount)+ ' Exist = ' + str(test.ExistADCount)+ ' Exist = ' + str(test.DeadCount)+" total pages = "+str(x))



