from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from app.models import match_probabilities, fair_odds, value_percentage
from app.utils import load_matches
from datetime import datetime, timedelta
import pytz
import os

app = FastAPI(title="Football Betting Site")

# Загружаем CSV
matches_df = load_matches()

MOSCOW = pytz.timezone("Europe/Moscow")


@app.get("/", response_class=HTMLResponse)
def home():
    html_file = os.path.join("frontend", "index.html")
    with open(html_file, "r", encoding="utf-8") as f:
        return f.read()


@app.get("/matches")
def get_matches():

    results = []

    now = datetime.now(MOSCOW)
    two_weeks = now + timedelta(days=14)

    for _, row in matches_df.iterrows():

        match_date_str = row.get("Date")

        if not match_date_str:
            continue

        try:
            # читаем дату из CSV
            match_date = datetime.strptime(str(match_date_str), "%d/%m/%Y")
            match_date = MOSCOW.localize(match_date)

        except:
            continue

        # показываем только матчи сегодня и на 14 дней вперед
        if match_date < now or match_date > two_weeks:
            continue

        lambda_home = row.get("HomeGoalsAvg", 1.5)
        lambda_away = row.get("AwayGoalsAvg", 1.2)

        probs = match_probabilities(lambda_home, lambda_away)

        home_prob = sum(v for k, v in probs.items() if int(k.split("-")[0]) > int(k.split("-")[1]))
        draw_prob = sum(v for k, v in probs.items() if int(k.split("-")[0]) == int(k.split("-")[1]))
        away_prob = sum(v for k, v in probs.items() if int(k.split("-")[0]) < int(k.split("-")[1]))

        fair_home = fair_odds(home_prob)
        fair_draw = fair_odds(draw_prob)
        fair_away = fair_odds(away_prob)

        value_home = value_percentage(home_prob, row.get("HomeOdds", 2.0))
        value_draw = value_percentage(draw_prob, row.get("DrawOdds", 3.3))
        value_away = value_percentage(away_prob, row.get("AwayOdds", 2.8))

        recommendations = []

        if value_home > 5:
            recommendations.append("Value на победу хозяев")

        if value_draw > 5:
            recommendations.append("Value на ничью")

        if value_away > 5:
            recommendations.append("Value на победу гостей")

        results.append({

            "league": row.get("League", "Unknown"),
            "home_team": row.get("HomeTeam", ""),
            "away_team": row.get("AwayTeam", ""),
            "date": match_date.strftime("%d/%m/%Y %H:%M"),

            "value": {
                "home": value_home,
                "draw": value_draw,
                "away": value_away
            },

            "highlight": {
                "home": "green" if value_home > 5 else "yellow" if value_home > 2 else "red",
                "draw": "green" if value_draw > 5 else "yellow" if value_draw > 2 else "red",
                "away": "green" if value_away > 5 else "yellow" if value_away > 2 else "red"
            },

            "recommendations": recommendations

        })

    return results
