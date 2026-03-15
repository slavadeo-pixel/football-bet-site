import math

def poisson(k, lam):
    return (lam ** k * math.exp(-lam)) / math.factorial(k)


def match_probabilities(home_xg, away_xg, max_goals=6):

    probs = {}

    for i in range(max_goals + 1):
        for j in range(max_goals + 1):

            probs[f"{i}-{j}"] = poisson(i, home_xg) * poisson(j, away_xg)

    return probs


def outcome_probabilities(score_probs):

    home = 0
    draw = 0
    away = 0

    for score, p in score_probs.items():

        h, a = map(int, score.split("-"))

        if h > a:
            home += p

        elif h == a:
            draw += p

        else:
            away += p

    return home, draw, away


def fair_odds(prob):

    if prob == 0:
        return 0

    return round(1 / prob, 2)


def value_bet(probability, odds):

    value = probability * odds - 1

    return round(value * 100, 2)
