from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from datetime import datetime
import pytz

from app.utils import load_matches
from app.models import match_probabilities, outcome_probabilities, value_bet

app = FastAPI()

MOSCOW = pytz.timezone("Europe/Moscow")


@app.get("/", response_class=HTMLResponse)
def home():

    with open("frontend/index.html", "r", encoding="utf-8") as f:

        return f.read()


@app.get("/matches")
def matches():

    matches_data = load_matches()

    results = []

    for row in matches_data:

        try:

            date = datetime.fromisoformat(row["Date"].replace("Z", "+00:00"))

            date = date.astimezone(MOSCOW)

        except Exception as e:

            print("DATE ERROR:", e)

            continue

        home_xg = row["HomeGoalsAvg"]
        away_xg = row["AwayGoalsAvg"]

        score_probs = match_probabilities(home_xg, away_xg)

        home_prob, draw_prob, away_prob = outcome_probabilities(score_probs)

        home_value = value_bet(home_prob, row["HomeOdds"])
        draw_value = value_bet(draw_prob, row["DrawOdds"])
        away_value = value_bet(away_prob, row["AwayOdds"])

        results.append({

            "league": row["League"],

            "home": row["HomeTeam"],

            "away": row["AwayTeam"],

            "date": date.strftime("%d.%m.%Y %H:%M"),

            "home_value": home_value,

            "draw_value": draw_value,

            "away_value": away_value

        })

    return results
