from flask import Flask
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import json

DIR = os.path.realpath(__FILE__)
sys.path.append(os.path.join(DIR, '..', 'module'))

from firebase_client import FirebaseClient

app = Flask(__name__)

FirebaseClient.initialize_with_file('secrets.json')
BEER_COLLECTION = BeerCollection.from_firebase_doc(FirebaseClient.get_database('beer'))

@app.route('/')
def client_startup():
    return 'Ok'

@app.route('/beers')
def get_beers():
    return json.dumps(BEER_COLLECTION.get_beer_details())

@app.route('/beers/<beer_id>')
def get_beer_details(beer):
    return json.dumps(BEER_COLLECTION.get_full_details(beer_id))

@app.route('/search/<param>')
def get_beer_keys_from_search(param):
    return 'keys for beers based on a search parameter'
