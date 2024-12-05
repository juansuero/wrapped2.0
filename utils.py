# utils.py
import os
from datetime import datetime

def get_output_path():
    output_dir = 'spotify_reports'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    return {
        'dir': output_dir,
        'data': f'{output_dir}/track_data_{timestamp}.csv',
        'pdf': f'{output_dir}/Spotify_Wrapped_{timestamp}.pdf'
    }