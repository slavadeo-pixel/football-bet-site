from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from app.models import match_probabilities, fair_odds, value_percentage
from app.utils import load_matches, update_all_leagues
import os

app = FastAPI(title="Football Betting Site")

matches_df = load_matches()

@app.get("/", response_class=HTMLResponse)
def home():
    html_file = os.path.join("frontend", "index.html")
    with open(html_file, "r", encoding="utf-8") as f:
        return f.read()

@app.get("/matches")
def get_matches():
    results = []
    for _, row in matches_df.iterrows():
        lambda_home = row.get('HomeGoalsAvg', 1.5)
        lambda_away = row.get('AwayGoalsAvg', 1.2)
        probs = match_probabilities(lambda_home, lambda_away)

        fair_home = fair_odds(sum([v for k,v in probs.items() if int(k.split('-')[0]) > int(k.split('-')[1])]))
        fair_draw = fair_odds(sum([v for k,v in probs.items() if int(k.split('-')[0]) == int(k.split('-')[1])]))
        fair_away = fair_odds(sum([v for k,v in probs.items() if int(k.split('-')[0]) < int(k.split('-')[1])]))

        value_home = value_percentage(0.45, row.get('HomeOdds', 2.0))
        value_draw = value_percentage(0.27, row.get('DrawOdds', 3.3))
        value_away = value_percentage(0.28, row.get('AwayOdds', 2.8))

        recommendations = []
        if value_home > 5 and fair_home > 2:
            recommendations.append("Ставка на победу хозяев")
        if value_draw > 5 and fair_draw > 2.5:
            recommendations.append("Ставка на ничью")
        if value_away > 5 and fair_away > 2:
            recommendations.append("Ставка на победу гостей")

        results.append({
            "home_team": row.get('HomeTeam', 'Home'),
            "away_team": row.get('AwayTeam', 'Away'),
            "league": row.get('League', 'Unknown'),
            "fair_odds": {"home": fair_home, "draw": fair_draw, "away": fair_away},
            "value": {"home": value_home, "draw": value_draw, "away": value_away},
            "highlight": {
                "home": "green" if value_home > 5 else "yellow" if value_home > 3 else "red",
                "draw": "green" if value_draw > 5 else "yellow" if value_draw > 3 else "red",
                "away": "green" if value_away > 5 else "yellow" if value_away > 3 else "red"
            },
            "recommendations": recommendations
        })
    return results
