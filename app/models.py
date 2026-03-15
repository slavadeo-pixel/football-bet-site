import math

def poisson(k, lam):
    """Вероятность k голов при среднем λ"""
    return (lam ** k * math.exp(-lam)) / math.factorial(k)

def match_probabilities(lambda_home, lambda_away, max_goals=5):
    """Таблица вероятностей точных счетов"""
    probs = {}
    for i in range(0, max_goals+1):
        for j in range(0, max_goals+1):
            probs[f"{i}-{j}"] = poisson(i, lambda_home) * poisson(j, lambda_away)
    return probs

def fair_odds(prob):
    """Перевод вероятности в коэффициент"""
    return round(1 / prob, 2) if prob > 0 else 0

def value_percentage(model_prob, bookie_odds):
    """Value в процентах"""
    bookie_prob = 1 / bookie_odds
    return round((model_prob - bookie_prob) * 100, 2)

def roi(net_profit, total_staked):
    """ROI в процентах"""
    return round((net_profit / total_staked) * 100, 2)
