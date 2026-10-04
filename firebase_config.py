import os
import firebase_admin
from firebase_admin import credentials, firestore, auth

# Base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KEY_PATH = os.path.join(BASE_DIR, "serviceAccountKey.json")

# Firebase initialize
cred = credentials.Certificate(KEY_PATH)
firebase_admin.initialize_app(cred)

# Firestore client
db = firestore.client()

# Auth client
auth_client = auth