# app.py
from flask import Flask, session, redirect, request, render_template
from spotipy.oauth2 import SpotifyOAuth
import spotipy
import os
from flask import jsonify
from collections import Counter
from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)  # For session management



# Configuration
# Configuration
CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
REDIRECT_URI = os.getenv('REDIRECT_URI', 'https://spotify-stats-rprj.onrender.com/callback')
SCOPE = os.getenv('SPOTIFY_SCOPE', "user-top-read user-read-recently-played user-library-read")

# OAuth setup with full callback URL
sp_oauth = SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=SCOPE
)
if not all([CLIENT_ID, CLIENT_SECRET, REDIRECT_URI]):
    raise ValueError("Missing required environment variables. Check .env file.")

# OAuth setup
sp_oauth = SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=SCOPE
)

@app.route('/')
def index():
    if 'token_info' not in session:
        return render_template('login.html')
    return render_template('dashboard.html')

@app.route('/login')
def login():
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/callback')
def callback():
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session['token_info'] = token_info
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    if 'token_info' not in session:
        return redirect('/')
        
    sp = spotipy.Spotify(auth=session['token_info']['access_token'])
    data = fetch_user_data(sp)
    return render_template('dashboard.html', data=data)

def fetch_user_data(sp):
    # Your existing data fetching logic here
    pass
# Add to app.py after existing routes

@app.route('/get_data')
def get_data():
    if 'token_info' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
        
    try:
        time_range = request.args.get('time_range', 'medium_term')
        sp = spotipy.Spotify(auth=session['token_info']['access_token'])
        
        # Get top 50 artists with images and genres
        artists = sp.current_user_top_artists(limit=50, time_range=time_range)
        top_artists = [{
            'name': artist['name'],
            'image': artist['images'][0]['url'] if artist['images'] else None,
            'rank': i + 1,
            'genres': artist['genres']
        } for i, artist in enumerate(artists['items'])]
        
        # Get top 50 tracks
        tracks = sp.current_user_top_tracks(limit=50, time_range=time_range)
        top_tracks = [{
            'name': track['name'],
            'artist': track['artists'][0]['name'],
            'image': track['album']['images'][0]['url'] if track['album']['images'] else None,
            'rank': i + 1
        } for i, track in enumerate(tracks['items'])]
        
        # Get popular tracks
        popular_tracks = [{
            'name': track['name'],
            'artist': track['artists'][0]['name'],
            'image': track['album']['images'][0]['url'] if track['album']['images'] else None,
            'popularity': track['popularity'],
            'rank': i + 1
        } for i, track in sorted(enumerate(tracks['items']), 
                               key=lambda x: x[1]['popularity'], 
                               reverse=True)]
        
        # Genre analysis
        all_genres = []
        for artist in artists['items']:
            all_genres.extend(artist['genres'])
        
        genre_counts = Counter(all_genres)
        genres = [{
            'name': genre,
            'count': count,
            'artists': [
                artist['name'] for artist in top_artists 
                if genre in artist['genres']
            ]
        } for genre, count in genre_counts.most_common()]
        
        return jsonify({
            'top_artists': top_artists,
            'top_tracks': top_tracks,
            'popular_tracks': popular_tracks,
            'genres': genres
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500



if __name__ == '__main__':
    app.run(debug=True)