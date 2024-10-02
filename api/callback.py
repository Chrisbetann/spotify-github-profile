from flask import Flask, Response, jsonify, render_template, redirect, request
from base64 import b64decode
from dotenv import load_dotenv, find_dotenv
import logging

load_dotenv(find_dotenv())

from firebase_admin import credentials
from firebase_admin import firestore
import firebase_admin

import os
import json
from util import spotify

print("Starting Server")

# Firebase setup
firebase_config = os.getenv("FIREBASE")
firebase_dict = json.loads(b64decode(firebase_config))

cred = credentials.Certificate(firebase_dict)
firebase_admin.initialize_app(cred)

db = firestore.client()

# Flask setup
app = Flask(__name__)

# Set up basic logging
logging.basicConfig(filename='app.log', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s: %(message)s')

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def catch_all(path):
    try:
        # Extract code from the request
        code = request.args.get("code")

        if code is None:
            app.logger.warning("No authorization code received in the callback request.")
            return Response("Authorization code missing, please try again.", status=400)

        # Generate Spotify token using received code
        token_info = spotify.generate_token(code)
        access_token = token_info.get("access_token")

        if not access_token:
            app.logger.error("Failed to retrieve access token from Spotify.")
            return Response("Failed to authenticate with Spotify. Please try again.", status=500)

        # Get user profile information from Spotify
        spotify_user = spotify.get_user_profile(access_token)
        user_id = spotify_user.get("id")

        if not user_id:
            app.logger.error("Failed to retrieve user profile from Spotify.")
            return Response("Unable to retrieve user profile. Please try again later.", status=500)

        # Save token information to Firestore
        doc_ref = db.collection("users").document(user_id)
        doc_ref.set(token_info)

        # Render callback template with necessary data
        rendered_data = {
            "uid": user_id,
            "BASE_URL": spotify.BASE_URL,
        }

        return render_template("callback.html.j2", **rendered_data)

    except requests.exceptions.HTTPError as http_err:
        app.logger.error(f"HTTP error occurred: {http_err}")
        return Response("Error during Spotify authentication. Please try again later.", status=500)

    except Exception as err:
        app.logger.error(f"Unexpected error occurred: {err}")
        return Response("An unexpected error occurred. Please contact support.", status=500)

if __name__ == "__main__":
    app.run(debug=True)
