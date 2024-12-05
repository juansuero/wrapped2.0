# fetch_data.py
import pandas as pd
from spotify_auth import sp
from utils import get_output_path

def get_user_data():
    try:
        ranges = ['short_term', 'medium_term', 'long_term']
        all_tracks = []
        
        for time_range in ranges:
            tracks = sp.current_user_top_tracks(limit=50, time_range=time_range)
            for track in tracks['items']:
                track_info = {
                    'name': track['name'],
                    'artist': track['artists'][0]['name'],
                    'album': track['album']['name'],
                    'popularity': track['popularity'],
                    'time_range': time_range
                }
                all_tracks.append(track_info)
        
        df = pd.DataFrame(all_tracks)
        paths = get_output_path()
        df.to_csv(paths['data'], index=False)
        return df
        
    except Exception as e:
        print(f"Error fetching user data: {str(e)}")
        return pd.DataFrame()

if __name__ == "__main__":
    data = get_user_data()
    if not data.empty:
        print(f'Successfully processed {len(data)} tracks')
    else:
        print('Error: No data was fetched')