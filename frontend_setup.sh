#!/bin/bash

cd ~/50.043_DBBD/flaskapp
python3 -m pip install pymongo
python3 -m pip install pymysql
export FLASK_APP=app.py
#flask run

cd ../amplifyapp
npm install
npm install --save-dev concurrently
npm run dev
