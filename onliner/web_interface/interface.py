from flask import Flask
import pymongo
app = Flask(__name__)

@app.route("/log")
def hello():
	myclient = pymongo.MongoClient("mongodb://localhost:27017/")
	mydb = myclient["global"]
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
        text='<table border="1">'
        text=text+'<tr>'
        text=text+'<th>Title</th>'
        text=text+'<th>Price</th>'
        text=text+'<th>Mean price</th>'
        text=text+'<th>Profit</th>'
        text=text+'<th>Timestamp</th>'
        
        
        
        
        

        text=text+'</tr>'
        
                
        for i in mycol.find():
                
        
                text=text+'<tr>'

               
                
                text=text+'<td align="center">'
                text=text+'<a href='+i.get('href')+">"+str(i.get('title'))+'</a>'
                text=text+'</td>'
                if i.get('price')!=None:
                        price=int(int(i.get('price'))/100)
                        text=text+'<td align="center">'
                        text=text+str(int(int(i.get('price'))/100))
                        text=text+'</td>'
                else:
                        continue
                        

                text=text+'<td align="center">'
                text=text+str(int(i.get('price_mean')))
                text=text+'</td>'
                
                text=text+'<td align="center">'
                text=text+str(int(i.get('price_mean'))-price)
                text=text+'</td>'

                text=text+'<td align="center">'
                text=text+str(i.get('timestamp').strftime("%Y-%m-%d %H:%M:%S"))
                text=text+'</td>'

                text=text+'</tr>'
        text=text+"</table>"
        return(text)



        
	


if __name__ == "__main__":
    app.run(host='0.0.0.0')
