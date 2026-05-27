import os
import json
import re
import ssl
import urllib.request
import urllib.error
from typing import AsyncGenerator
import certifi

_SSL_CTX = ssl.create_default_context(cafile=certifi.where())

_API_KEY = os.environ.get("GEMINI_API_KEY", "")
AI_AVAILABLE = bool(_API_KEY)

_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/models"
_MODEL = "gemini-2.0-flash"

METHOD_NAMES = {
    "moscow": "MoSCoW (Must/Should/Could/Won't)",
    "topsis": "TOPSIS (Technique for Order of Preference by Similarity to Ideal Solution)",
    "kano": "Модель Кано",
    "fuzzy_ahp_type1": "Fuzzy AHP Type-1 (нечёткий метод иерархического анализа)",
    "fuzzy_ahp_type2": "Fuzzy AHP Type-2",
    "fuzzy_topsis": "Fuzzy TOPSIS (трапециевидные нечёткие числа)",
    "intuitionistic_topsis": "Интуиционистский нечёткий TOPSIS",
    "fuzzy_delphi": "Fuzzy Delphi (IT2FS)",
    "intuitionistic_delphi": "Интуиционистский Дельфи (IFS)",
}


def _generate(prompt: str) -> str:
    """Call Gemini generateContent REST endpoint."""
    url = f"{_BASE_URL}/{_MODEL}:generateContent?key={_API_KEY}"
    body = json.dumps({
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"maxOutputTokens": 800, "temperature": 0.4},
    }).encode()
    req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30, context=_SSL_CTX) as resp:
        data = json.loads(resp.read())
    return data["candidates"][0]["content"]["parts"][0]["text"]


def _stream_generate(system: str, history: list, user_message: str):
    """Call Gemini streamGenerateContent REST endpoint, yield text chunks."""
    url = f"{_BASE_URL}/{_MODEL}:streamGenerateContent?key={_API_KEY}&alt=sse"

    # Prepend system context to first user message
    contents = []
    for msg in history:
        role = "model" if msg["role"] == "assistant" else "user"
        contents.append({"role": role, "parts": [{"text": msg["content"]}]})
    full_user = f"{system}\n\nВопрос: {user_message}" if not history else user_message
    contents.append({"role": "user", "parts": [{"text": full_user}]})

    body = json.dumps({
        "contents": contents,
        "generationConfig": {"maxOutputTokens": 800, "temperature": 0.5},
    }).encode()
    req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"})

    with urllib.request.urlopen(req, timeout=60, context=_SSL_CTX) as resp:
        buffer = b""
        while True:
            chunk = resp.read(512)
            if not chunk:
                break
            buffer += chunk
            # Parse SSE lines
            while b"\n" in buffer:
                line, buffer = buffer.split(b"\n", 1)
                line = line.strip()
                if not line.startswith(b"data:"):
                    continue
                raw = line[5:].strip()
                if raw == b"[DONE]":
                    return
                try:
                    data = json.loads(raw)
                    text = data["candidates"][0]["content"]["parts"][0]["text"]
                    if text:
                        yield text
                except Exception:
                    pass


def generate_interpretation(method: str, results: dict) -> str:
    if not AI_AVAILABLE:
        return None

    sorted_results = sorted(results.items(), key=lambda x: x[1].get("score", 0), reverse=True)
    results_text = "\n".join(
        f"- {alt}: score={data.get('score', 0):.1f}, {data.get('comment', '')}"
        for alt, data in sorted_results
    )
    method_name = METHOD_NAMES.get(method, method)

    prompt = f"""Ты эксперт по приоритизации требований к ПО.
Проанализируй результаты метода {method_name} и дай:
1. 3-4 предложения: какие требования в приоритете и почему
2. Что стоит отметить (одинаковые score, необычные паттерны)
3. Краткую практическую рекомендацию для команды

Результаты (по убыванию приоритета):
{results_text}

Отвечай на том же языке, что и названия альтернатив. Будь краток."""

    try:
        return _generate(prompt)
    except urllib.error.HTTPError as e:
        if e.code == 429:
            return "⚠️ Достигнут дневной лимит Gemini API (бесплатный тариф). Лимит сбросится завтра в 00:00 UTC."
        return f"⚠️ Ошибка AI (HTTP {e.code})"
    except Exception as e:
        return f"⚠️ AI недоступен: {e}"


