import streamlit as st
import pandas as pd
import plotly.express as px
import spotipy
import os
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

def clear_session():
    """Clear session state and cached tokens"""
    if 'token_info' in st.session_state:
        del st.session_state.token_info
    if 'data' in st.session_state:
        del st.session_state.data
    # Remove cache file if it exists
    if os.path.exists('.cache'):
        os.remove('.cache')

def validate_spotify_data(data):
    """Validate Spotify data integrity"""
    validation_results = {
        'total_tracks': len(data),
        'unique_tracks': len(data['name'].unique()),
        'unique_artists': len(data['artist'].unique()),
        'time_ranges': sorted(data['time_range'].unique()),
        'popularity_range': f"{data['popularity'].min()}-{data['popularity'].max()}",
        'missing_images': sum(data['album_image'].isnull()),
        'missing_genres': sum(data['genres'] == '')
    }
    return validation_results

def display_debug_info(data, time_range):
    """Display debug information for data verification"""
    with st.expander("⚙️ Data Verification"):
        validation = validate_spotify_data(data)
        
        st.write("### Data Overview")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Tracks", validation['total_tracks'])
            st.metric("Unique Tracks", validation['unique_tracks'])
        
        with col2:
            st.metric("Unique Artists", validation['unique_artists'])
            st.metric("Time Periods", len(validation['time_ranges']))
        
        with col3:
            st.metric("Popularity Range", validation['popularity_range'])
            st.metric("Missing Images", validation['missing_images'])
        
        # Sample data display
        st.write("### Sample Data Check")
        st.dataframe(data[data['time_range'] == time_range].head())
        
        # Time range distribution
        st.write("### Tracks per Time Range")
        time_dist = data['time_range'].value_counts()
        st.write(time_dist)

def display_visualizations(data):
    """Display user's listening data with validation"""
    time_range = st.sidebar.selectbox(
        "Select Time Range",
        ["short_term", "medium_term", "long_term"],
        format_func=lambda x: {
            'short_term': 'Last Month',
            'medium_term': 'Last 6 Months',
            'long_term': 'All Time'
        }[x]
    )
    
    # Add debug/verification information
    display_debug_info(data, time_range)
    
    period_data = data[data['time_range'] == time_range]
    
    # Rest of your visualization code...
    
def initialize_session_state():
    """Initialize Streamlit session state variables"""
    if 'token_info' not in st.session_state:
        st.session_state.token_info = None
    if 'data' not in st.session_state:
        st.session_state.data = None

def fetch_user_data(sp):
    """
    Fetch user's listening data from Spotify API
    Returns DataFrame with track info, play counts, and genres
    """
    data = []
    ranges = ['short_term', 'medium_term', 'long_term']
    
    for time_range in ranges:
        # Get top 50 tracks for each time period
        top_tracks = sp.current_user_top_tracks(limit=50, time_range=time_range)
        
        # Process each track
        for position, track in enumerate(top_tracks['items'], 1):
            # Get artist details for genre information
            artist_id = track['artists'][0]['id']
            artist_info = sp.artist(artist_id)
            
            track_info = {
                'name': track['name'],
                'artist': track['artists'][0]['name'],
                'album': track['album']['name'],
                'popularity': track['popularity'],
                'play_rank': position,
                'time_range': time_range,
                'genres': ','.join(artist_info['genres']) if artist_info['genres'] else '',
                'duration_ms': track['duration_ms'],
                'album_image': track['album']['images'][0]['url'] if track['album']['images'] else None,
                'artist_image': artist_info['images'][0]['url'] if artist_info['images'] else None
            }
            data.append(track_info)
    
    return pd.DataFrame(data)

def display_visualizations(data):
    """Display user's listening data with tabs"""
    time_range = st.sidebar.selectbox(
        "Select Time Range",
        ["short_term", "medium_term", "long_term"],
        format_func=lambda x: {
            'short_term': 'Last Month',
            'medium_term': 'Last 6 Months',
            'long_term': 'All Time'
        }[x]
    )
    
    period_data = data[data['time_range'] == time_range]
    
    tabs = st.tabs([
        "Top Artists", 
        "Top Tracks", 
        "Popular Tracks", 
        "Genres",
    ])
