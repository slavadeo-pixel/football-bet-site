import math

def poisson(k, lam):
    return (lam ** k * math.exp(-lam)) / math.factorial(k)

def match_probabilities(lambda_home, lambda_away, max_goals=5):
    probs = {}
    for i in range(0, max_goals+1):
        for j in range(0, max_goals+1):
            probs[f"{i}-{j}"] = poisson(i, lambda_home) * poisson(j, lambda_away)
    return probs

def fair_odds(prob):
    return round(1 / prob, 2) if prob > 0 else 0

def value_percentage(model_prob, bookie_odds):
    bookie_prob = 1 / bookie_odds
    return round((model_prob - bookie_prob) * 100, 2)
