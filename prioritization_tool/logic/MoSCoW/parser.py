import pandas as pd
import re

# Разрешенные комбинации категорий (в алфавитном порядке)
VALID_COMBINATIONS = {
    ("M",), ("S",), ("C",), ("W",),
    ("C", "S"),
    ("M", "S"),
    ("C", "W"),
}

CATEGORY_ORDER = ["M", "S", "C", "W"]

def parse_score_string(score_str):
    """
    Преобразует строку вида "60% M, 40% S" в словарь {"M": 0.6, "S": 0.4}
    """
    score_str = score_str.strip('"').strip()
    parts = score_str.split(',')
    score_dict = {}
    total = 0.0

    for part in parts:
        match = re.match(r'\s*(\d+)%\s*([MSCW])', part.strip())
        if not match:
            raise ValueError(f"Неверный формат оценки: '{part.strip()}'")
        percent, label = match.groups()
        value = int(percent) / 100
        score_dict[label] = score_dict.get(label, 0.0) + value
        total += value

    # Проверка суммы процентов
    if abs(total - 1.0) > 0.01:
        raise ValueError(f"Сумма процентов должна быть 100%, а не {total * 100:.1f}%")

    # Проверка допустимых сочетаний
    keys = tuple(sorted(score_dict.keys()))
    if keys not in VALID_COMBINATIONS:
        raise ValueError(f"Недопустимое сочетание категорий: {list(score_dict.keys())}. "
                         f"Допустимы только пары: M/S, S/C, C/W, а также одиночные M, S, C, W.")

    return score_dict


def load_requirements(filepath):
    """
    Загружает и валидирует CSV с требованиями.
    Возвращает структуру вида: {альтернатива -> критерий -> стейкхолдер -> {"M": ..., "S": ...}}
    """
    df = pd.read_csv(filepath)
    required_cols = {"Альтернатива", "Критерий", "Стейкхолдер", "Оценка"}
    if not required_cols.issubset(df.columns):
        raise ValueError(f"Файл должен содержать столбцы: {', '.join(required_cols)}")

    data = {}

    for _, row in df.iterrows():
        alt = row["Альтернатива"]
        crit = row["Критерий"]
        stakeholder = row["Стейкхолдер"]
        score_str = row["Оценка"]

        try:
            parsed_score = parse_score_string(score_str)
        except ValueError as e:
            raise ValueError(f"Ошибка в строке с альтернативой '{alt}', критерием '{crit}', стейкхолдером '{stakeholder}': {e}")

        data.setdefault(alt, {}).setdefault(crit, {})[stakeholder] = parsed_score

    return data


def load_weights(filepath):
    """
    Загружает веса стейкхолдеров из CSV: {S1: 1.0, S2: 1.5, ...}
    """
    df = pd.read_csv(filepath)
    if not {"Стейкхолдер", "Вес"}.issubset(df.columns):
        raise ValueError("Файл с весами должен содержать столбцы: Стейкхолдер, Вес")

    weights = {}
    for _, row in df.iterrows():
        stakeholder = row["Стейкхолдер"]
        weight = float(row["Вес"])
        weights[stakeholder] = weight

    return weights
