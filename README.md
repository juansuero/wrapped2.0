# Spotify Stats Viewer

A Flask web application that displays your personalized Spotify listening statistics, including top artists, tracks, and genre analysis.

## Features

- View top 50 artists across different time periods
- Display most played tracks
- Show tracks sorted by popularity
- Analyze genre distribution
- Time range filtering (Last Month, Last 6 Months, All Time)
- Album artwork and artist images display

## Prerequisites

- Python 3.8+
- Spotify Developer Account
- Web browser

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd spotify-stats

2. Create Virtual Environment
python -m venv venv
source venv/bin/activate  # Linux/Mac

3. Install Dependencies
pip install -r requirements.txt

4. Create .env with your Spoitfy Crednetials
SPOTIFY_CLIENT_ID=your_client_id
SPOTIFY_CLIENT_SECRET=your_client_secret
REDIRECT_URI=http://localhost:5000/callback
SPOTIFY_SCOPE="user-top-read user-read-recently-played user-library-read"

Spotify API Setup
1. Go to Spotify Developer Dashboard
2. Create a new application
3. Add http://localhost:5000/callback to Redirect URIs
4. Copy Client ID and Client Secret to your .env file

Running the Application
1. Start the Flask server:
flask run
2. Open browser and navigate to:
http://localhost:5000

