# insights.py
import pandas as pd
from utils import get_output_path

def generate_insights(data):
    if data.empty:
        return {}
        
    insights = {
        'top_artists': {
            'short_term': data[data['time_range'] == 'short_term']['artist'].value_counts().head(5).to_dict(),
            'medium_term': data[data['time_range'] == 'medium_term']['artist'].value_counts().head(5).to_dict(),
            'long_term': data[data['time_range'] == 'long_term']['artist'].value_counts().head(5).to_dict()
        },
        'top_tracks': {
            'short_term': data[data['time_range'] == 'short_term'].nlargest(5, 'popularity')[['name', 'artist']].to_dict('records'),
            'medium_term': data[data['time_range'] == 'medium_term'].nlargest(5, 'popularity')[['name', 'artist']].to_dict('records'),
            'long_term': data[data['time_range'] == 'long_term'].nlargest(5, 'popularity')[['name', 'artist']].to_dict('records')
        }
    }
    return insights