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