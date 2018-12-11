import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["local"]
mycol = mydb["startup_log"]

x = mycol.find_one()
mycol.fi

print(x)
