# spotify_auth.py
import os
from spotipy.oauth2 import SpotifyOAuth

# Get deployment URL from environment or use localhost
REDIRECT_URI = os.getenv('REDIRECT_URI', 'http://localhost:8501/')
CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID', '45c01f01bb3447b2bb2c99902d9461c5')
CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET', '2ce37e31b5b6411885dd4d8b4d7f9478')
SCOPE = 'user-top-read user-read-recently-played user-library-read'

def create_spotify_oauth():
    """Create SpotifyOAuth instance for authentication"""
    return SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope=SCOPE,
        cache_path=False  # Disable caching for cloud deployment
    )

def get_token():
    """Get cached token or create new one"""
    sp_oauth = create_spotify_oauth()
    token_info = sp_oauth.get_cached_token()
    if not token_info:
        auth_url = sp_oauth.get_authorize_url()
        return None
    return token_info
