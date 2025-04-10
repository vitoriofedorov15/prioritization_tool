# import pandas as pd
# import numpy as np
# import re
#
#
# def parse_trapezoid(s):
#     """Парсит строку вида '(a,b,c,d)' в массив"""
#     if isinstance(s, str):
#         s = s.strip()
#         if s.startswith('(') and s.endswith(')'):
#             numbers = list(map(float, s[1:-1].split(',')))
#         else:
#             numbers = list(map(float, re.findall(r"[-+]?\d*\.\d+|\d+", s)))
#     elif isinstance(s, (int, float)):
#         numbers = [float(s)]
#     else:
#         numbers = list(map(float, s))
#
#     if len(numbers) == 1:
#         numbers = numbers * 4
#     elif len(numbers) != 4:
#         raise ValueError(f"Ожидается 4 числа, получено {len(numbers)}")
#
#     return np.array(numbers)
#
# def normalize_fuzzy_matrix(fuzzy_matrix):
#     """Нормализация трапециевидных чисел"""
#     n_rows, n_cols = fuzzy_matrix.shape[:2]
#     # Находим максимальные верхние границы (d-значения) для каждого критерия
#     max_upper = np.max(fuzzy_matrix[:, :, 3], axis=0)
#
#     norm_matrix = np.zeros_like(fuzzy_matrix)
#
#     for i in range(n_rows):
#         for j in range(n_cols):
#             # Поэлементное деление каждого компонента трапециевидного числа
#             norm_matrix[i, j] = np.array([
#                 fuzzy_matrix[i, j, 0] / max_upper[j],
#                 fuzzy_matrix[i, j, 1] / max_upper[j],
#                 fuzzy_matrix[i, j, 2] / max_upper[j],
#                 fuzzy_matrix[i, j, 3] / max_upper[j]
#             ])
#     return norm_matrix
#
# def fuzzy_distance(a, b):
#     """Расстояние между двумя трапециевидными числами"""
#     return np.sqrt(np.mean((np.array(a) - np.array(b)) ** 2))
#
#
# def parse_scale_file(scale_path):
#     """Парсит файл шкалы с числами в скобках"""
#     scale_df = pd.read_csv(scale_path)
#     scale_dict = {}
#
#     for _, row in scale_df.iterrows():
#         text = row["Оценка эксперта"].strip()
#         trapezoid_str = row["Трапециевидное число"].strip()
#
#         # Проверяем формат (должны быть скобки)
#         if not (trapezoid_str.startswith('(') and trapezoid_str.endswith(')')):
#             raise ValueError(
#                 f"Неверный формат трапециевидного числа для '{text}': {trapezoid_str}. Должны быть скобки.")
#         for text, numbers in scale_dict.items():
#             if not isinstance(numbers, np.ndarray) or numbers.shape != (4,):
#                 raise ValueError(f"Некорректный формат чисел для оценки '{text}' в шкале")
#         # Парсим числа внутри скобок
#         try:
#             numbers = list(map(float, trapezoid_str[1:-1].split(',')))
#             if len(numbers) != 4:
#                 raise ValueError(f"Нужно 4 числа, получено {len(numbers)}")
#             scale_dict[text] = np.array(numbers)
#         except Exception as e:
#             raise ValueError(f"Ошибка парсинга числа для '{text}': {str(e)}")
#
#     return scale_dict
#
# def process_fuzzy_topsis(filepath, scale_path):
#     # Загрузка данных
#     df = pd.read_csv(filepath)
#
#     # Проверка обязательных колонок
#     if "Альтернатива" not in df.columns:
#         raise ValueError("Файл должен содержать колонку 'Альтернатива'")
#
#     # Загрузка шкалы
#     scale_dict = parse_scale_file(scale_path)
#
#     # Проверка всех оценок
#     for col in df.columns[1:]:  # Все колонки кроме "Альтернатива"
#         invalid_values = set(df[col]) - set(scale_dict.keys())
#         if invalid_values:
#             raise ValueError(
#                 f"Найдены недопустимые оценки в колонке '{col}': {invalid_values}\n"
#                 f"Допустимые значения: {list(scale_dict.keys())}"
#             )
#
#     # Создание матрицы
#     alternatives = df["Альтернатива"].values
#     criteria_cols = df.columns[1:]  # Все колонки кроме первой
#
#     fuzzy_matrix = np.zeros((len(df), len(criteria_cols), 4), dtype=np.float64)
#
#     for i, col in enumerate(criteria_cols):
#         for j, alt in enumerate(alternatives):
#             text_value = df.loc[j, col].strip()
#             fuzzy_matrix[j, i] = scale_dict[text_value]
#
#     # Дальнейшая обработка (нормализация, расчеты)
#     norm_matrix = normalize_fuzzy_matrix(fuzzy_matrix)
#     pis = np.max(norm_matrix, axis=0)
#     nis = np.min(norm_matrix, axis=0)
#
#     # Расстояния до PIS и NIS
#     # Расчет расстояний до идеальных решений
#     d_plus = np.zeros(len(alternatives))
#     d_minus = np.zeros(len(alternatives))
#
#     for i in range(len(alternatives)):
#         for j in range(len(criteria_cols)):
#             # Расчет расстояния для каждого критерия отдельно
#             d_plus[i] += fuzzy_distance(norm_matrix[i, j], pis[j]) ** 2
#             d_minus[i] += fuzzy_distance(norm_matrix[i, j], nis[j]) ** 2
#
#         # Извлечение квадратного корня для евклидова расстояния
#         d_plus[i] = np.sqrt(d_plus[i])
#         d_minus[i] = np.sqrt(d_minus[i])
#     # Приоритет
#     c_scores = d_minus / (d_plus + d_minus)
#     c_scores = np.round(c_scores, 3)
#
#     results = {}
#     for i, alt in enumerate(alternatives):
#         score = float(c_scores[i])
#         results[alt] = {
#             "score": score,
#             "comment": f"Индекс близости к идеальному решению: {score}"
#         }
#
#     return results


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