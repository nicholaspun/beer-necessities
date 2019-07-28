from flask import Flask
import json
import os
import sys

DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(DIR, 'module'))

from firebase_client import FirebaseClient
from beer import BeerCollection

app = Flask(__name__)

FirebaseClient.initialize_with_file(os.path.join(DIR, 'secrets', 'secrets.json'))
BEER_COLLECTION = BeerCollection.from_firebase_doc(FirebaseClient.get_database(FirebaseClient.BEER_DB_NAME))

@app.route('/')
def client_startup():
    return 'Ok'

@app.route('/beers')
def get_beers():
    return json.dumps(BEER_COLLECTION.get_basic_details())

@app.route('/beers/<beer_id>')
def get_beer_details(beer):
    return json.dumps(BEER_COLLECTION.get_full_details(beer_id))

@app.route('/search/<param>')
def get_beer_keys_from_search(param):
    return 'keys for beers based on a search parameter'