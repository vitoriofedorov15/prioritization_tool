import pandas as pd
import numpy as np
import re
from typing import Dict, Tuple, List

# ============================ TYPE-1 ============================

fuzzy_scale_type1 = {
    "1": (1.0, 1.0, 1.0),
    "2": (1.5, 2.0, 2.5),
    "3": (2.5, 3.0, 3.5),
    "5": (4.5, 5.0, 5.5),
    "7": (6.5, 7.0, 7.5),
    "9": (8.5, 9.0, 9.5),
    "1/2": (0.4, 0.5, 0.6),
    "1/3": (0.28, 0.33, 0.38),
    "1/5": (0.17, 0.2, 0.25),
    "1/7": (0.13, 0.14, 0.16),
    "1/9": (0.1, 0.11, 0.12),
}


def parse_tfn(value: str) -> np.ndarray:
    """Парсит треугольное нечеткое число из строки"""
    if pd.isna(value):
        raise ValueError("Пустое значение TFN")

    value = str(value).strip().strip('"').strip()

    if value in fuzzy_scale_type1:
        return np.array(fuzzy_scale_type1[value])

    if re.match(r"\(.*\)", value):
        nums = list(map(float, re.findall(r"[-+]?\d*\.?\d+", value)))
        if len(nums) == 3:
            return np.array(nums)

    raise ValueError(f"Неверный формат TFN: {value}")


def geometric_mean(tfn_list: List[np.ndarray]) -> np.ndarray:
    """Вычисляет геометрическое среднее для списка TFN"""
    tfn_array = np.array(tfn_list)
    return np.exp(np.mean(np.log(tfn_array), axis=0))


def defuzzify(tfn: np.ndarray) -> float:
    """Дефаззификация треугольного числа (центроид)"""
    return np.mean(tfn)


def normalize_weights(weights: List[float]) -> List[float]:
    """Нормализует веса к сумме 1"""
    total = sum(weights)
    return [w / total for w in weights]


def process_fuzzy_ahp_type1(
        criteria_path: str,
        alternatives_path: str,
        weights_path: str
) -> Dict[str, Dict[str, float]]:
    """Основная функция обработки для Type-1 Fuzzy AHP"""

    # Загрузка данных с явным указанием quotechar
    df_criteria = pd.read_csv(criteria_path, quotechar='"')
    df_alternatives = pd.read_csv(alternatives_path, quotechar='"')
    df_weights = pd.read_csv(weights_path, quotechar='"')

    # Проверка обязательных колонок
    if "Эксперт" not in df_weights.columns or "Вес" not in df_weights.columns:
        raise ValueError("Файл весов должен содержать колонки 'Эксперт' и 'Вес'")

    if "Альтернатива" not in df_alternatives.columns or "Эксперт" not in df_alternatives.columns:
        raise ValueError("Файл альтернатив должен содержать колонки 'Альтернатива' и 'Эксперт'")

    # Обработка критериев
    criteria_names = df_criteria.columns[1:].tolist()
    n = len(criteria_names)

    # Построение матрицы парных сравнений
    fuzzy_matrix = np.zeros((n, n, 3))
    for i in range(n):
        for j in range(n):
            val = str(df_criteria.iloc[i, j + 1])
            fuzzy_matrix[i, j] = parse_tfn(val)

    # Вычисление весов критериев
    row_gm = np.array([geometric_mean(fuzzy_matrix[i]) for i in range(n)])
    weights_fuzzy = normalize_weights([defuzzify(row) for row in row_gm])

    # Обработка альтернатив
    alternatives = df_alternatives["Альтернатива"].unique()
    crit_names = [col for col in df_alternatives.columns
                  if col not in ["Альтернатива", "Эксперт"]]

    # Создаем словарь весов экспертов
    expert_weights = dict(zip(
        df_weights["Эксперт"],
        df_weights["Вес"].astype(float)
    ))

    # Проверка суммы весов экспертов
    total_weight = sum(expert_weights.values())
    if not np.isclose(total_weight, 1.0, atol=0.01):
        raise ValueError(f"Сумма весов экспертов должна быть 1.0 (получено {total_weight})")

    alt_scores = {}
    for alt in alternatives:
        alt_data = df_alternatives[df_alternatives["Альтернатива"] == alt]
        crit_scores = []

        for crit in crit_names:
            # Агрегируем оценки всех экспертов по критерию
            weighted_sum = np.zeros(3)
            total_weight = 0.0

            for _, row in alt_data.iterrows():
                expert = row["Эксперт"]
                weight = expert_weights.get(expert, 0.0)
                tfn = parse_tfn(row[crit])
                weighted_sum += tfn * weight
                total_weight += weight

            if total_weight > 0:
                aggregated = weighted_sum / total_weight
                crit_scores.append(defuzzify(aggregated))
            else:
                crit_scores.append(0.0)

        # Итоговый приоритет альтернативы
        total_score = sum(w * s for w, s in zip(weights_fuzzy, crit_scores))
        alt_scores[alt] = {
            "score": round(total_score, 4),
            "comment": f"Итоговый приоритет: {round(total_score, 4)}"
        }

    return alt_scores


