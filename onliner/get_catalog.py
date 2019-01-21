# -*- coding: utf-8 -*-

from functions_kufar import *

catalog={}

for page in range(1,2):
    
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
            models.append([m,price])

        catalog[manufacture[0].text]=models

print(catalog)    


