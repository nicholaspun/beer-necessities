import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

class FirebaseClient:
    __INITIALIZED__ = None
    BEER_DB_NAME = 'beer'

    def __init__(self):
        pass

    @staticmethod
    def initialize_with_file(filepath):
        if not FirebaseClient.__INITIALIZED__:
            cred = credentials.Certificate(filepath)
            firebase_admin.initialize_app(cred)
            FirebaseClient.__INITIALIZED__ = True

    @staticmethod
    def get_database(db_name):
        if not FirebaseClient.__INITIALIZED__:
            raise Exception('Firebase Client not initialized!')

        return firestore.client().collection(db_name).get()

    @staticmethod
    def add_to_database(db_name, data):
        if not FirebaseClient.__INITIALIZED__:
            raise Exception('Firebase Client not initialized!')

        firestore.client().collection(db_name).add(data)
