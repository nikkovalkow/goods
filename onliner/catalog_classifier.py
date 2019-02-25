# -*- coding: utf-8 -*-

from functions_kufar import *
import pprint


    



        
    







def ClassifyAdCat(title,catalog_name):
    #classify AD based on single catalog
    Result=[]
    

    try:
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["kufar"]
        mycol_catalog = mydb[catalog_name]
    except:
        ExceptionMessage("catalog_classifier.py - DB OPEN ERROR")
        return None
   
 
    catalog=mycol_catalog.find()

    
   
    
    lastResult=0
    lastTanimoto=0
    for manufacture in catalog: # for each manufacturer
        

        
           
        mdl=clearString(manufacture['model'])      #remove extra characters from model title
        title=clearString(title)        #remove extra characters from AD title
        compResult=compareStrings(mdl,title,0.8) # how many words are pretty the same
        tanimotoResult=compareWords(mdl,title)*tanimotok(mdl,title) # whats the difference between strings based on Livenstain*Tanimoto
            
            
                        
        if len(compResult)>lastResult:  # compare how many identical words are in the model and title
            Result=[]
            lastResult=len(compResult)
            lastTanimoto=tanimotoResult
            Result.append([len(compResult),tanimotoResult,mdl,manufacture['manufacture'].strip().lower()])
        elif len(compResult)==lastResult:
            if tanimotoResult>lastTanimoto and tanimotoResult<1:
                lastTanimoto=tanimotoResult
                Result=[]
                Result.append([len(compResult),tanimotoResult,mdl,manufacture['manufacture'].strip().lower()])
            elif tanimotoResult==lastTanimoto:
                 Result.append([len(compResult),tanimotoResult,mdl,manufacture['manufacture'].strip().lower()])
                    
                
                
    if len(Result)>0:
        return Result[0]
    else:
        return []

def ClassifyAd(iteam):
    try:
        return ClassifyAdCat(iteam,'catalog')
    except:
        return []
        
   






def ClearCatalog():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["kufar"]
    mycol_catalog = mydb['catalog']
    mycol_catalog.delete_many({'manufacture':'2017'})
    mycol_catalog.delete_many({'manufacture':'2018'})


    
    
   







    
            
    


            





    
    


    

