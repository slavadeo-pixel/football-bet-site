import os
import pandas as pd
import requests
import json

API_KEY = os.getenv("FOOTBALL_API_KEY")
BASE_URL = "https://www.football-data.co.uk/mmz4281"

def load_matches(folder="data/all_leagues"):
    all_files = []
    for file in os.listdir(folder):
        if file.endswith(".csv"):
            df = pd.read_csv(os.path.join(folder, file))
            all_files.append(df)
    if all_files:
        return pd.concat(all_files, ignore_index=True)
    return pd.DataFrame()

def fetch_csv_for_league(league_code, season="2526"):
    url = f"{BASE_URL}/{league_code}.csv"
    response = requests.get(url, headers={"X-Auth-Token": API_KEY})
    if response.status_code == 200:
        csv_path = f"data/all_leagues/{league_code}_{season}.csv"
        with open(csv_path, "wb") as f:
            f.write(response.content)
        print(f"Updated {csv_path}")
        return csv_path
    else:
        print(f"Error downloading {league_code}: {response.status_code}")
        return None

def update_all_leagues():
    with open("app/leagues.json") as f:
        leagues = json.load(f)
    for league_code in leagues:
        fetch_csv_for_league(league_code)
