import requests

API_KEY = "530a55cc2ed9c60ee0458dd6e8f77cd4"

url = "https://v3.football.api-sports.io/fixtures?next=50"

headers = {
    "x-apisports-key": API_KEY
}

def load_matches():

    response = requests.get(url, headers=headers)

    print("STATUS:", response.status_code)

    data = response.json()

    matches = []

    if "response" not in data:
        print("API ERROR:", data)
        return []

    for m in data["response"]:

        matches.append({
            "League": m["league"]["name"],
            "HomeTeam": m["teams"]["home"]["name"],
            "AwayTeam": m["teams"]["away"]["name"],
            "Date": m["fixture"]["date"],
            "HomeGoalsAvg": 1.5,
            "AwayGoalsAvg": 1.2,
            "HomeOdds": 2.0,
            "DrawOdds": 3.2,
            "AwayOdds": 3.0
        })

    print("MATCHES:", len(matches))

    return matches
