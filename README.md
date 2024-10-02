# spotify-github-profile

Create Spotify now playing card on your github profile

Running on Vercel serverless function, store data in Firebase (store only access_token, refresh_token, token_expired_timestamp)

## Annoucements

## Enhancements and Updates by Christopher Betancourt
## This project has undergone several updates to enhance its functionality, maintainability, and performance:

1. Enhanced Error Handling and Logging
Implemented comprehensive error handling across both callback.py and login.py files.
Added logging to capture and log various types of errors for easier debugging and enhanced visibility.
Created custom error responses to provide meaningful messages to users when errors occur.

2. Spotify Utility Refactoring
Refactored Spotify-specific operations (such as generating tokens, getting user profiles, and saving data to Firebase) into reusable utility functions.
These functions are located in util/spotify_util.py and ensure that the code is modular and easily maintainable.
The login.py and callback.py files now import and use these utility functions, making the main logic cleaner and easier to understand.

3. Performance Tuning with Gunicorn
Optimized the application for production by running it with Gunicorn, a Python WSGI HTTP Server, to handle multiple requests concurrently.
Added a Gunicorn configuration file (gunicorn.conf.py) to manage worker and thread settings to improve scalability.
Dockerfile now runs the Flask app using Gunicorn for improved performance in production environments.

4. Docker Healthcheck Integration
Added a healthcheck route (/healthcheck) to ensure the service is running properly.
Integrated a Docker HEALTHCHECK to verify the container's health and improve monitoring and reliability.

5. Dynamic SVG for Enhanced Profile Display
Developed a dynamic SVG that updates automatically to reflect the currently playing song on Spotify, offering a more visually engaging display on GitHub profiles.
SVG components like album art, track name, and artist are dynamically rendered and updated periodically, making the profile interactive and attractive.
Future enhancements to the SVG include animated song features based on Spotify’s audio data, such as tempo and energy.

7. Environment Configuration Updates
Introduced .env support to store sensitive information (such as API keys and Firebase credentials) securely.
Added support for python-dotenv to load environment variables, making local and deployment configurations easier.

**2024-06-21**

Vercel change the package the free tier is not enough for our usage. I moved service to self-host at Digital Ocean.

Please replace your old endpoint `https://spotify-github-profile.vercel.app` to `https://spotify-github-profile.kittinanx.com`

## Table of Contents  
[Connect And Grant Permission](#connect-and-grant-permission)  
[Example](#example)  
[Running for development locally](#running-for-development-locally)  
[Setting up Vercel](#setting-up-vercel)  
[Setting up Firebase](#setting-up-firebase)  
[Setting up Spotify dev](#setting-up-spotify-dev)  
[Running locally](#running-locally)  
[How to Contribute](#how-to-contribute)  
[Known Bugs](#known-bugs)  
[Features in Progress](#features-in-progress)  
[Credit](#credit)  

## Connect And Grant Permission

- Click `Connect with Spotify` button below to grant permission

[<img src="/img/btn-spotify.png">](https://spotify-github-profile.kittinanx.com/api/login)

## Example

- Default theme

![spotify-github-profile](/img/default.svg)

- Compact theme

![spotify-github-profile](/img/compact.svg)

- Natemoo-re theme

![spotify-github-profile](/img/natemoo-re.svg)

- Novatorem theme

![spotify-github-profile](/img/novatorem.svg)

- Karaoke theme

![spotify-github-profile](/img/karaoke.svg)



## Running for development locally

To develop locally, you need:

- A fork of this project as your repository
- A Vercel project connected with the forked repository
- A Firebase project with Cloud Firestore setup
- A Spotify developer account

### Setting up Vercel

- [Create a new Vercel project by importing](https://vercel.com/import) the forked project on GitHub

### Setting up Firebase

- Create [a new Firebase project](https://console.firebase.google.com/u/0/)
- Create a new Cloud Firestore in the project
- Download configuration JSON file from _Project settings_ > _Service accounts_ > _Generate new private key_
- Convert private key content as BASE64
  - You can use Encode/Decode extension in VSCode to do so
  - This key will be used in step explained below

### Setting up Spotify dev

- Login to [developer.spotify.com](https://developer.spotify.com/dashboard/applications)
- Create a new project
- Edit settings to add _Redirect URIs_
  - add `http://localhost:3000/api/callback`

### Running locally

- Install [Vercel command line](https://vercel.com/download) with `npm i -g vercel`
- Create `.env` file at the root of the project and paste your keys in `SPOTIFY_CLIENT_ID`, `SPOTIFY_SECRET_ID`, and `FIREBASE`

```sh
BASE_URL='http://localhost:3000/api'
SPOTIFY_CLIENT_ID='____'
SPOTIFY_SECRET_ID='____'
FIREBASE='__BASE64_FIREBASE_JSON_FILE__'
```

- Run `vercel dev`

```sh
$ vercel dev
Vercel CLI 20.1.2 dev (beta) — https://vercel.com/feedback
> Ready! Available at http://localhost:3000
```

- Now try to access http://localhost:3000/api/login

## How to Contribute

- Develop locally and submit a pull request!
- Submit newly encountered bugs to the [Issues](https://github.com/kittinan/spotify-github-profile/issues) page
- Submit feature suggestions to the [Issues](https://github.com/kittinan/spotify-github-profile/issues) page, with the label [Feature Suggestion]

## Known Bugs

[404/500 Error when playing local files](https://github.com/kittinan/spotify-github-profile/issues/19)

## Other Platforms
- [Apple Music GitHub Profile](https://github.com/rayriffy/apple-music-github-profile)

## Credit

Inspired by https://github.com/natemoo-re
