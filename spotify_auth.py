# spotify_auth.py
import streamlit as st
from spotipy.oauth2 import SpotifyOAuth

# Load credentials from Streamlit secrets
SPOTIPY_CLIENT_ID = st.secrets["SPOTIFY_CLIENT_ID"]
SPOTIPY_CLIENT_SECRET = st.secrets["SPOTIFY_CLIENT_SECRET"]
SPOTIPY_REDIRECT_URI = st.secrets["REDIRECT_URI"]
SCOPE = "user-top-read user-read-recently-played user-library-read"
CACHE = '.spotipyoauthcache'

def create_spotify_oauth():
    """Create SpotifyOAuth instance with credentials"""
    try:
        return SpotifyOAuth(
            client_id=SPOTIPY_CLIENT_ID,
            client_secret=SPOTIPY_CLIENT_SECRET,
            redirect_uri=SPOTIPY_REDIRECT_URI,
            scope=SCOPE,
            cache_path=CACHE,
            show_dialog=True
        )
    except Exception as e:
        st.error(f"Failed to create Spotify OAuth: {str(e)}")
        return None

def get_token():
    """Get cached token or new one"""
    sp_oauth = create_spotify_oauth()
    token_info = sp_oauth.get_cached_token()
    
    if not token_info:
        auth_url = sp_oauth.get_authorize_url()
        st.markdown(f"[Login to Spotify]({auth_url})")
        
        # Handle callback with authorization code
        if 'code' in st.query_params:
            code = st.query_params['code']
            try:
                token_info = sp_oauth.get_access_token(code, as_dict=True)
            except Exception as e:
                st.error(f"Error getting access token: {str(e)}")
                return None
                
    return token_info