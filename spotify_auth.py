# spotify_auth.py
import os
import streamlit as st
from spotipy.oauth2 import SpotifyOAuth

# For debugging
DEBUG = True

def log_debug(msg):
    if DEBUG:
        st.write(f"Debug: {msg}")

# Get credentials from environment only
REDIRECT_URI = os.getenv('REDIRECT_URI')
CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')

if not all([REDIRECT_URI, CLIENT_ID, CLIENT_SECRET]):
    st.error("Missing Spotify credentials. Please set environment variables.")
    st.stop()

SCOPE = 'user-top-read user-read-recently-played user-library-read'

def create_spotify_oauth():
    """Create SpotifyOAuth instance for authentication"""
    try:
        # Add debug logging
        log_debug(f"Creating OAuth with URI: {REDIRECT_URI}")
        log_debug(f"Client ID exists: {'Yes' if CLIENT_ID else 'No'}")
        log_debug(f"Client Secret exists: {'Yes' if CLIENT_SECRET else 'No'}")
        
        # Ensure REDIRECT_URI ends with slash
        clean_uri = REDIRECT_URI.rstrip('/') + '/'
        
        oauth = SpotifyOAuth(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            redirect_uri=clean_uri,
            scope=SCOPE,
            cache_path=False,
            show_dialog=True,
            requests_session=False,  # Disable session handling for better compatibility
            open_browser=False
        )
        
        # Test auth URL generation
        auth_url = oauth.get_authorize_url()
        log_debug(f"Generated auth URL: {auth_url}")
        
        return oauth
    except Exception as e:
        log_debug(f"OAuth creation failed: {str(e)}")
        log_debug(f"Full error details: {repr(e)}")
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