import requests

API_KEY = "fa1b293b0c6ba1fa11843b282642600c"

headers = {
    "x-apisports-key": API_KEY
}

BASE_URL = "https://v3.football.api-sports.io"


def load_matches():

    url = f"{BASE_URL}/fixtures?next=100"

    response = requests.get(url, headers=headers)

    print("STATUS:", response.status_code)

    data = response.json()

    matches = []

    if "response" not in data:
        print("API ERROR:", data)
        return []

    for match in data["response"]:

        try:

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

        except Exception as e:

            print("MATCH PARSE ERROR:", e)

    print("MATCHES LOADED:", len(matches))

    return matches
