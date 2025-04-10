import os
import matplotlib.pyplot as plt
from fpdf import FPDF
import textwrap
import unicodedata


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
        "–": "-", "—": "-", "…": "...", "’": "'", "‘": "'", "“": '"', "”": '"',
        "\u00A0": " ", "\u200B": "", "🔹": "•"
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
        line = f"{clean_text(alt)} — {data['score']}%: {clean_text(data['comment'])}"
        lines = textwrap.wrap(line, width=100)
        if lines:
            pdf.multi_cell(0, 6, f"• {lines[0]}")
            for l in lines[1:]:
                pdf.multi_cell(0, 6, f"  {l}")
        pdf.ln(2)

    pdf.ln(4)


def generate_bar_chart(results, output_path="output/topsis_chart.png"):
    names = list(results.keys())
    scores = [res["score"] for res in results.values()]

    plt.figure(figsize=(10, 5))
    bars = plt.bar(names, scores, color='#2ecc71')
    plt.ylabel("Итоговый приоритет (%)")
    plt.title("Результаты приоритизации (TOPSIS)")
    plt.xticks(rotation=30, ha='right')
    plt.tight_layout()

    for bar, score in zip(bars, scores):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1,
                 f'{score}%', ha='center', va='bottom', fontsize=8)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path)
    plt.close()


def generate_topsis_report(results, filename="output/topsis_report.pdf"):
    chart_path = "output/topsis_chart.png"
    generate_bar_chart(results, chart_path)

    sorted_items = sorted(results.items(), key=lambda x: -x[1]["score"])
    high = [(k, v) for k, v in sorted_items if v["score"] > 65]
    medium = [(k, v) for k, v in sorted_items if 40 <= v["score"] <= 65]
    low = [(k, v) for k, v in sorted_items if v["score"] < 40]

    pdf = UnicodePDF()
    pdf.add_page()

    pdf.set_font("DejaVu", "B", 14)
    pdf.multi_cell(0, 10, "Отчет по приоритизации требований (метод TOPSIS)", align='C')
    pdf.ln(10)

    pdf.set_font("DejaVu", "", 10)
    pdf.multi_cell(0, 8, "Итоговая диаграмма:")
    try:
        pdf.image(chart_path, x=10, y=pdf.get_y(), w=190)
        pdf.ln(100 if len(results) <= 20 else 120)
    except Exception as e:
        pdf.multi_cell(0, 8, f"[Ошибка диаграммы: {str(e)}]", ln=True)
        pdf.ln(10)

    write_section(pdf, "🔺 Высокий приоритет (реализовать в первую очередь):", high)
    write_section(pdf, "🟡 Средний приоритет (возможна реализация при наличии ресурсов):", medium)
    write_section(pdf, "🔻 Низкий приоритет (может быть отложен):", low)

    os.makedirs(os.path.dirname(filename), exist_ok=True)
    pdf.output(filename)
