import os
import matplotlib.pyplot as plt
from fpdf import FPDF
import textwrap
import unicodedata


class UnicodePDF(FPDF):
    def __init__(self):
        super().__init__()
        try:
            self.add_font("DejaVu", "", "fonts/DejaVuSans.ttf", uni=True)
            self.add_font("DejaVu", "B", "fonts/DejaVuSans-Bold.ttf", uni=True)
            self.set_font("DejaVu", "", 9)
        except:
            self.set_font("Arial", "", 9)


def clean_text(text, max_length=300):
    """Очистка текста для корректного отображения в PDF"""
    if not text:
        return ""
    replacements = {
        "–": "-", "—": "-", "…": "...", "’": "'", "‘": "'", "“": '"', "”": '"',
        "\u00A0": " ", "\u200B": "", "🔹": "•"
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    text = ''.join(c for c in text if unicodedata.category(c)[0] != 'C')
    return text.strip()[:max_length]


def safe_multicell(pdf, text, width=100, cell_height=5):
    """Безопасный вывод текста с переносами"""
    wrapped_lines = textwrap.wrap(clean_text(text), width=width,
                                  break_long_words=True, break_on_hyphens=True)
    if not wrapped_lines:
        wrapped_lines = [" "]
    for line in wrapped_lines:
        try:
            pdf.multi_cell(0, cell_height, line)
        except Exception as e:
            print(f"Ошибка при выводе текста: '{line}' → {e}")


def write_section(pdf, title, items):
    """Форматирование секции отчета"""
    pdf.set_font("DejaVu", "B", 12)
    pdf.set_text_color(0, 0, 128)
    safe_multicell(pdf, title, width=90, cell_height=7)
    pdf.set_draw_color(180, 180, 180)
    pdf.set_line_width(0.5)
    pdf.cell(0, 1, "", ln=True, border="T")
    pdf.ln(3)

    pdf.set_font("DejaVu", "", 9)
    pdf.set_text_color(0, 0, 0)

    for name, data in items:
        if isinstance(data, dict):
            score = data.get('score', 0)
            comment = data.get('comment', '')
            line = f"• {name} — Итоговый приоритет: {score:.4f} {comment}"
        else:
            line = f"• {name} — Итоговый приоритет: {data:.4f}"
        safe_multicell(pdf, line, width=90)
        pdf.ln(2)
    pdf.ln(4)


def generate_bar_chart(results, output_path, title):
    """Генерация столбчатой диаграммы"""
    names = list(results.keys())
    scores = [r['score'] if isinstance(r, dict) else r for r in results.values()]

    plt.figure(figsize=(10, 5))
    bars = plt.bar(names, scores, color='#4e79a7')
    plt.ylabel("Значение")
    plt.title(title)
    plt.xticks(rotation=30, ha='right')

    for bar, score in zip(bars, scores):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.01,
                 f'{score:.3f}', ha='center', va='bottom', fontsize=8)

    plt.tight_layout()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()


def classify(results):
    """Классификация результатов по приоритетам"""
    sorted_items = sorted(results.items(),
                          key=lambda x: -x[1]['score'] if isinstance(x[1], dict) else -x[1])
    high = [(k, v) for k, v in sorted_items if (v['score'] if isinstance(v, dict) else v) >= 0.6]
    medium = [(k, v) for k, v in sorted_items if 0.4 <= (v['score'] if isinstance(v, dict) else v) < 0.6]
    low = [(k, v) for k, v in sorted_items if (v['score'] if isinstance(v, dict) else v) < 0.4]
    return high, medium, low


def generate_report(results_type1, results_type2, filename="output/fuzzy_ahp_report.pdf"):
    """Генерация комбинированного отчета AHP"""
    # Подготовка данных для Type-2
    type2_formatted = {k: {'score': v, 'comment': ''} for k, v in results_type2.items()}

    # Генерация графиков
    chart_type1 = "output/charts/ahp_type1.png"
    chart_type2 = "output/charts/ahp_type2.png"
    generate_bar_chart(results_type1, chart_type1, "Fuzzy AHP Type-1 (Приоритеты альтернатив)")
    generate_bar_chart(type2_formatted, chart_type2, "Fuzzy AHP Type-2 (Веса критериев)")

    # Классификация результатов
    high_t1, med_t1, low_t1 = classify(results_type1)
    high_t2, med_t2, low_t2 = classify(type2_formatted)

    # Создание PDF
    pdf = UnicodePDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Заголовок отчета
    pdf.set_font("DejaVu", "B", 14)
    safe_multicell(pdf, "Отчет по приоритизации требований (Fuzzy AHP)", width=100, cell_height=8)
    pdf.ln(10)

    # Раздел Type-1
    pdf.set_font("DejaVu", "B", 12)
    safe_multicell(pdf, "Результаты Fuzzy AHP Type-1 (Альтернативы)", width=100)
    pdf.ln(2)

    try:
        if pdf.h - pdf.y > 100:
            pdf.image(chart_type1, x=10, y=pdf.get_y(), w=180)
            pdf.ln(110)
        else:
            pdf.add_page()
            pdf.image(chart_type1, x=10, y=20, w=180)
            pdf.ln(110)
    except Exception as e:
        safe_multicell(pdf, f"[Ошибка загрузки диаграммы: {str(e)}]")
        pdf.ln(10)

    write_section(pdf, "Высокий приоритет (≥ 0.6):", high_t1)
    write_section(pdf, "Средний приоритет (0.4-0.6):", med_t1)
    write_section(pdf, "Низкий приоритет (< 0.4):", low_t1)

    # Раздел Type-2
    pdf.add_page()
    pdf.set_font("DejaVu", "B", 12)
    safe_multicell(pdf, "Результаты Fuzzy AHP Type-2 (Критерии)", width=100)
    pdf.ln(2)

    try:
        if pdf.h - pdf.y > 100:
            pdf.image(chart_type2, x=10, y=pdf.get_y(), w=180)
            pdf.ln(110)
        else:
            pdf.add_page()
            pdf.image(chart_type2, x=10, y=20, w=180)
            pdf.ln(110)
    except Exception as e:
        safe_multicell(pdf, f"[Ошибка загрузки диаграммы: {str(e)}]")
        pdf.ln(10)

    write_section(pdf, "Ключевые критерии (≥ 0.6):", high_t2)
    write_section(pdf, "Средние критерии (0.4-0.6):", med_t2)
    write_section(pdf, "Второстепенные критерии (< 0.4):", low_t2)

    # Сохранение отчета
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    pdf.output(filename)