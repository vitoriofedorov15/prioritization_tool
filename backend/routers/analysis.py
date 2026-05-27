import statistics
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.session import get_session, update_session
from services.logic_bridge import (
    moscow_calculate,
    load_requirements,
    load_weights,
    process_topsis,
    process_kano_csv,
    process_fuzzy_ahp_type1,
    process_fuzzy_ahp_type2,
    calculate_fuzzy_topsis,
    process_fuzzy_delphi,
    process_delphi_ifs,
    calculate_ifs_topsis,
)

router = APIRouter()

MOSCOW_WEIGHTS = {"M": 3, "S": 2, "C": 1, "W": 0}


def _safe(obj):
    if isinstance(obj, dict):
        return {k: _safe(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_safe(v) for v in obj]
    if hasattr(obj, "item"):
        return obj.item()
    return obj


def detect_moscow_conflicts(alternatives_data: dict) -> list:
    conflicts = []
    for alt, crit_data in alternatives_data.items():
        all_cats, scores = [], []
        for sh_scores in crit_data.values():
            for score_dict in sh_scores.values():
                primary = max(score_dict, key=lambda k: score_dict[k])
                all_cats.append(primary)
                scores.append(sum(MOSCOW_WEIGHTS.get(k, 0) * v for k, v in score_dict.items()))

        if "M" in all_cats and "W" in all_cats:
            conflicts.append(
                {
                    "alternative": alt,
                    "type": "hard",
                    "description": f"Жёсткий конфликт: одни стейкхолдеры считают '{alt}' обязательным (Must), другие — ненужным (Won't)",
                }
            )
        elif len(scores) > 1 and statistics.stdev(scores) > 0.7:
            std = statistics.stdev(scores)
            conflicts.append(
                {
                    "alternative": alt,
                    "type": "soft",
                    "description": f"Расхождение оценок '{alt}' между стейкхолдерами (σ={std:.2f})",
                }
            )
    return conflicts


def detect_kano_conflicts(results: dict) -> list:
    conflicts = []
    for alt, data in results.items():
        dist = data.get("distribution", {})
        total = sum(dist.values())
        if total == 0:
            continue
        must = dist.get("Must-be", 0) / total
        attr = dist.get("Attractive", 0) / total
        rev = dist.get("Reverse", 0) / total

        if rev > 0.2 and (must + attr) > 0.3:
            conflicts.append(
                {
                    "alternative": alt,
                    "type": "hard",
                    "description": f"Конфликт: часть стейкхолдеров негативно оценивает '{alt}' (Reverse {rev:.0%}), другие — позитивно",
                }
            )
        elif must > 0.3 and attr > 0.3:
            conflicts.append(
                {
                    "alternative": alt,
                    "type": "soft",
                    "description": f"Неоднозначная Kano-классификация '{alt}': Must-be {must:.0%} vs Attractive {attr:.0%}",
                }
            )
    return conflicts


def detect_delphi_conflicts(results: dict) -> list:
    return [
        {
            "alternative": alt,
            "type": "soft",
            "description": f"Низкая согласованность экспертов для '{alt}' (индекс уверенности: {data.get('confidence_index', 0):.2f})",
        }
        for alt, data in results.items()
        if data.get("confidence_index", 1.0) < 0.6
    ]


class AnalyzeRequest(BaseModel):
    session_id: str


@router.post("/analyze/{method}")
async def analyze(method: str, req: AnalyzeRequest):
    session = get_session(req.session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Сессия не найдена")

    files = session["files"]
    conflicts = []

    def need(*keys):
        missing = [k for k in keys if not files.get(k)]
        if missing:
            raise HTTPException(status_code=400, detail=f"Не загружены файлы: {', '.join(missing)}")

    try:
        if method == "moscow":
            need("requirements_file", "weights_file")
            alt_data = load_requirements(files["requirements_file"])
            weights = load_weights(files["weights_file"])
            results = moscow_calculate(alt_data, weights)
            conflicts = detect_moscow_conflicts(alt_data)

        elif method == "topsis":
            need("data_file")
            results = process_topsis(files["data_file"])

        elif method == "kano":
            need("data_file")
            results = process_kano_csv(files["data_file"])
            conflicts = detect_kano_conflicts(results)

        elif method == "fuzzy_ahp_type1":
            need("criteria_file", "alternatives_file", "weights_file")
            results = process_fuzzy_ahp_type1(
                files["criteria_file"], files["alternatives_file"], files["weights_file"]
            )

        elif method == "fuzzy_ahp_type2":
            need("data_file")
            raw = process_fuzzy_ahp_type2(files["data_file"])
            results = {
                k: {"score": round(v * 100, 2), "comment": f"Нормализованный вес критерия: {v:.4f}"}
                for k, v in raw.items()
            }

        elif method == "fuzzy_topsis":
            need("data_file", "scale_file")
            results = calculate_fuzzy_topsis(files["data_file"], files["scale_file"])

        elif method == "intuitionistic_topsis":
            need("data_file", "scale_file")
            results = calculate_ifs_topsis(files["data_file"], files["scale_file"])

        elif method == "fuzzy_delphi":
            need("data_file")
            raw = process_fuzzy_delphi(files["data_file"])
            results = {
                alt: {
                    "score": round(d["confidence_index"] * 100, 2),
                    "comment": f"Индекс уверенности: {d['confidence_index']}",
                }
                for alt, d in raw.items()
            }
            conflicts = detect_delphi_conflicts({a: {"confidence_index": d["confidence_index"]} for a, d in raw.items()})

        elif method == "intuitionistic_delphi":
            need("data_file")
            raw = process_delphi_ifs(files["data_file"])
            results = {
                alt: {
                    "score": round(d["confidence_index"] * 100, 2),
                    "comment": f"Индекс уверенности: {d['confidence_index']}",
                }
                for alt, d in raw.items()
            }
            conflicts = detect_delphi_conflicts({a: {"confidence_index": d["confidence_index"]} for a, d in raw.items()})

        else:
            raise HTTPException(status_code=400, detail=f"Неизвестный метод: {method}")

        results = _safe(results)
        conflicts = _safe(conflicts)

        update_session(req.session_id, method=method, results=results, conflicts=conflicts)

        return {"success": True, "method": method, "results": results, "conflicts": conflicts}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
