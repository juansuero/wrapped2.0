import os
import streamlit as st
from spotipy.oauth2 import SpotifyOAuth

DEBUG = True

def log_debug(msg):
    """Log debug messages if debugging is enabled."""
    if DEBUG:
        st.write(f"Debug: {msg}")

# Load credentials from Streamlit Secrets (for production) or environment variables (local dev)
try:
    REDIRECT_URI = st.secrets["REDIRECT_URI"]
    CLIENT_ID = st.secrets["SPOTIFY_CLIENT_ID"]
    CLIENT_SECRET = st.secrets["SPOTIFY_CLIENT_SECRET"]
except:
    REDIRECT_URI = os.getenv("REDIRECT_URI")
    CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
    CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

# Validate credentials
if not all([REDIRECT_URI, CLIENT_ID, CLIENT_SECRET]):
    st.error("Missing Spotify credentials. Please set them in secrets or environment variables.")
    st.stop()

# Scopes required by the app
SCOPE = "user-top-read user-read-recently-played user-library-read"

def create_spotify_oauth():
    """Create and return a SpotifyOAuth instance."""
    try:
        log_debug(f"Creating SpotifyOAuth with Redirect URI: {REDIRECT_URI}")
        oauth = SpotifyOAuth(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            redirect_uri=REDIRECT_URI,
            scope=SCOPE,
            cache_path=".cache",  # Cache tokens for reuse
            show_dialog=True,     # Show auth dialog for every login
        )
        return oauth
    except Exception as e:
        log_debug(f"Error creating SpotifyOAuth: {e}")
        st.error("Failed to initialize Spotify authentication.")
        st.stop()

def get_token():
    """Get a cached token or generate a new one through the authentication process."""
    try:
        sp_oauth = create_spotify_oauth()
        token_info = sp_oauth.get_cached_token()
        
        # If no token is cached, generate an auth URL
        if not token_info:
            auth_url = sp_oauth.get_authorize_url()
            st.write(f"[Log in with Spotify]({auth_url})")
            st.stop()
        
        return token_info
    except Exception as e:
        log_debug(f"Error retrieving token: {e}")
        st.error("Spotify authentication failed. Please try again.")
        st.stop()

def display_user_data(token_info):
    """Fetch and display user data using the access token."""
    import spotipy

    try:
        # Create a Spotipy client
        spotify = spotipy.Spotify(auth=token_info["access_token"])
        st.success("Successfully authenticated with Spotify!")
        
        # Fetch and display top artists
        st.subheader("Your Top Artists")
        top_artists = spotify.current_user_top_artists(limit=5)
        for idx, artist in enumerate(top_artists["items"], start=1):
            st.write(f"{idx}. {artist['name']}")
        
        # Fetch and display recently played tracks
        st.subheader("Recently Played Tracks")
        recently_played = spotify.current_user_recently_played(limit=5)
        for idx, item in enumerate(recently_played["items"], start=1):
            track = item["track"]
            st.write(f"{idx}. {track['name']} by {track['artists'][0]['name']}")
    except Exception as e:
        log_debug(f"Error fetching user data: {e}")
        st.error("Failed to fetch Spotify user data.")

# Main logic
st.title("Spotify Login and Data Fetcher")
token_info = get_token()  # Authenticate and get token
if token_info:
    display_user_data(token_info)
