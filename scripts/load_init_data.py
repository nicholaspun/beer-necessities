import csv
import json
import os
import sys
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(DIR, '..', 'module'))

from firebase_client import FirebaseClient
from beer import Beer

FirebaseClient.initialize_with_file(os.path.join(DIR, '..', 'secrets', 'secrets.json'))

with open(os.path.join(DIR, 'data.csv'), encoding='utf-8-sig') as csvfile:
  data_reader = csv.DictReader(csvfile)
  beers = [ Beer(row) for row in data_reader ]

for beer in beers:
    FirebaseClient.add_to_database(FirebaseClient.BEER_DB_NAME, beer.to_dict())