def analyze_conflicts_with_ai(conflicts: list, method: str) -> list:
    if not AI_AVAILABLE or not conflicts:
        return conflicts

    conflicts_text = "\n".join(
        f"- {c['alternative']}: {c['description']}" for c in conflicts
    )
    method_name = METHOD_NAMES.get(method, method)

    prompt = f"""Эксперт по управлению стейкхолдерами. Конфликты в анализе {method_name}:

{conflicts_text}

Для каждого конфликта — JSON-объект с полями: alternative, why (причина), resolution (стратегия).
Верни только JSON-массив, без markdown.
Отвечай на том же языке, что и названия требований."""

    try:
        text = _generate(prompt).strip()
        json_match = re.search(r"\[.*\]", text, re.DOTALL)
        if json_match:
            ai_analysis = json.loads(json_match.group())
            result = []
            for conflict in conflicts:
                matching = next(
                    (a for a in ai_analysis if a.get("alternative") == conflict["alternative"]),
                    None,
                )
                enriched = dict(conflict)
                if matching:
                    enriched["ai_why"] = matching.get("why", "")
                    enriched["ai_resolution"] = matching.get("resolution", "")
                result.append(enriched)
            return result
    except Exception:
        pass

    return conflicts


async def stream_chat(
    session_data: dict, user_message: str, chat_history: list
) -> AsyncGenerator[str, None]:
    if not AI_AVAILABLE:
        msg = "AI-чат недоступен: не задан GEMINI_API_KEY."
        yield f"data: {json.dumps({'chunk': msg}, ensure_ascii=False)}\n\n"
        yield f"data: {json.dumps({'done': True})}\n\n"
        return

    method = session_data.get("method", "unknown")
    results = session_data.get("results") or {}
    conflicts = session_data.get("ai_conflicts") or session_data.get("conflicts") or []
    ai_summary = session_data.get("ai_summary", "")

    top_items = sorted(results.items(), key=lambda x: x[1].get("score", 0), reverse=True)[:10]
    results_summary = "\n".join(
        f"  {alt}: {data.get('score', 0):.1f} — {data.get('comment', '')}"
        for alt, data in top_items
    )
    conflicts_text = ""
    if conflicts:
        conflicts_text = "\nКонфликты:\n" + "\n".join(
            f"  - {c.get('alternative')}: {c.get('description')}" for c in conflicts
        )

    system = f"""Ты AI-аналитик по приоритизации требований к ПО.

Метод: {METHOD_NAMES.get(method, method)}
Результаты:
{results_summary}
{conflicts_text}
Интерпретация: {ai_summary}

Отвечай конкретно, ссылайся на числа. Язык — как у пользователя."""

    try:
        for text_chunk in _stream_generate(system, chat_history[-10:], user_message):
            yield f"data: {json.dumps({'chunk': text_chunk}, ensure_ascii=False)}\n\n"
    except urllib.error.HTTPError as e:
        msg = "⚠️ Дневной лимит Gemini API исчерпан. Попробуйте завтра." if e.code == 429 else f"⚠️ Ошибка AI (HTTP {e.code})"
        yield f"data: {json.dumps({'chunk': msg}, ensure_ascii=False)}\n\n"
    except Exception as e:
        yield f"data: {json.dumps({'chunk': f'⚠️ AI недоступен: {e}'}, ensure_ascii=False)}\n\n"

    yield f"data: {json.dumps({'done': True})}\n\n"
