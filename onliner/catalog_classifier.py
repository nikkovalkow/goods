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


def compareStrings(str1,str2):
    result=[]
    wordResult=[]
    
    for word1 in str1.split(' '):
        for word2 in str2.split(' '):         
            wordResult.append(compareWords(word1,word2))
            print(compareWords(word1,word2),'/',word1,'/',word2)
        result.append(wordResult)
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




objList=mycol.find({}).limit(100)

for i in objList:  
    title=i['title'].replace('\r','').replace('\n','').replace('\t','').replace('  ','').lower()
    compareStrings('Iphone 6s'.lower(),title.lower())
   

#print(LivenstainDistance('s6','blackview'))    


    
    


    

