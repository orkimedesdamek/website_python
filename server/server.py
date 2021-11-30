#!/usr/bin/env python3
"""Simple website based on Flask and Pymongo"""
import os
from flask import Flask, render_template, request, redirect
#import pymongo
from pymongo import MongoClient

#from dotenv import load_dotenv

#load_dotenv()

APP = Flask(__name__)

#TAG = os.getenv('TAG')
#container_name = website_mongo_TAG

try:
    CLIENT = MongoClient('website_mongo', 27017)
    DB_STATUS = 'Connected to DB!'
except: # pylint: disable=bare-except
    DB_STATUS = 'Failed to connect'

DB = CLIENT.website_data
TEXT_ADD = DB.text

@APP.route("/action", methods=['POST'])
"""In this function text string adds to database"""
def action():
    #Adding a Text
    textdata = request.values.get("textdata")
    TEXT_ADD.insert({"text":textdata})
    return redirect("/")

@APP.route('/')
#Render index
"""Rendering main page"""
def index():
    return render_template('index.html')

@APP.route('/db_list')
"""In this function database contents displayed on db list page"""
def db_list():
    #List db contents
    text_list = DB.text.find()
    return render_template('db_list.html', text2html=text_list, DB_STATUS_HTML=DB_STATUS)

if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 1234))
    APP.run(debug=True, host='0.0.0.0', port=PORT)
