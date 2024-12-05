# spotify_auth.py
import spotipy
from spotipy.oauth2 import SpotifyOAuth

CLIENT_ID = '45c01f01bb3447b2bb2c99902d9461c5'
CLIENT_SECRET = '2ce37e31b5b6411885dd4d8b4d7f9478'
REDIRECT_URI = 'http://localhost:8888/callback'
SCOPE = ('user-library-read user-top-read user-read-recently-played '
         'user-read-playback-state playlist-read-private')

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=SCOPE,
    cache_path='.spotifycache'))
