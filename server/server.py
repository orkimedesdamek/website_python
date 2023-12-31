#!/usr/bin/env python3
"""Simple website based on Flask and Pymongo"""
import os
from flask import Flask, render_template, request, redirect
from pymongo import MongoClient

APP = Flask(__name__)

"""They say it's a bad code, but why not, maybe i'll do it right way later"""
try:
    CLIENT = MongoClient("mongodb://db:27017/")
    DB_STATUS = 'Connected to DB!'
except: # pylint: disable=bare-except
    DB_STATUS = 'Failed to connect'

DB = CLIENT.website_data
TEXT_ADD = DB.text

@APP.route("/action", methods=['POST'])
def action():
    """In this function text string adds to database"""
    #Adding a Text
    textdata = request.values.get("textdata")
    TEXT_ADD.insert_one({"text":textdata})
    return redirect("/")

@APP.route('/')
#Render index
def index():
    """Rendering main page"""
    return render_template('index.html')

@APP.route('/db_list')
def db_list():
    """In this function database contents displayed on db list page"""
    #List db contents
    text_list = DB.text.find()
    return render_template('db_list.html', text2html=text_list, DB_STATUS_HTML=DB_STATUS)

if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 1234))
    APP.run(debug=True, host='0.0.0.0', port=PORT)
    