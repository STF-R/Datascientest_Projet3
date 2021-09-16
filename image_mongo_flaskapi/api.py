import random
import pandas as pd
from flask import Flask
import os
import json
from flask import jsonify
from flask import make_response
from flask import abort, request
import requests
from pymongo import MongoClient
import time
from pprint import pprint

time.sleep(12)
##API
host="0.0.0.0"
api = Flask(import_name='mongo_api')

@api.route('/mongodb/wine/wine_test/status', methods=['GET']) #renvoie 1 si l’API fonctionne
def api_in_use():
    return  make_response(jsonify({'it works!': '1'}), 200)

@api.route('/mongodb/wine/wine_test/databases', methods=['GET']) #renvoie le nom des databases présentes dans mongodb
def database_name():
    client = MongoClient(
        host='mongodb',
        port=27017,
        username='admin_user',
        password='admin_pwd',
        authSource='admin'
    )
    return  make_response(jsonify({"database_names": client.list_database_names()}), 200)

@api.route('/mongodb/wine/wine_test/distinct', methods=['GET']) #renvoie les valeurs uniques de la clé sélectionnée
def distincts():
    client = MongoClient(
        host='mongodb',
        port=27017,
        username='admin_user',
        password='admin_pwd',
        authSource='admin'
    )
    db = client['wine']
    col = db['wine_test']
    key = request.args.get('key')
    return col.find(filter={key:{'$exists': True}}).distinct(key)
#    return  make_response(jsonify({"document": [col.find_one()]}), 200)


if __name__ == '__main__':
    api.run(host="0.0.0.0", port=5000)
