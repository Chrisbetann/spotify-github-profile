import logging
from flask import Flask, redirect, request, Response
import requests
from util.spotify_util import get_auth_url

app = Flask(__name__)

# Set up basic logging
logging.basicConfig(filename='login.log', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s: %(message)s')

@app.route("/login")
def login():
    try:
        # Construct the Spotify authorization URL using the utility function
        auth_url = get_auth_url()
        return redirect(auth_url)

    except requests.exceptions.RequestException as req_err:
        app.logger.error(f"Request error occurred: {req_err}")
        return Response("Failed to initiate Spotify login. Please try again later.", status=500)

    except Exception as err:
        app.logger.error(f"Unexpected error occurred during login: {err}")
        return Response("An unexpected error occurred. Please contact support.", status=500)

if __name__ == "__main__":
    app.run(debug=True)
