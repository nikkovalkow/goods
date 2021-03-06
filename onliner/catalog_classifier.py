# -*- coding: utf-8 -*-

from functions_kufar import *
import pprint

class Timer(object):
    def __init__(self):
        pass
    


#Расстояние_Левенштейна

def LivenstainDistance(a, b):
    #"Calculates the Levenshtein distance between a and b."
    n, m = len(a), len(b)
    if n > m:
        # Make sure n <= m, to use O(min(n,m)) space
        a, b = b, a
        n, m = m, n

    current_row = range(n+1) # Keep current and previous row, not entire matrix
    for i in range(1, m+1):
        previous_row, current_row = current_row, [i]+[0]*n
        for j in range(1,n+1):
            add, delete, change = previous_row[j]+1, current_row[j-1]+1, previous_row[j-1]
            if a[j-1] != b[i-1]:
                change += 1
            current_row[j] = min(add, delete, change)

    return current_row[n]

#Коэффициент Жаккара (частное — коэф. Танимото) 

def tanimotok(s1, s2):
    a, b, c = len(s1), len(s2), 0.0

    for sym in s1:
        if sym in s2:
            c += 1

    return c / (a + b - c)


def clearString(str1):
    str1=str1.replace('\r','').replace('\n','').replace('\t','').replace('(',' ')
    str1=str1.replace(')',' ').replace(',',' ').replace('.','').replace('-',' ')
    str1=str1.replace('  ','').lower().strip()
    return str1
    


def compareWords(str1,str2):
    len1=len(str1)
    len2=len(str2)
    maxLen=max(len1,len2)
    averageLen=(len1+len2)/2
    return((maxLen-LivenstainDistance(str1,str2))/maxLen)


def compareStrings(str1,str2,c):
    
    result=[]
    wordResult=[]
    lastResult=0
    
    for word1 in str1.split(' '):
        lastResult=0
        for word2 in str2.split(' '):         
            compResult=compareWords(word1,word2)
            if compResult>lastResult:
                lastResult=compResult
        if lastResult!=0 and lastResult>=c:
            result.append(lastResult)         
        
    return result

def countWords(str1):
    text=str1.strip()
    text=text.rstrip()
    c=0
    for word in text.split(' '):
        c=c+1
    return c            
            
        
    







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


    
    
   







    
            
    


            





    
    


    

