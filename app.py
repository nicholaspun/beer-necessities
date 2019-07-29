from flask import Flask
import json
import os
import sys

DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(DIR, 'module'))

from firebase_client import FirebaseClient
from beer import BeerCollection

app = Flask(__name__)

# TODO: Had too much trouble trying to initialize the client
# without using the file .... hence this.
SECRETS_FILE_NAME = 'secrets.json'
with open(SECRETS_FILE_NAME, 'w') as secretsfile:
    secretsfile.write(os.environ['FIREBASE_SECRETS_FILE'])

FirebaseClient.initialize_with_file(os.path.join(DIR, SECRETS_FILE_NAME))
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