# Tab 1: Top Artists
    with tabs[0]:
        st.header("Your Top 50 Artists")
        # Get unique artists and their total track count
        artist_counts = period_data.groupby('artist').size().sort_values(ascending=False).head(50)
        
        for i, (artist, count) in enumerate(artist_counts.items(), 1):
            artist_data = period_data[period_data['artist'] == artist].iloc[0]
            col1, col2 = st.columns([1, 4])
            with col1:
                if artist_data['artist_image']:
                    st.image(artist_data['artist_image'], width=60)
            with col2:
                st.write(f"{i}. **{artist}** - {count} tracks in your top songs")
    # Tab 2: Top Tracks
    with tabs[1]:
        st.header("Your Most Played Tracks")
        most_played = period_data.nsmallest(50, 'play_rank')
        for i, row in most_played.iterrows():
            col1, col2 = st.columns([1, 4])
            with col1:
                if row['album_image']:
                    st.image(row['album_image'], width=50)
            with col2:
                st.write(f"{i+1}. **{row['name']}** by {row['artist']}")
    
    # Tab 3: Popular Tracks
    with tabs[2]:
        st.header("Your Top 50 Tracks by Spotify Popularity")
        most_popular = period_data.nlargest(50, 'popularity')
        for i, row in most_popular.iterrows():
            col1, col2 = st.columns([1, 4])
            with col1:
                if row['album_image']:
                    st.image(row['album_image'], width=50)
            with col2:
                st.write(f"{i+1}. **{row['name']}** by {row['artist']} - Popularity: {row['popularity']}")

    # Tab 4: Genres
    with tabs[3]:
        st.header("Your Music by Genre")
        genres = [g for genres in period_data['genres'].str.split(',') for g in genres if g]
        genre_counts = pd.Series(genres).value_counts()
        
        fig_genres = px.pie(
            values=genre_counts.values,
            names=genre_counts.index,
            title="Genre Distribution"
        )
        st.plotly_chart(fig_genres)
        
        for genre in genre_counts.index:
            genre_tracks = period_data[period_data['genres'].str.contains(genre, na=False)]
            with st.expander(f"{genre} ({len(genre_tracks)} tracks)"):
                for _, track in genre_tracks.iterrows():
                    col1, col2 = st.columns([1, 4])
                    with col1:
                        if track['album_image']:
                            st.image(track['album_image'], width=50)
                    with col2:
                        st.write(f"**{track['name']}** by {track['artist']}")

# Update main() function in app.py

def main():
    """Main application flow"""
    st.title("Your Personal Spotify Stats")
    initialize_session_state()
    
    # Add logout button in sidebar
    if st.session_state.token_info:
        if st.sidebar.button("Logout"):
            clear_session()
            st.rerun()
    
    if not st.session_state.token_info:
        sp_oauth = create_spotify_oauth()
        auth_url = sp_oauth.get_authorize_url()
        
        # Display login button
        st.markdown(
            f"""
            <div style="display: flex; justify-content: center; margin: 50px 0;">
                <a href="{auth_url}" target="_self" 
                   style="text-decoration: none; 
                          background-color: #1DB954; 
                          color: white; 
                          padding: 15px 30px; 
                          border-radius: 25px; 
                          font-weight: bold;
                          box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                    Login with Spotify
                </a>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Handle OAuth callback
        try:
            if 'code' in st.query_params:
                code = st.query_params['code']
                try:
                    # Try to get cached token first
                    token_info = sp_oauth.get_cached_token()
                    if not token_info:
                        # If no cached token, get new one
                        token_info = sp_oauth.get_access_token(code)
                    
                    if token_info:
                        st.session_state.token_info = token_info
                        st.rerun()
                    else:
                        raise Exception("Failed to get token")
                        
                except Exception as e:
                    st.error("Authentication failed - please try logging in again")
                    clear_session()
                    st.rerun()
        except Exception as e:
            st.error(f"Authentication error: {str(e)}")
            clear_session()
            st.rerun()
    
    else:
        try:
            sp = spotipy.Spotify(auth=st.session_state.token_info['access_token'])
            
            # Test the connection
            try:
                sp.current_user()
            except:
                st.error("Session expired - please login again")
                clear_session()
                st.rerun()
            
            if st.button("Fetch My Data") or st.session_state.data is None:
                with st.spinner("Fetching your Spotify data..."):
                    st.session_state.data = fetch_user_data(sp)
                st.success("Data fetched successfully!")
            
            if st.session_state.data is not None:
                display_visualizations(st.session_state.data)
                
        except Exception as e:
            st.error(f"Error accessing Spotify: {str(e)}")
            clear_session()
            st.rerun()

if __name__ == "__main__":
    main()