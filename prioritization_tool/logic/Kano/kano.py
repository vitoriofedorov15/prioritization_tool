import pandas as pd
from collections import defaultdict, Counter

# Матрица Кано: пары функционального и дисфункционального ответа → категория
KANO_MATRIX = {
    ("Attractive", "Must-be"): "One-dimensional",
    ("Attractive", "Indifferent"): "Attractive",
    ("Attractive", "Reverse"): "Questionable",
    ("Attractive", "Attractive"): "Attractive",
    ("Must-be", "Must-be"): "Must-be",
    ("Must-be", "Indifferent"): "Must-be",
    ("Must-be", "Reverse"): "Reverse",
    ("Indifferent", "Must-be"): "One-dimensional",
    ("Indifferent", "Indifferent"): "Indifferent",
    ("Indifferent", "Reverse"): "Reverse",
    ("Reverse", "Must-be"): "Questionable",
    ("Reverse", "Indifferent"): "Reverse",
    ("Reverse", "Reverse"): "Reverse",
}

# Весовая значимость категорий для подсчета итогового score
CATEGORY_WEIGHTS = {
    "Must-be": 1.0,
    "One-dimensional": 0.8,
    "Attractive": 0.6,
    "Indifferent": 0.3,
    "Reverse": 0.1,
    "Questionable": 0.0
}

def process_kano_csv(filepath):
    df = pd.read_csv(filepath)
    required_cols = {"Альтернатива", "Стейкхолдер", "Функциональный", "Дисфункциональный", "Вес"}
    if not required_cols.issubset(df.columns):
        raise ValueError("CSV должен содержать колонки: Альтернатива, Стейкхолдер, Функциональный, Дисфункциональный, Вес")

    results = defaultdict(list)

    for _, row in df.iterrows():
        alt = row["Альтернатива"]
        f = str(row["Функциональный"]).strip()
        d = str(row["Дисфункциональный"]).strip()
        weight = float(row["Вес"])

        category = KANO_MATRIX.get((f, d), "Questionable")
        results[alt].append((category, weight))

    final = {}

    for alt, votes in results.items():
        counter = Counter()
        for cat, w in votes:
            counter[cat] += w

        distribution = dict(counter)
        weighted_priority = sum(CATEGORY_WEIGHTS.get(cat, 0) * weight for cat, weight in counter.items())
        score = round((weighted_priority / sum(counter.values())) * 100, 2) if counter else 0.0

        final[alt] = {
            "distribution": distribution,
            "score": score,
            "comment": f"Итоговая значимость по шкале Кано: {score}%"
        }

    return final
