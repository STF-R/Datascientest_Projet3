#importer la classe MongoClient depuis la librairie pymongo
from pymongo import MongoClient
import os
import json
from collections import Counter
import time

time.sleep(8)

## instancier la classe MongoClient
client = MongoClient(
    host='mongodb', ##'127.0.0.1',
    port=27017,
    username='admin_user', ##get_my_username(),
    password='admin_pwd', ##get_my_password(),
    authSource='admin'
)

##Créer la bdd wine et assigner l'accès à cette base de données dans un objet nommé db.
db = client['wine']
##créer la collection wine_test et assigner l'accès à cette collection dans un objet nommé col.
col = db['wine_test']
##peupler la collection à partir du fichier winemag-data-130k-v2.json
with open('./winemag-data-130k-v2.json') as f:
    file_data = json.load(f)
# for pymongo >= 3.0 => use insert_many() for inserting many documents
col.insert_many(file_data)
client.close()

## nous pouvons lister toutes les bases de données disponibles dans MongoDB
print(client.list_database_names())

# récupération de toutes les observations
data = list(col.find())
# comptage du nombre de champs par document
fields_count = list(map(lambda x: len(x), data))
# calcul de la distribution du nombre de champs par document
counter = Counter(fields_count)
print(counter)
