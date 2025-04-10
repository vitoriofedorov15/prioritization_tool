import os
import matplotlib.pyplot as plt
from fpdf import FPDF
import textwrap
import unicodedata


class UnicodePDF(FPDF):
    def __init__(self):
        super().__init__()
        # Шрифт с поддержкой Unicode (убедитесь, что файлы шрифтов в папке fonts/)
        self.add_font("DejaVu", "", "fonts/DejaVuSans.ttf", uni=True)
        self.add_font("DejaVu", "B", "fonts/DejaVuSans-Bold.ttf", uni=True)
        self.set_font("DejaVu", "", 10)  # Уменьшен размер шрифта для безопасности


def generate_bar_chart(results, output_path="output/chart.png"):
    names = list(results.keys())
    scores = [res["score"] for res in results.values()]

    plt.figure(figsize=(10, 5))
    bars = plt.bar(names, scores)
    plt.ylabel("Приоритет (%)")
    plt.title("Результаты приоритизации (MoSCoW)")
    plt.xticks(rotation=30, ha='right')
    plt.tight_layout()

    for bar, score in zip(bars, scores):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1,
                 f'{score}%', ha='center', va='bottom', fontsize=8)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path)
    plt.close()


def categorize_results(results):
    high, medium, low = [], [], []

    for alt, data in sorted(results.items(), key=lambda x: -x[1]["score"]):
        alt = alt[:30] + "..." if len(alt) > 30 else alt
        comment = data["comment"][:50] + "..." if len(data["comment"]) > 50 else data["comment"]

        line = f"{alt} — {data['score']}%: {comment}"

        if data["score"] >= 80:
            high.append(line)
        elif data["score"] >= 50:
            medium.append(line)
        else:
            low.append(line)

    return high, medium, low

def clean_text(text):
    """Удаляет проблемные символы"""
    if not text:
        return ""

    replacements = {
        "–": "-", "—": "-", "…": "...",
        "’": "'", "‘": "'", "“": '"', "”": '"',
        "\u00A0": " ", "\u200B": "", "🔺": "[HIGH]", "🟡": "[MED]", "🔻": "[LOW]"
    }
    for old, new in replacements.items():
        text = text.replace(old, new)

    text = ''.join(c for c in text if unicodedata.category(c)[0] != 'C')
    text = ''.join(c for c in text if ord(c) < 65536)
    return text.strip()


def write_section(pdf, title, items):
    pdf.set_font("DejaVu", "B", 12)
    pdf.set_text_color(0, 0, 128)  # Темно-синий
    pdf.multi_cell(0, 8, clean_text(title))
    pdf.set_draw_color(180, 180, 180)
    pdf.set_line_width(0.5)
    pdf.cell(0, 1, "", ln=True, border="T")
    pdf.ln(3)

    pdf.set_font("DejaVu", "", 10)
    pdf.set_text_color(0, 0, 0)

    for item in items:
        item = clean_text(item)
        if not item:
            continue

        # Автоматическая разбивка по абзацам, без агрессивного переноса слов
        paragraphs = textwrap.wrap(item, width=100)  # мягкий перенос
        if not paragraphs:
            continue

        # Первый абзац — с маркером
        pdf.multi_cell(0, 6, f"• {paragraphs[0]}", ln=True)
        # Остальные — как продолжение (без маркера)
        for line in paragraphs[1:]:
            pdf.multi_cell(0, 6, f"  {line}", ln=True)

        pdf.ln(2)

    pdf.ln(4)


def generate_pdf(results, filename="output/last_report.pdf"):
    chart_path = "output/chart.png"
    generate_bar_chart(results, chart_path)

    high, medium, low = categorize_results(results)

    pdf = UnicodePDF()
    pdf.add_page()

    # Заголовок
    pdf.set_font("DejaVu", "B", 14)
    pdf.set_text_color(0, 0, 0)
    pdf.multi_cell(0, 10, "Отчет по приоритизации требований (метод MoSCoW)", align='C')
    pdf.ln(10)

    # Диаграмма
    pdf.set_font("DejaVu", "", 10)
    pdf.multi_cell(0, 8, "Итоговая диаграмма:")
    try:
        pdf.image(chart_path, x=10, y=pdf.get_y(), w=190)
        pdf.ln(100 if len(results) <= 15 else 110)
    except:
        pdf.multi_cell(0, 8, "[Диаграмма не доступна]", ln=True)
        pdf.ln(10)

    # Секции с приоритетами
    write_section(pdf, "🔺 Высокий приоритет (реализовать в первую очередь):", high)
    write_section(pdf, "🟡 Средний приоритет (реализовать при наличии ресурсов):", medium)
    write_section(pdf, "🔻 Низкий приоритет (может быть отложен):", low)

    os.makedirs(os.path.dirname(filename), exist_ok=True)
    pdf.output(filename)
