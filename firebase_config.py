import os
import json
import firebase_admin
from firebase_admin import credentials, firestore, auth

firebase_creds_json = os.environ.get("FIREBASE_CREDENTIALS")

if firebase_creds_json:
    cred_dict = json.loads(firebase_creds_json)
    cred = credentials.Certificate(cred_dict)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    KEY_PATH = os.path.join(BASE_DIR, "serviceAccountKey.json")
    cred = credentials.Certificate(KEY_PATH)

firebase_admin.initialize_app(cred)
db = firestore.client()
auth_client = auth