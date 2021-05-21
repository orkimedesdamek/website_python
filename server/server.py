#!/usr/bin/env python3
from flask import Flask, render_template, request, redirect
import os
import pymongo
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

TAG = os.getenv('TAG')
container_name = website_mongo_TAG

try:
 client = MongoClient(container_name,27017)
 db_status = 'Connected to DB!'
except:
 db_status = 'Failed to connect'

db = client.website_data
text_add = db.text

@app.route("/action", methods=['POST'])
def action ():
        #Adding a Text
        textdata = request.values.get("textdata")
        text_add.insert({ "text":textdata})
        return redirect("/")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/db_list')
def db_list():
    text_list = db.text.find()
    return render_template('db_list.html',tasks=text_list,db_status_html=db_status)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 1234))
    app.run(debug=True,host='0.0.0.0',port=port)