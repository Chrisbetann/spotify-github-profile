import requests
import json
import firebase_admin
from firebase_admin import credentials, firestore
from base64 import b64decode
import os
import logging

# Set up logging for utility functions
logging.basicConfig(filename='app.log', level=logging.DEBUG, 
                    format='%(asctime)s %(levelname)s: %(message)s')

# Load Firebase setup
firebase_config = os.getenv("FIREBASE")
firebase_dict = json.loads(b64decode(firebase_config))

cred = credentials.Certificate(firebase_dict)
firebase_admin.initialize_app(cred)

db = firestore.client()

# Spotify Utility Functions
def generate_token(code):
    try:
        response = requests.post('https://accounts.spotify.com/api/token', data={
            # Replace with the appropriate data for token exchange
            'client_id': os.getenv("SPOTIFY_CLIENT_ID"),
            'client_secret': os.getenv("SPOTIFY_SECRET_ID"),
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': os.getenv("REDIRECT_URI")
        })
        response.raise_for_status()
        logging.info("Successfully generated Spotify token.")
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to generate Spotify token: {e}")
        raise

def get_user_profile(access_token):
    try:
        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        response = requests.get('https://api.spotify.com/v1/me', headers=headers)
        response.raise_for_status()
        logging.info("Successfully retrieved user profile.")
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to retrieve Spotify user profile: {e}")
        raise

def save_user_data_to_firestore(user_id, token_info):
    try:
        doc_ref = db.collection("users").document(user_id)
        doc_ref.set(token_info)
        logging.info(f"User data for {user_id} successfully saved to Firestore.")
    except Exception as e:
        logging.error(f"Failed to save user data to Firestore: {e}")
        raise
