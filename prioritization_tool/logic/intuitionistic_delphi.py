import pandas as pd
from collections import defaultdict


def parse_ifs(value):
    try:
        value = value.strip().replace("(", "").replace(")", "")
        parts = value.split(",")
        if len(parts) != 3:
            raise ValueError(f"Ожидается 3 значения, получено {len(parts)}: {value}")
        mu, nu, pi = map(float, parts)
        return mu, nu, pi
    except Exception as e:
        raise ValueError(f"Неверный формат IFS-числа: {value} — {str(e)}")


def process_intuitionistic_delphi_csv(filepath):
    df = pd.read_csv(filepath)
    required_cols = {"Альтернатива", "Эксперт", "Вес эксперта"}
    if not required_cols.issubset(df.columns):
        raise ValueError("CSV должен содержать колонки: Альтернатива, Эксперт, критерии, Вес эксперта")

    criteria = [col for col in df.columns if col not in {"Альтернатива", "Эксперт", "Вес эксперта"}]
    results = defaultdict(lambda: defaultdict(list))

    for _, row in df.iterrows():
        alt = row["Альтернатива"]
        weight = float(row["Вес эксперта"])

        for crit in criteria:
            mu, nu, pi = parse_ifs(str(row[crit]))
            results[alt][crit].append(((mu, nu, pi), weight))

    final_results = {}
    for alt, crit_dict in results.items():
        aggregated = {}
        for crit, values in crit_dict.items():
            mu_sum = sum(mu * w for (mu, _, _), w in values)
            nu_sum = sum(nu * w for (_, nu, _), w in values)
            pi_vals = [pi for (_, _, pi), _ in values]

            weight_sum = sum(w for _, w in values)
            mu_avg = mu_sum / weight_sum if weight_sum else 0
            nu_avg = nu_sum / weight_sum if weight_sum else 0
            pi_range = max(pi_vals) - min(pi_vals) if pi_vals else 0

            aggregated[crit] = {
                "mu": round(mu_avg, 3),
                "nu": round(nu_avg, 3),
                "pi_range": round(pi_range, 3),
                "confidence": round(1 - pi_range, 3)
            }

        final_results[alt] = aggregated

    return final_results
