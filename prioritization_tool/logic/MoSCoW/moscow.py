import math

CATEGORY_WEIGHTS = {"M": 3, "S": 2, "C": 1, "W": 0}


def calculate_individual_score(score_dict):
    """
    Вычисляет оценку по формуле: 3M + 2S + 1C + 0W
    """
    return sum(CATEGORY_WEIGHTS.get(k, 0) * v for k, v in score_dict.items())


def calculate(alternatives_data, weights):
    """
    Основная функция для расчета приоритетов по MoSCoW
    """
    raw_scores = {}  # альтернатива -> взвешенная сумма
    all_individual = {}  # альтернатива -> [все индивидуальные оценки]

    max_score = 0.0

    for alt, crit_data in alternatives_data.items():
        alt_total = 0.0
        weight_total = 0.0

        individual_scores = []

        for crit, stakeholder_scores in crit_data.items():
            for stakeholder, score_dict in stakeholder_scores.items():
                weight = weights.get(stakeholder, 1.0)
                score = calculate_individual_score(score_dict)
                alt_total += score * weight
                weight_total += weight
                individual_scores.append(score)

        avg_score = alt_total / weight_total if weight_total > 0 else 0.0
        raw_scores[alt] = avg_score
        all_individual[alt] = individual_scores

        if avg_score > max_score:
            max_score = avg_score

    results = {}
    for alt, score in raw_scores.items():
        normalized = round((score / max_score) * 100, 1) if max_score > 0 else 0.0
        comment = interpret_priority(normalized)
        results[alt] = {
            "score": normalized,
            "comment": comment
        }

    return results


def interpret_priority(score):
    if score >= 80:
        return "Высокий приоритет — реализовать в первую очередь"
    elif score >= 50:
        return "Средний приоритет — желательно реализовать"
    else:
        return "Низкий приоритет — можно отложить"
