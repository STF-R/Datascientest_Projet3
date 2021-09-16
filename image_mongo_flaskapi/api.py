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

@api.route('/mongodb/status', methods=['GET']) #renvoie 1 si l’API fonctionne
def api_in_use():
    return  make_response(jsonify({'it works!': '1'}), 200)

@api.route('/mongodb/databases', methods=['GET']) #renvoie le nom des databases présentes dans mongodb
def database_name():
    client = MongoClient(
        host='mongodb',
        port=27017,
        username='admin_user',
        password='admin_pwd',
        authSource='admin'
    )
    return  make_response(jsonify({"database_names": client.list_database_names()}), 200)

@api.route('/mongodb/wine/collection', methods=['GET']) #renvoie le nom des collections de la base wine
def collection():
    client = MongoClient(
        host='mongodb',
        port=27017,
        username='data_user',
        password='data_pwd',
        authSource='wine'
    )
    db = client['wine']
    col = db['wine_test']
    return  make_response(jsonify({"collection_names": db.list_collection_names()}), 200)

@api.route('/mongodb/wine/wine_test/find_one', methods=['GET']) #renvoie un document de la collection wine_test
def find_one():
    client = MongoClient(
        host='mongodb',
        port=27017,
        username='data_user',
        password='data_pwd',
        authSource='wine'
    )
    db = client['wine']
    col = db['wine_test']
    return  make_response(jsonify({"document": str(col.find_one())}), 200)

@api.route('/mongodb/wine/wine_test/distinct', methods=['GET']) #renvoie les valeurs uniques de la clé sélectionnée
def distinct():
    client = MongoClient(
        host='mongodb',
        port=27017,
        username='data_user',
        password='data_pwd',
        authSource='wine'
    )
    db = client['wine']
    col = db['wine_test']
    key = request.args.get('key')
    return make_response(jsonify({key: str(col.find(filter={key:{'$exists': True}}).distinct(key))}),200)

@api.route('/mongodb/wine/wine_test/filter', methods=['GET']) #renvoie les documents correspondants aux critères sélectionnés
def filter():
    client = MongoClient(
        host='mongodb',
        port=27017,
        username='data_user',
        password='data_pwd',
        authSource='wine'
    )
    db = client['wine']
    col = db['wine_test']
    country = request.args.get('country', default = '*', type = str)
    points = request.args.get('points', default = '*', type = str)
#    taster_name = request.args.get('taster_name', default = '*', type = str)
#    price = request.args.get('price', default = '*', type = str)
#    designation = request.args.get('designation', default = '*', type = str)
#    variety = request.args.get('variety', default = '*', type = str)
#    region_1 = request.args.get('region_1', default = '*', type = str)
#    region_2 = request.args.get('region_2', default = '*', type = str)
    province = request.args.get('province', default = '*', type = str)
#    winery = request.args.get('winery', default = {'$exists': True}, type = str)
    results = list(col.find(filter={'country':country,'points':points, 'province':province}))
#    filtered_query = []
    return make_response(jsonify({'query length':len(results)}),200)
#    for result in results:
#        filtered_query.append(str(result))
#    return make_response(jsonify({'filtered_query': str(filtered_query)}),200)


if __name__ == '__main__':
    api.run(host="0.0.0.0", port=5000)