# ============================ TYPE-2 ============================

def fuzzy_saaty_type2_scale() -> Dict[str, Tuple[Tuple[float, ...], Tuple[float, ...]]]:
    return {
        "Одинаково": ((1.0, 1.0, 1.0, 1.0), (1.0, 1.0, 1.0, 1.0)),
        "Слабо": ((1.5, 2.0, 2.0, 2.5), (1.3, 2.0, 2.0, 2.7)),
        "Умеренно": ((2.5, 3.0, 3.0, 3.5), (2.2, 3.0, 3.0, 3.8)),
        "Сильно": ((4.5, 5.0, 5.0, 5.5), (4.0, 5.0, 5.0, 6.0)),
        "Абсолютно": ((8.5, 9.0, 9.0, 9.5), (8.0, 9.0, 9.0, 10.0)),
    }


def parse_type2_label(label: str) -> Tuple[np.ndarray, np.ndarray]:
    """Парсит метки Type-2 в нижние и верхние функции принадлежности"""
    scale = fuzzy_saaty_type2_scale()
    label = str(label).strip().strip('"').capitalize()
    if label not in scale:
        raise ValueError(f"Неверная оценка '{label}'. Допустимые: {list(scale.keys())}")
    return np.array(scale[label][0]), np.array(scale[label][1])


def defuzzify_type2(lower: np.ndarray, upper: np.ndarray) -> float:
    """Дефаззификация интервального Type-2 нечеткого числа"""
    c1 = np.mean([lower[0], lower[1], lower[3]])
    c2 = np.mean([upper[0], upper[2], upper[3]])
    return (c1 + c2) / 2


def process_fuzzy_ahp_type2(filepath: str) -> Dict[str, float]:
    """Основная функция обработки для Type-2 Fuzzy AHP"""

    df = pd.read_csv(filepath, quotechar='"')

    # Проверка обязательных колонок
    required_cols = {"Эксперт", "Вес"}
    if not required_cols.issubset(df.columns):
        missing = required_cols - set(df.columns)
        raise ValueError(f"Отсутствуют обязательные колонки: {missing}")

    # Проверка суммы весов экспертов
    total_weight = df["Вес"].astype(float).sum()
    if not np.isclose(total_weight, 1.0, atol=0.01):
        raise ValueError(f"Сумма весов экспертов должна быть 1.0 (получено {total_weight})")

    # Извлечение критериев из названий колонок
    comparison_cols = [col for col in df.columns
                       if col not in ["Эксперт", "Вес"]]
    criteria = sorted({c for col in comparison_cols
                       for c in col.split(" > ")})
    n = len(criteria)

    # Агрегация оценок экспертов
    aggregated = {}
    for col in comparison_cols:
        lower_sums = np.zeros(4)
        upper_sums = np.zeros(4)
        total_weight = 0.0

        for _, row in df.iterrows():
            weight = float(row["Вес"])
            lower, upper = parse_type2_label(row[col])
            lower_sums += lower * weight
            upper_sums += upper * weight
            total_weight += weight

        if total_weight > 0:
            aggregated[col] = (
                lower_sums / total_weight,
                upper_sums / total_weight
            )

    # Построение матрицы парных сравнений
    matrix = np.eye(n)
    crit_to_idx = {crit: i for i, crit in enumerate(criteria)}

    for pair, (lower, upper) in aggregated.items():
        a, b = pair.split(" > ")
        i, j = crit_to_idx[a], crit_to_idx[b]
        crisp_val = defuzzify_type2(lower, upper)
        matrix[i, j] = crisp_val
        matrix[j, i] = 1 / crisp_val

    # Вычисление весов критериев
    normalized = matrix / matrix.sum(axis=0)
    weights = normalized.mean(axis=1)
    weights /= weights.sum()  # Нормализация к сумме 1

    return {crit: float(weight) for crit, weight in zip(criteria, weights)}