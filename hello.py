from flask import Flask, flash, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
import os

mongohost = str(os.environ['MONGOHOST'])

DEBUG = True
app = Flask(__name__,template_folder='./templates')
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'


mongo_uri = "mongodb://mongo:mongo@"+mongohost+":27017/prod?authSource=admin"
client = MongoClient(mongo_uri)
db = client['prod']
collection = db['prodocs']



@app.route('/')
def index():
    doc_count = collection.find().count()
    return render_template("index.html", response=doc_count)

@app.route('/aep', methods=['GET', 'POST'])
def aep():
    if request.method == "GET":
        return render_template("aep.html", response="Add more key-value pairs by clicking here")
    elif request.method == "POST":
        rowcount = int(request.form['rowcount'])
        print(rowcount)
        form_data = {}
        for i in range(rowcount):
            try:
                keyholder = "key-"+str(i)
                valholder = "value-"+str(i)
                key = request.form[keyholder]
                val = request.form[valholder]
                form_data[key] = val
            except Exception:
                continue
        print(form_data)
        if form_data:
            try:
                response = collection.insert_one(form_data).inserted_id
                response = "Inserted with id: "+str(response)
            except Exception as err:
                response = str(err)
                if (response.find('duplicate key error collection')!= -1):
                    response = "Error pattern already exists"
                else:
                    response = err
            return render_template("aep.html", response=response)
        else:
            return render_template("aep.html", response="Zero inputs!")

@app.route('/dep', methods=['GET', 'POST'])
def dep():
    if request.method == "GET":
        return render_template("dep.html")
    elif request.method == "POST":
        _id = request.form['patternid']
        try:
            response = collection.delete_one({'_id': ObjectId(_id)})
            response = str(response)

        except Exception as err:
            response = str(err)
        print(response)
        return redirect("http://localhost:5000/vep", code=302)

@app.route('/vep', methods=['GET', 'POST'])
def vep():
    if request.method == "GET":
        documents = collection.find()
        response = []
        for document in documents:
            document['_id'] = str(document['_id'])
            response.append(document)
        if not response:
            response = "Nothing found in mongo! Head over to Add-docs"
        return render_template("vep.html", response=response)
    elif request.method == "POST":
        return render_template("vep.html")

if __name__ == '__main__':
   app.run(debug=True)