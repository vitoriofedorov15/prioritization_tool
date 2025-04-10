import pandas as pd
import numpy as np
import re


def parse_trapezoid(value):
    numbers = list(map(float, re.findall(r"[-+]?\d*\.?\d+", value)))
    if len(numbers) == 1:
        numbers *= 4
    if len(numbers) != 4:
        raise ValueError(f"Неверное трапециевидное число: {value}")
    return np.array(numbers)


def parse_fuzzy_scale(scale_path):
    df = pd.read_csv(scale_path)
    scale_dict = {}
    for _, row in df.iterrows():
        label = row["Оценка эксперта"].strip()
        trapezoid_str = str(row["Трапециевидное число"])
        scale_dict[label] = parse_trapezoid(trapezoid_str)
    return scale_dict


def normalize_fuzzy_matrix(fuzzy_matrix):
    n_alts, n_criteria = fuzzy_matrix.shape[:2]
    normalized = np.zeros_like(fuzzy_matrix)
    for j in range(n_criteria):
        col_max = np.max(fuzzy_matrix[:, j, 3])
        for i in range(n_alts):
            a, b, c, d = fuzzy_matrix[i, j]
            normalized[i, j] = np.array([a / col_max, b / col_max, c / col_max, d / col_max])
    return normalized


def fuzzy_distance(a, b):
    return np.sqrt(np.sum((a - b) ** 2) / 4)


def interpret_score(score):
    if score >= 0.7:
        return "Высокий приоритет"
    elif score >= 0.4:
        return "Средний приоритет"
    else:
        return "Низкий приоритет"


def calculate_fuzzy_topsis(input_path: str, scale_path: str) -> dict:
    df = pd.read_csv(input_path)
    scale = parse_fuzzy_scale(scale_path)

    fuzzy_matrix = []
    alt_names = []
    for _, row in df.iterrows():
        alt_names.append(row["Альтернатива"])
        alt_values = []
        for col in df.columns[1:]:
            key = str(row[col]).strip()
            if key not in scale:
                raise ValueError(f"Недопустимое значение '{key}' в столбце '{col}'")
            alt_values.append(scale[key])
        fuzzy_matrix.append(alt_values)

    fuzzy_matrix = np.array(fuzzy_matrix)
    norm_matrix = normalize_fuzzy_matrix(fuzzy_matrix)

    F_plus = np.max(norm_matrix, axis=0)
    F_minus = np.min(norm_matrix, axis=0)

    D_plus = np.array([
        np.sqrt(np.sum([fuzzy_distance(norm_matrix[i, j], F_plus[j]) ** 2
                        for j in range(norm_matrix.shape[1])]))
        for i in range(norm_matrix.shape[0])
    ])

    D_minus = np.array([
        np.sqrt(np.sum([fuzzy_distance(norm_matrix[i, j], F_minus[j]) ** 2
                        for j in range(norm_matrix.shape[1])]))
        for i in range(norm_matrix.shape[0])
    ])

    C = D_minus / (D_plus + D_minus)

    return {
        alt: {"score": round(float(score), 4), "comment": interpret_score(score)}
        for alt, score in zip(alt_names, C)
    }