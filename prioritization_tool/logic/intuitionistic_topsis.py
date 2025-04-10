import pandas as pd
import numpy as np
from typing import Dict, Tuple, Union

#
# def parse_ifs_scale(scale_path: str) -> Dict[str, Tuple[float, float, float]]:
#     """Загружает и парсит файл шкалы IFS"""
#     scale_df = pd.read_csv(scale_path)
#     scale_dict = {}
#     for _, row in scale_df.iterrows():
#         text = row["Оценка эксперта"].strip()
#         mu = float(row["Степень принадлежности"])
#         nu = float(row["Степень непринадлежности"])
#         pi = float(row["Степень неопределённости"])
#         scale_dict[text] = (mu, nu, pi)
#     return scale_dict
#
#
# def process_ifs_topsis(input_path: str, scale_path: str) -> dict:
#     """
#     Обрабатывает файл с текстовыми оценками IFS
#     Args:
#         input_path: путь к CSV с оценками альтернатив
#         scale_path: путь к CSV с шкалой преобразования
#     Returns:
#         Словарь с результатами ранжирования
#     """
#     # Загрузка шкалы
#     ifs_scale = parse_ifs_scale(scale_path)
#
#     # Проверка шкалы
#     for key, (mu, nu, pi) in ifs_scale.items():
#         if not (0 <= mu <= 1 and 0 <= nu <= 1 and 0 <= pi <= 1):
#             raise ValueError(f"Некорректные значения в шкале для оценки '{key}': μ={mu}, ν={nu}, π={pi}")
#         if not np.isclose(mu + nu + pi, 1.0, atol=0.1):
#             raise ValueError(f"Нарушено условие μ+ν+π≈1 для оценки '{key}': сумма={mu + nu + pi}")
#
#     # Загрузка и проверка входных данных
#     df = pd.read_csv(input_path)
#     if "Альтернатива" not in df.columns:
#         raise ValueError("Отсутствует обязательная колонка 'Альтернатива'")
#
#     alternatives = df["Альтернатива"].values
#     criteria_cols = [col for col in df.columns if col != "Альтернатива"]
#
#     # Преобразование текстовых оценок в числа
#     ifs_matrix = np.zeros((len(df), len(criteria_cols), 3))
#     for i, col in enumerate(criteria_cols):
#         for j, alt in enumerate(alternatives):
#             text_value = df.loc[j, col].strip()
#             if text_value not in ifs_scale:
#                 raise ValueError(f"Неизвестная оценка '{text_value}' в альтернативе '{alt}'")
#             ifs_matrix[j, i] = ifs_scale[text_value]
#
#     # Нормализация матрицы
#     norm_matrix = ifs_matrix / np.sqrt(np.sum(ifs_matrix ** 2, axis=0))
#
#     # Расчет идеальных решений
#     pis = np.max(norm_matrix, axis=0)
#     nis = np.min(norm_matrix, axis=0)
#
#     # Расчет расстояний
#     d_plus = np.sqrt(np.sum((norm_matrix - pis) ** 2, axis=1))
#     d_minus = np.sqrt(np.sum((norm_matrix - nis) ** 2, axis=1))
#
#     # Расчет индексов близости
#     c_scores = d_minus / (d_plus + d_minus)
#     c_scores = np.round(c_scores, 3)
#
#     # Формирование результатов
#     results = {}
#     for i, alt in enumerate(alternatives):
#         results[alt] = {
#             "score": float(c_scores[i]),
#             "details": {
#                 "distance_to_positive": float(d_plus[i]),
#                 "distance_to_negative": float(d_minus[i]),
#                 "ifs_values": {col: ifs_matrix[i, j].tolist() for j, col in enumerate(criteria_cols)}
#             }
#         }
#
#     return results

import pandas as pd
import numpy as np
from typing import Dict, Tuple, Union

def parse_ifs_scale(scale_path: str) -> Dict[str, Tuple[float, float, float]]:
    df = pd.read_csv(scale_path)
    scale_dict = {}
    for _, row in df.iterrows():
        label = row["Оценка эксперта"].strip()
        mu = float(row["Степень принадлежности"])
        nu = float(row["Степень непринадлежности"])
        pi = float(row["Степень неопределённости"])
        scale_dict[label] = (mu, nu, pi)
    return scale_dict

def calculate_ifs_topsis(input_path: str, scale_path: str) -> Dict[str, Dict[str, Union[float, str]]]:
    df = pd.read_csv(input_path)
    scale = parse_ifs_scale(scale_path)

    matrix = []
    alt_names = []
    for _, row in df.iterrows():
        alt_names.append(row["Альтернатива"])
        row_vals = []
        for col in df.columns[1:]:
            val = str(row[col]).strip()
            if val not in scale:
                raise ValueError(f"Недопустимое значение '{val}' в столбце '{col}'")
            row_vals.append(scale[val])
        matrix.append(row_vals)

    matrix = np.array(matrix)
    mu = matrix[:, :, 0]
    nu = matrix[:, :, 1]
    pi = matrix[:, :, 2]

    mu_plus = np.max(mu, axis=0)
    nu_minus = np.min(nu, axis=0)
    pi_minus = np.min(pi, axis=0)

    mu_minus = np.min(mu, axis=0)
    nu_plus = np.max(nu, axis=0)
    pi_plus = np.max(pi, axis=0)

    D_plus = np.sqrt(np.sum((mu - mu_plus)**2 + (nu - nu_minus)**2 + (pi - pi_minus)**2, axis=1))
    D_minus = np.sqrt(np.sum((mu - mu_minus)**2 + (nu - nu_plus)**2 + (pi - pi_plus)**2, axis=1))

    C = D_minus / (D_plus + D_minus)

    def interpret(c):
        if c >= 0.7:
            return "Высокий приоритет"
        elif c >= 0.4:
            return "Средний приоритет"
        else:
            return "Низкий приоритет"

    return {
        alt: {"score": round(float(ci), 4), "comment": interpret(ci)}
        for alt, ci in zip(alt_names, C)
    }