import os
import matplotlib.pyplot as plt
from fpdf import FPDF
import unicodedata
import textwrap


class UnicodePDF(FPDF):
    def __init__(self):
        super().__init__()
        self.add_font("DejaVu", "", "fonts/DejaVuSans.ttf", uni=True)
        self.add_font("DejaVu", "B", "fonts/DejaVuSans-Bold.ttf", uni=True)
        self.set_font("DejaVu", "", 10)


def clean_text(text, max_length=300):
    if not text:
        return ""
    replacements = {
        "–": "-", "—": "-", "…": "...", "’": "'", "‘": "'",
        "“": '"', "”": '"', "\u00A0": " ", "\u200B": "", "🔹": "•"
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    text = ''.join(c for c in text if unicodedata.category(c)[0] != 'C')
    text = ''.join(c for c in text if ord(c) < 65536)
    return text.strip()[:max_length]


def write_section(pdf, title, items):
    pdf.set_font("DejaVu", "B", 12)
    pdf.set_text_color(0, 0, 128)
    pdf.multi_cell(0, 8, clean_text(title))
    pdf.set_draw_color(180, 180, 180)
    pdf.set_line_width(0.5)
    pdf.cell(0, 1, "", ln=True, border="T")
    pdf.ln(3)

    pdf.set_font("DejaVu", "", 10)
    pdf.set_text_color(0, 0, 0)

    for alt, data in items:
        line = f"{clean_text(alt)} — {data['score']} : {clean_text(data['comment'])}"
        lines = textwrap.wrap(line, width=100)
        if lines:
            pdf.multi_cell(0, 6, f"• {lines[0]}")
            for l in lines[1:]:
                pdf.multi_cell(0, 6, f"  {l}")
        pdf.ln(2)
    pdf.ln(4)


def generate_bar_chart(results, output_path, title):
    names = list(results.keys())
    scores = [res["score"] for res in results.values()]

    plt.figure(figsize=(10, 5))
    bars = plt.bar(names, scores)
    plt.ylabel("Индекс приоритета")
    plt.title(title)
    plt.xticks(rotation=30, ha='right')
    plt.tight_layout()

    for bar, score in zip(bars, scores):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.01,
                 f'{score:.3f}', ha='center', va='bottom', fontsize=8)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path)
    plt.close()


def generate_combined_report(fuzzy_results, ifs_results, filename="output/fuzzy_topsis_report.pdf"):
    chart_fuzzy = "output/fuzzy_chart.png"
    chart_ifs = "output/ifs_chart.png"

    generate_bar_chart(fuzzy_results, chart_fuzzy, "Fuzzy TOPSIS Type-1")
    generate_bar_chart(ifs_results, chart_ifs, "Intuitionistic Fuzzy TOPSIS")

    def classify(results):
        sorted_items = sorted(results.items(), key=lambda x: -x[1]["score"])
        high = [(k, v) for k, v in sorted_items if v["score"] >= 0.7]
        medium = [(k, v) for k, v in sorted_items if 0.4 <= v["score"] < 0.7]
        low = [(k, v) for k, v in sorted_items if v["score"] < 0.4]
        return high, medium, low

    fuzzy_high, fuzzy_med, fuzzy_low = classify(fuzzy_results)
    ifs_high, ifs_med, ifs_low = classify(ifs_results)

    pdf = UnicodePDF()
    pdf.add_page()

    pdf.set_font("DejaVu", "B", 14)
    pdf.multi_cell(0, 10, "Отчет по приоритизации требований (Fuzzy TOPSIS)", align='C')
    pdf.ln(10)

    pdf.set_font("DejaVu", "B", 12)
    pdf.multi_cell(0, 8, "Метод Fuzzy TOPSIS Type-1")
    pdf.set_font("DejaVu", "", 10)
    pdf.ln(2)

    try:
        pdf.image(chart_fuzzy, x=10, y=pdf.get_y(), w=190)
        pdf.ln(110 if len(fuzzy_results) <= 20 else 130)
    except:
        pdf.multi_cell(0, 6, "[Диаграмма Fuzzy TOPSIS Type-1 недоступна]")
        pdf.ln(10)

    write_section(pdf, "Высокий приоритет:", fuzzy_high)
    write_section(pdf, "Средний приоритет:", fuzzy_med)
    write_section(pdf, "Низкий приоритет:", fuzzy_low)

    pdf.add_page()
    pdf.set_font("DejaVu", "B", 12)
    pdf.multi_cell(0, 8, "Метод Intuitionistic Fuzzy TOPSIS")
    pdf.set_font("DejaVu", "", 10)
    pdf.ln(2)

    try:
        pdf.image(chart_ifs, x=10, y=pdf.get_y(), w=190)
        pdf.ln(110 if len(ifs_results) <= 20 else 130)
    except:
        pdf.multi_cell(0, 6, "[Диаграмма Intuitionistic TOPSIS недоступна]")
        pdf.ln(10)

    write_section(pdf, "Высокий приоритет:", ifs_high)
    write_section(pdf, "Средний приоритет:", ifs_med)
    write_section(pdf, "Низкий приоритет:", ifs_low)

    os.makedirs(os.path.dirname(filename), exist_ok=True)
    pdf.output(filename)