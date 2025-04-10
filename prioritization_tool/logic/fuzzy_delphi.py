import pandas as pd
import numpy as np
import re

# Лингвистические оценки с модификаторами уверенности
LINGUISTIC_IT2FS = {
    "Очень низкая": (0.0, 0.1, 0.1, 0.2),
    "Низкая": (0.2, 0.3, 0.3, 0.4),
    "Средняя": (0.3, 0.5, 0.5, 0.7),
    "Высокая": (0.5, 0.7, 0.7, 0.9),
    "Очень высокая": (0.8, 0.9, 0.9, 1.0),
}

CONFIDENCE_MODIFIER = {
    "Очень высокая уверенность": 0.05,
    "Высокая уверенность": 0.1,
    "Средняя уверенность": 0.2,
    "Низкая уверенность": 0.3,
}


def clean_string(s):
    """Очистка строки от кавычек и лишних пробелов"""
    return str(s).strip().strip('"\'') if pd.notna(s) else ""


def parse_linguistic_it2fs(s):
    """Парсинг лингвистических оценок в IT2FS"""
    s_clean = clean_string(s)
    if not s_clean:
        return np.array([0, 0, 0, 0])

    try:
        # Разделяем на уверенность и значение
        parts = [p.strip() for p in s_clean.split("–") if p.strip()]
        if len(parts) != 2:
            raise ValueError(f"Неверный формат оценки: {s_clean}")

        conf_part, value_part = parts
        base = LINGUISTIC_IT2FS[value_part]
        mod = CONFIDENCE_MODIFIER[conf_part]

        lower = (max(0, base[0] - mod), max(0, base[1] - mod))
        upper = (min(1, base[2] + mod), min(1, base[3] + mod))

        return np.array([lower[0], lower[1], upper[0], upper[1]])
    except KeyError as e:
        raise ValueError(f"Неизвестное значение в оценке '{s_clean}': {str(e)}")
    except Exception as e:
        raise ValueError(f"Ошибка при разборе оценки '{s_clean}': {str(e)}")


def process_fuzzy_delphi(filepath):
    """Обработка файла с лингвистическими оценками (Fuzzy Delphi IT2FS)"""
    try:
        # Чтение CSV с обработкой кавычек
        df = pd.read_csv(filepath, quotechar='"')

        # Нормализация названий столбцов
        df.columns = [clean_string(col) for col in df.columns]

        # Проверка обязательных столбцов
        required = {"Альтернатива", "Эксперт", "Вес эксперта"}
        missing = required - set(df.columns)
        if missing:
            raise ValueError(f"Отсутствуют обязательные столбцы: {missing}")

        criteria_cols = [col for col in df.columns if col not in required]
        grouped = df.groupby("Альтернатива")
        results = {}

        for alt, group in grouped:
            crit_result = {}
            for crit in criteria_cols:
                values = group[crit].apply(parse_linguistic_it2fs).tolist()
                weights = group["Вес эксперта"].astype(float).to_numpy()
                values = np.array(values)

                # Взвешенное среднее
                mean = np.average(values, axis=0, weights=weights)
                fou = mean[3] - mean[0]  # Размах неопределенности

                crit_result[crit] = {
                    "mean": tuple(np.round(mean, 3)),
                    "fou": round(fou, 3)
                }

            # Индекс уверенности (1 - средний размах неопределенности)
            avg_fou = np.mean([v["fou"] for v in crit_result.values()])
            results[alt] = {
                "criteria": crit_result,
                "confidence_index": round(1 - avg_fou, 3)
            }

        return results

    except Exception as e:
        raise ValueError(f"Ошибка обработки файла Fuzzy Delphi: {str(e)}")


def parse_ifs(s):
    """Парсинг строк вида (μ, ν, π) в массив"""
    s_clean = clean_string(s)
    if not s_clean:
        return np.array([0, 0, 0])

    try:
        # Удаляем все скобки и кавычки
        s_clean = re.sub(r'[()"\']', '', s_clean)
        numbers = list(map(float, re.findall(r"[-+]?\d*\.\d+|\d+", s_clean)))

        if len(numbers) != 3:
            raise ValueError(f"Ожидалось 3 числа, получено {len(numbers)}")

        # Проверка допустимости значений
        if not (0 <= numbers[0] <= 1 and 0 <= numbers[1] <= 1 and 0 <= numbers[2] <= 1):
            raise ValueError("Значения должны быть в диапазоне [0, 1]")

        if not np.isclose(sum(numbers), 1.0, atol=0.01):
            raise ValueError(f"Сумма значений должна быть ~1.0 (получено {sum(numbers)})")

        return np.array(numbers)
    except Exception as e:
        raise ValueError(f"Ошибка при разборе IFS '{s_clean}': {str(e)}")


def process_delphi_ifs(filepath):
    """Обработка файла с IFS-оценками (Delphi Intuitionistic)"""
    try:
        # Чтение CSV с обработкой кавычек
        df = pd.read_csv(filepath, quotechar='"')

        # Нормализация названий столбцов
        df.columns = [clean_string(col) for col in df.columns]

        # Проверка обязательных столбцов
        required = {"Альтернатива", "Эксперт", "Вес эксперта"}
        missing = required - set(df.columns)
        if missing:
            raise ValueError(f"Отсутствуют обязательные столбцы: {missing}")

        criteria_cols = [col for col in df.columns if col not in required]
        grouped = df.groupby("Альтернатива")
        results = {}

        for alt, group in grouped:
            crit_result = {}
            expert_pis = []
            weights = group["Вес эксперта"].astype(float).to_numpy()

            for crit in criteria_cols:
                values = group[crit].apply(parse_ifs).tolist()
                values = np.array(values)

                # Взвешенное среднее
                mean = np.average(values, axis=0, weights=weights)
                pi_values = values[:, 2]  # Параметры неопределенности
                fou = np.max(pi_values) - np.min(pi_values)  # Размах неопределенности

                crit_result[crit] = {
                    "mean": tuple(np.round(mean, 3)),
                    "fou": round(fou, 3)
                }
                expert_pis.extend(pi_values)

            # Индекс уверенности (1 - средняя неопределенность)
            avg_pi = np.mean(expert_pis)
            results[alt] = {
                "criteria": crit_result,
                "confidence_index": round(1 - avg_pi, 3)
            }

        return results

    except Exception as e:
        raise ValueError(f"Ошибка обработки файла Delphi Intuitionistic: {str(e)}")