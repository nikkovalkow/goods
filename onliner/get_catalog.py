# -*- coding: utf-8 -*-

from functions_kufar import *
import pprint

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

catalog={}
''' #1k.by
for page in range(1,1000):
    
    page_text=GetPageText('https://phone.1k.by/mobile/all-list/page'+str(page))

    if page_text==None:
        break

    page=html.document_fromstring(page_text)
    sectionsList=page.find_class("item-section")
    for section in sectionsList:
        manufacture=section.find_class('item-title-category')
        

        models=[]
        for model in section.find_class('checkboxCompare'):
            m=model.text_content().replace('\t', '').replace('\n', '').replace('\r','')
            try:
                price=int(m[m.find('от')+2:m.find('б.р')].split(',')[0].replace(' ',''))
            except:
                price=0
                
            m=m[:m.find("от")]
            models.append([m,price,0])

        DBPutObject(myclient,'kufar','catalog',{'manufature':manufacture[0].text,'models':models})
        
'''

#smartphone.ua

page_text=GetPageText('http://www.smartphone.ua/phones/')
page=html.document_fromstring(page_text)

page=page.find_class('cols')
manufacture_name=''

model_list=[]
for m in page:
    for link in m:
        url=link[0].get('href')
        
        for pageNum in range (1,100):
            page2_text=GetPageText(url+'_page'+str(pageNum)+'.html')
            page2=html.document_fromstring(page2_text)
            page2=page2.find_class('green')
            if len(page2)<2: break
            for phone in page2:
                
                phone_model=phone.text_content()
                manufacture_name=phone_model[:phone_model.find(' ')].strip().lower()
                phone_model=phone_model[phone_model.find(' ')+1:].strip().lower()
                model_list.append(phone_model)
        print(manufacture_name,model_list)
        DBPutObject(myclient,'kufar','catalog2',{'manufature':manufacture_name,'models':model_list})
        model_list=[]
        
                





