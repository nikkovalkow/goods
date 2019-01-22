# -*- coding: utf-8 -*-

from functions_kufar import *



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

#Коэффициент Жаккара (частное — коэф. Танимото) NOT INCLUDED


def compareWords(str1,str2):
    len1=len(str1)
    len2=len(str2)
    maxLen=max(len1,len2)
    averageLen=(len1+len2)/2
    return((maxLen-LivenstainDistance(str1,str2))/maxLen)


def compareStrings(str1,str2,c):
    result=[]
    wordResult=[]
    
    for word1 in str1.split(' '):
        wordResult=[]
        for word2 in str2.split(' '):         
            compResult=compareWords(word1,word2)
            if compResult>=c:
                result.append(1)
                break
            
        
    return result
            
            
        
    



try:
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["kufar"]
    mycol_catalog = mydb["catalog"]
    mycol=mydb["data"]
    mycol_sold=mydb["data_sold"]
except:
    ExceptionMessage("recheck_dead.py - DB OPEN ERROR")
    exit




objList=mycol.find({}).limit(10000)

for i in objList:
    
    title=i['title'].replace('\r','').replace('\n','').replace('\t','').replace('  ','').lower()
    result=compareStrings('iphone 6s'.lower(),title.lower(),0.8)
    if len(result)>1: print(result,title,i.get('price'))
   

#print(LivenstainDistance('s6','blackview'))    


    
    


    

