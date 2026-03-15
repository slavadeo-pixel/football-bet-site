from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from app.utils import load_matches
from app.models import match_probabilities, outcome_probabilities, value_bet
import os
from datetime import datetime, timedelta
import pytz

app = FastAPI()

MOSCOW = pytz.timezone("Europe/Moscow")

matches_df = load_matches()


@app.get("/", response_class=HTMLResponse)
def home():

    with open("frontend/index.html", "r", encoding="utf-8") as f:

        return f.read()


@app.get("/matches")
def matches():

    results = []

    now = datetime.now(MOSCOW)

    future = now + timedelta(days=14)

    for _, row in matches_df.iterrows():

        try:

            date = datetime.strptime(row["Date"], "%d/%m/%Y")

            date = MOSCOW.localize(date)

        except:
            continue

        if date < now or date > future:
            continue

        home_xg = row.get("HomeGoalsAvg", 1.5)
        away_xg = row.get("AwayGoalsAvg", 1.3)

        score_probs = match_probabilities(home_xg, away_xg)

        home_prob, draw_prob, away_prob = outcome_probabilities(score_probs)

        home_odds = row.get("HomeOdds", 2.0)
        draw_odds = row.get("DrawOdds", 3.2)
        away_odds = row.get("AwayOdds", 3.0)

        home_value = value_bet(home_prob, home_odds)
        draw_value = value_bet(draw_prob, draw_odds)
        away_value = value_bet(away_prob, away_odds)

        results.append({

            "league": row.get("League"),

            "home": row.get("HomeTeam"),

            "away": row.get("AwayTeam"),

            "date": date.strftime("%d/%m/%Y %H:%M"),

            "home_value": home_value,

            "draw_value": draw_value,

            "away_value": away_value

        })

    results.sort(key=lambda x: max(x["home_value"], x["draw_value"], x["away_value"]), reverse=True)

    return results
