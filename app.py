from flask import Flask
from flask_cors import CORS
import json
import os
import sys

DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(DIR, 'module'))

from firebase_client import FirebaseClient
from beer import BeerCollection

app = Flask(__name__)
port = int(os.environ.get('PORT', 5000))
CORS(app)

# TODO: Had too much trouble trying to initialize the client
# without using the file .... hence this.
FIREBASE_INITIALIZATION = {
  "type": "{}".format(os.environ['FIREBASE_SECRETS_TYPE']),
  "project_id": "{}".format(os.environ['FIREBASE_SECRETS_PROJECT_ID']),
  "private_key_id": "{}".format(os.environ['FIREBASE_SECRETS_PRIVATE_KEY_ID']),
  "private_key": "{}".format(os.environ['FIREBASE_SECRETS_PRIVATE_KEY']),
  "client_email": "{}".format(os.environ['FIREBASE_SECRETS_CLIENT_EMAIL']),
  "client_id": "{}".format(os.environ['FIREBASE_SECRETS_CLIENT_ID']),
  "auth_uri": "{}".format(os.environ['FIREBASE_SECRETS_AUTH_URI']),
  "token_uri": "{}".format(os.environ['FIREBASE_SECRETS_TOKEN_URI']),
  "auth_provider_x509_cert_url": "{}".format(os.environ['FIREBASE_SECRETS_AUTH_PROVIDER']),
  "client_x509_cert_url": "{}".format(os.environ['FIREBASE_SECRETS_CLIENT_X509_CERT_URL'])
}

SECRETS_FILE_NAME = 'secrets.json'
with open(SECRETS_FILE_NAME, 'w') as secretsfile:
    secretsfile.write(json.dumps(FIREBASE_INITIALIZATION))

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

if __name__ == '__main__':
    app.run(debug = True, host = '0.0.0.0', port = port)
