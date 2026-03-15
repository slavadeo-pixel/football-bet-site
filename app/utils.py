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

    url = f"{BASE_URL}/fixtures?from={today}&to={future}"

    response = requests.get(url, headers=headers)

    data = response.json()

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

            # средние голы (пока фиксированные)
            "HomeGoalsAvg": 1.5,
            "AwayGoalsAvg": 1.3,

            # пример коэффициентов
            "HomeOdds": 2.1,
            "DrawOdds": 3.2,
            "AwayOdds": 3.1

        })

    return matches 
