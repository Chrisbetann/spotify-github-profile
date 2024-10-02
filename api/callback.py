from flask import Flask, Response, jsonify, render_template, request
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

import logging
from util.spotify_util import generate_token, get_user_profile, save_user_data_to_firestore

print("Starting Server")

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
        token_info = generate_token(code)
        access_token = token_info.get("access_token")

        if not access_token:
            app.logger.error("Failed to retrieve access token from Spotify.")
            return Response("Failed to authenticate with Spotify. Please try again.", status=500)

        # Get user profile information from Spotify
        spotify_user = get_user_profile(access_token)
        user_id = spotify_user.get("id")

        if not user_id:
            app.logger.error("Failed to retrieve user profile from Spotify.")
            return Response("Unable to retrieve user profile. Please try again later.", status=500)

        # Save token information to Firestore
        save_user_data_to_firestore(user_id, token_info)

        # Render callback template with necessary data
        rendered_data = {
            "uid": user_id,
            "BASE_URL": os.getenv("BASE_URL"),
        }

        return render_template("callback.html.j2", **rendered_data)

    except requests.exceptions.RequestException as req_err:
        app.logger.error(f"HTTP error occurred: {req_err}")
        return Response("Error during Spotify authentication. Please try again later.", status=500)

    except Exception as err:
        app.logger.error(f"Unexpected error occurred: {err}")
        return Response("An unexpected error occurred. Please contact support.", status=500)

if __name__ == "__main__":
    app.run(debug=True)
