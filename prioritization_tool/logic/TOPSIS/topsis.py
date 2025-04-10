import pandas as pd
import numpy as np


def process_topsis(file_path):
    df = pd.read_csv(file_path)

    if "Альтернатива" not in df.columns or "Вес стейкхолдера" not in df.columns:
        raise ValueError("CSV должен содержать колонки 'Альтернатива' и 'Вес стейкхолдера'")

    alt_names = df["Альтернатива"]
    stakeholder_weights = df["Вес стейкхолдера"].astype(float).values
    criteria_cols = [col for col in df.columns if col not in ["Альтернатива", "Вес стейкхолдера"]]
    matrix = df[criteria_cols].astype(float).values

    # 1. Нормализация
    norm_matrix = matrix / np.sqrt((matrix ** 2).sum(axis=0))

    # 2. Взвешивание по весам стейкхолдеров (на каждую строку)
    weighted_matrix = norm_matrix * stakeholder_weights[:, np.newaxis]

    # 3. Идеальные решения (PIS и NIS)
    pis = np.max(weighted_matrix, axis=0)
    nis = np.min(weighted_matrix, axis=0)

    # 4. Расстояния до идеалов
    d_plus = np.linalg.norm(weighted_matrix - pis, axis=1)
    d_minus = np.linalg.norm(weighted_matrix - nis, axis=1)

    # 5. Расчет приоритета
    scores = d_minus / (d_plus + d_minus)
    scores = np.round(scores, 3)

    # 6. Классификация по диапазонам
    results = {}
    for i, name in enumerate(alt_names):
        score = scores[i]
        if score > 0.65:
            comment = "Высокий приоритет (реализовать в первую очередь)"
        elif score >= 0.4:
            comment = "Средний приоритет (возможна реализация при наличии ресурсов)"
        else:
            comment = "Низкий приоритет (может быть отложен)"

        results[name] = {
            "score": round(score * 100, 2),
            "comment": comment
        }

    return results
