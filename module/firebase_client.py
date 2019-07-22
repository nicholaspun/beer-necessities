import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

class FirebaseClient:
    __INITIALIZED__ = None
    
    def __init__(self):
        pass

    @staticmethod
    def initialize_with_file(filepath):
        if not __INITIALIZED__:
            cred = credentials.Certificate(filepath)
            firebase_admin.initialize_app(cred)
            __INITIALIZED__ = True

    @staticmethod
    def get_database(db_name):
        if not __INITIALIZED__:
            raise Exception('Firebase Client not initialized!')

        return firestore.client().collection(db_name).get()
