from flask import Flask
import pymongo
app = Flask(__name__)

@app.route("/log")
def hello():
	myclient = pymongo.MongoClient("mongodb://localhost:27017/")
	mydb = myclient["kufar"]
	mycol = mydb["log"]

	
	
	lst=[]
	for i in mycol.find():
    		lst.append(i)
    		lst.append('<br><br>')

	return(str(lst))

@app.route("/essential")
def essential():
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["kufar"]
        mycol = mydb["data_essential"]
        text='<table>'
        for i in mycol.find():
                
        
                text=text+'<tr>'
                
                text=text+'<td>'
                text=text+'<a href='+i.get('href')+">"+str(i.get('title'))+'</a>'
                text=text+'</td>'
                if i.get('price')!=None:
                        
                        text=text+'<td>'
                        text=text+str(int(i.get('price'))/100)
                        text=text+'</td>'
                else:
                        text=text+'<td>'
                        text=text+str(0)
                        text=text+'</td>'
                        

                text=text+'<td>'
                text=text+str(int(i.get('price_mean')))
                text=text+'</td>'
                
                text=text+'<td>'
                text=text+str(int(i.get('price_std')))
                text=text+'</td>'

                text=text+'</tr>'
        text=text+"</table>"
        return(text)



        
	


if __name__ == "__main__":
    app.run(host='0.0.0.0')
