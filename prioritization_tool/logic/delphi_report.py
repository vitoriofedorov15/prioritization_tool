import os
import matplotlib.pyplot as plt
from fpdf import FPDF
import textwrap
import unicodedata
import numpy as np

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
    if not text:
        return ""
    replacements = {
        "–": "-", "—": "-", "…": "...", "’": "'", "‘": "'", "“": '"', "”": '"',
        "\u00A0": " ", "\u200B": "", "🔹": "•"
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    text = ''.join(c for c in text if unicodedata.category(c)[0] != 'C')
    text = ''.join(c for c in text if ord(c) < 65536)
    return text.strip()[:max_length]

def safe_multicell(pdf, line, width=100, cell_height=5):
    wrapped_lines = textwrap.wrap(clean_text(line), width=width, break_long_words=True, break_on_hyphens=True)
    if not wrapped_lines:
        wrapped_lines = ["."]
    for l in wrapped_lines:
        try:
            pdf.multi_cell(0, cell_height, l)
        except Exception as e:
            print(f"Ошибка при выводе строки: '{l}' → {e}")

def write_section(pdf, title, items):
    pdf.set_font("DejaVu", "B", 12)
    pdf.set_text_color(0, 0, 128)
    safe_multicell(pdf, title, width=90, cell_height=7)
    pdf.set_draw_color(180, 180, 180)
    pdf.set_line_width(0.5)
    pdf.cell(0, 1, "", ln=True, border="T")
    pdf.ln(3)

    pdf.set_font("DejaVu", "", 9)
    pdf.set_text_color(0, 0, 0)

    for alt, data in items:
        line = f"• {alt} — коэффициент уверенности: {data['confidence_index']}"
        safe_multicell(pdf, line, width=90)
        pdf.ln(2)
    pdf.ln(4)

def generate_bar_chart(results, output_path, title):
    names = list(results.keys())
    scores = [r['confidence_index'] for r in results.values()]

    plt.figure(figsize=(10, 5))
    bars = plt.bar(names, scores)
    plt.ylabel("Коэффициент уверенности")
    plt.title(title)
    plt.xticks(rotation=30, ha='right')
    plt.tight_layout()

    for bar, score in zip(bars, scores):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.01,
                 f'{score}', ha='center', va='bottom', fontsize=8)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path)
    plt.close()

def classify(results):
    sorted_items = sorted(results.items(), key=lambda x: -x[1]['confidence_index'])
    high = [(k, v) for k, v in sorted_items if v['confidence_index'] >= 0.6]
    medium = [(k, v) for k, v in sorted_items if 0.4 <= v['confidence_index'] < 0.6]
    low = [(k, v) for k, v in sorted_items if v['confidence_index'] < 0.4]
    return high, medium, low

def generate_combined_report(results_type2, results_ifs, filename="output/fuzzy_delphi_report.pdf"):
    chart_type2 = "output/chart_delphi_type2.png"
    chart_ifs = "output/chart_delphi_ifs.png"

    generate_bar_chart(results_type2, chart_type2, "Fuzzy Delphi Type-2")
    generate_bar_chart(results_ifs, chart_ifs, "Delphi Intuitionistic")

    high_t2, med_t2, low_t2 = classify(results_type2)
    high_ifs, med_ifs, low_ifs = classify(results_ifs)

    pdf = UnicodePDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    pdf.set_font("DejaVu", "B", 14)
    safe_multicell(pdf, "Отчет по приоритизации требований (Fuzzy Delphi)", width=100, cell_height=8)
    pdf.ln(10)

    pdf.set_font("DejaVu", "B", 12)
    safe_multicell(pdf, "Метод Fuzzy Delphi Type-2", width=100)
    pdf.set_font("DejaVu", "", 9)
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
        safe_multicell(pdf, "[Диаграмма недоступна]")
        pdf.ln(10)

    write_section(pdf, "Высокий приоритет:", high_t2)
    write_section(pdf, "Средний приоритет:", med_t2)
    write_section(pdf, "Низкий приоритет:", low_t2)

    pdf.add_page()
    pdf.set_font("DejaVu", "B", 12)
    safe_multicell(pdf, "Метод Delphi Intuitionistic", width=100)
    pdf.set_font("DejaVu", "", 9)
    pdf.ln(2)

    try:
        if pdf.h - pdf.y > 100:
            pdf.image(chart_ifs, x=10, y=pdf.get_y(), w=180)
            pdf.ln(110)
        else:
            pdf.add_page()
            pdf.image(chart_ifs, x=10, y=20, w=180)
            pdf.ln(110)
    except Exception as e:
        safe_multicell(pdf, "[Диаграмма недоступна]")
        pdf.ln(10)

    write_section(pdf, "Высокий приоритет:", high_ifs)
    write_section(pdf, "Средний приоритет:", med_ifs)
    write_section(pdf, "Низкий приоритет:", low_ifs)

    os.makedirs(os.path.dirname(filename), exist_ok=True)
    pdf.output(filename)