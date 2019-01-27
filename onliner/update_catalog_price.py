from sold_analyse import *

def updatePriceDiviation():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["kufar"]
    mycol = mydb["catalog"]
    for model in mycol.find():
        price=getMeanAndStdPrice(clearString(model['model']))
        if price!=[]:
            print(clearString(model['model']))
            print(price)


updatePriceDiviation()

    
    
