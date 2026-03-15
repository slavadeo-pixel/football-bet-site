import requests
from datetime import datetime, timedelta

API_KEY = "fa1b293b0c6ba1fa11843b282642600c"

BASE_URL = "https://v3.football.api-sports.io"

headers = {
    "x-apisports-key": API_KEY
}


def load_matches():

    today = datetime.utcnow().strftime("%Y-%m-%d")

    future = (datetime.utcnow() + timedelta(days=14)).strftime("%Y-%m-%d")

    url = f"{BASE_URL}/fixtures?next=100"

    response = requests.get(url, headers=headers)

    print("API STATUS:", response.status_code)

    data = response.json()

    print("API RESPONSE:", data)

    matches = []

    if "response" not in data:
        return []

    for match in data["response"]:

        league = match["league"]["name"]

        home = match["teams"]["home"]["name"]
        away = match["teams"]["away"]["name"]

        date = match["fixture"]["date"]

        matches.append({
            "League": league,
            "HomeTeam": home,
            "AwayTeam": away,
            "Date": date,
            "HomeGoalsAvg": 1.5,
            "AwayGoalsAvg": 1.3,
            "HomeOdds": 2.0,
            "DrawOdds": 3.2,
            "AwayOdds": 3.0
        })

    print("MATCHES FOUND:", len(matches))

    return matches
