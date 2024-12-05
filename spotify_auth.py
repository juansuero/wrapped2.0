# spotify_auth.py
import os
import streamlit as st
from spotipy.oauth2 import SpotifyOAuth

# For debugging
DEBUG = True

def log_debug(msg):
    if DEBUG:
        st.write(f"Debug: {msg}")

# Get deployment URL from Streamlit secrets if available
if st.secrets and hasattr(st.secrets, "REDIRECT_URI"):
    REDIRECT_URI = st.secrets.REDIRECT_URI
    CLIENT_ID = st.secrets.SPOTIFY_CLIENT_ID
    CLIENT_SECRET = st.secrets.SPOTIFY_CLIENT_SECRET
else:
    REDIRECT_URI = os.getenv('REDIRECT_URI', 'http://localhost:8501/')
    CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID', '45c01f01bb3447b2bb2c99902d9461c5')
    CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET', '2ce37e31b5b6411885dd4d8b4d7f9478')

SCOPE = 'user-top-read user-read-recently-played user-library-read'

def create_spotify_oauth():
    """Create SpotifyOAuth instance for authentication"""
    try:
        oauth = SpotifyOAuth(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            redirect_uri=REDIRECT_URI,
            scope=SCOPE,
            cache_path=False,
            show_dialog=True  # Force display of auth dialog
        )
        if DEBUG:
            log_debug(f"OAuth created with redirect URI: {REDIRECT_URI}")
        return oauth
    except Exception as e:
        log_debug(f"OAuth creation failed: {str(e)}")
        raise

def get_token():
    """Get cached token or create new one"""
    try:
        sp_oauth = create_spotify_oauth()
        token_info = sp_oauth.get_cached_token()
        if DEBUG:
            log_debug(f"Token info retrieved: {'Yes' if token_info else 'No'}")
        if not token_info:
            auth_url = sp_oauth.get_authorize_url()
            log_debug(f"Auth URL generated: {auth_url}")
            return None
        return token_info
    except Exception as e:
        log_debug(f"Token retrieval failed: {str(e)}")
        return None