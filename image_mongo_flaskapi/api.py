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

##fonctions utiles
def results():
    client = MongoClient(
        host='mongodb',
        port=27017,
        username='data_user',
        password='data_pwd',
        authSource='wine'
    )
    db = client['wine']
    col = db['wine_test']
    country = request.args.get('country', default = {'$exists': True}, type = str)
    points = request.args.get('points', default = {'$exists': True}, type = str)
    taster_name = request.args.get('taster_name', default = {'$exists': True}, type = str)
    taster_twitter_handle = request.args.get('taster_twitter_handle', default = {'$exists': True}, type = str)
    price = request.args.get('price', default = {'$exists': True}, type = str)
    designation = request.args.get('designation', default = {'$exists': True}, type = str)
    variety = request.args.get('variety', default = {'$exists': True}, type = str)
    region_1 = request.args.get('region_1', default = {'$exists': True}, type = str)
    region_2 = request.args.get('region_2', default = {'$exists': True}, type = str)
    province = request.args.get('province', default = {'$exists': True}, type = str)
    winery = request.args.get('winery', default = {'$exists': True}, type = str)
    results = list(col.find(filter={'country':country,'points':points, 'taster_name':taster_name, 'taster_twitter_handle':taster_twitter_handle, 'price':price, 'designation':designation, 'variety':variety, 'region_1':region_1, 'region_2':region_2, 'province':province, 'winery':winery}))
    return results

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
        authSource='admin')
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

@api.route('/mongodb/wine/wine_test/filter_len', methods=['GET']) #renvoie les documents correspondants aux critères sélectionnés
def filter_len():
    res = results()
    return make_response(jsonify({'query length':len(res)}),200)

@api.route('/mongodb/wine/wine_test/filter', methods=['GET']) #renvoie les documents correspondants aux critères sélectionnés
def filter():
    res = results()
    return make_response(jsonify({'query':str(res)}),200)

if __name__ == '__main__':
    api.run(host="0.0.0.0", port=5000)
