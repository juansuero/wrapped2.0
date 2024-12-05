# report.py
from fpdf import FPDF
from insights import generate_insights
import pandas as pd
from utils import get_output_path
import os
import sys
from datetime import datetime

def get_output_path():
    # Create output directory
    output_dir = 'spotify_reports'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Generate timestamp with correct datetime usage
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    return {
        'dir': output_dir,
        'data': f'{output_dir}/track_data_{timestamp}.csv',
        'pdf': f'{output_dir}/Spotify_Wrapped_{timestamp}.pdf'
    }

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'Your Spotify Wrapped 2.0', 0, 1, 'C')
        
    def chapter_title(self, title):
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, title, 0, 1, 'L')
        
    def chapter_body(self, body):
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 10, str(body))
        self.ln()


def generate_report():
    try:
        print("Starting report generation...", flush=True)
        paths = get_output_path()
        
        # Check output directory
        print(f"Checking directory: {paths['dir']}", flush=True)
        if not os.path.exists(paths['dir']):
            os.makedirs(paths['dir'])
            print(f"Created directory: {paths['dir']}", flush=True)
            
        # Verify data file
        print(f"Checking data file: {paths['data']}", flush=True)
        if not os.path.exists(paths['data']):
            print(f"ERROR: Data file not found at {paths['data']}", flush=True)
            return
            
        # Load data
        print("Reading data file...", flush=True)
        data = pd.read_csv(paths['data'])
        print(f"Loaded {len(data)} rows", flush=True)
        
        print("Generating insights...")
        insights = generate_insights(data)
        
        print("Creating PDF...")
        pdf = PDF()
        pdf.add_page()
        
        time_ranges = ['short_term', 'medium_term', 'long_term']
        labels = {'short_term': 'Last Month', 'medium_term': 'Last 6 Months', 'long_term': 'All Time'}
        
        for time_range in time_ranges:
            print(f"Processing {time_range}...", flush=True)
            pdf.chapter_title(f"\nTop Artists - {labels[time_range]}")
            for artist, count in insights['top_artists'][time_range].items():
                pdf.chapter_body(f"- {artist}: {count} tracks")
                
            pdf.chapter_title(f"\nTop Tracks - {labels[time_range]}")
            for track in insights['top_tracks'][time_range]:
                pdf.chapter_body(f"- {track['name']} by {track['artist']}")
        
        output_path = paths['pdf']
        print(f"Saving PDF to: {output_path}", flush=True)
        pdf.output(output_path)
        print(f"Report saved successfully to: {output_path}", flush=True)
        
    except Exception as e:
        print(f"ERROR in report generation: {str(e)}", flush=True)
        import traceback
        print(traceback.format_exc(), flush=True)

if __name__ == "__main__":
    print("Starting main...", flush=True)
    generate_report()
    print("Done.", flush=True)