import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate('./firebase.json')

firebase_admin.initialize_app(cred)
db = firestore.client()

doc = db.collection('unstop-assessment').document('backend')

def getState():
    return doc.get().to_dict()['current_state']

def getInitialState():
    return doc.get().to_dict()['initial_state']

def setState(state):
    doc.update({"current_state": state})


def resetInitialState():
    doc.update({"initial_state": [ 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 3 ] })
    doc.update({"current_state": [ 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 3 ] })


resetInitialState()