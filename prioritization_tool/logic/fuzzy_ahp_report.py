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



def generate_bar_chart(results, output_path, title):
    names = list(results.keys())
    # Извлекаем только значения score из вложенных словарей
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
    """Универсальная классификация для обоих типов"""
    if not results:
        return [], [], []

    # Проверяем тип первого элемента
    is_type1 = isinstance(next(iter(results.values())), dict)

    if is_type1:
        sorted_items = sorted(results.items(), key=lambda x: -x[1]['score'])
        high = [(k, v) for k, v in sorted_items if v['score'] >= 0.6]
        medium = [(k, v) for k, v in sorted_items if 0.4 <= v['score'] < 0.6]
        low = [(k, v) for k, v in sorted_items if v['score'] < 0.4]
    else:
        sorted_items = sorted(results.items(), key=lambda x: -x[1])
        high = [(k, {'score': v, 'comment': ''}) for k, v in sorted_items if v >= 0.6]
        medium = [(k, {'score': v, 'comment': ''}) for k, v in sorted_items if 0.4 <= v < 0.6]
        low = [(k, {'score': v, 'comment': ''}) for k, v in sorted_items if v < 0.4]

    return high, medium, low


def write_section(pdf, title, items):
    """Обновленная функция для вывода секций"""
    pdf.set_font("DejaVu", "B", 12)
    pdf.set_text_color(0, 0, 128)
    safe_multicell(pdf, title, width=90, cell_height=7)
    pdf.ln(3)

    pdf.set_font("DejaVu", "", 9)
    pdf.set_text_color(0, 0, 0)

    for name, data in items:
        line = f"• {name} — Приоритет: {data['score']:.4f}"
        safe_multicell(pdf, line, width=90)
        pdf.ln(2)
    pdf.ln(4)


def generate_single_report(results, method_name, filename):
    """Генерация отчета для одного метода (поддержка Type-1 и Type-2)"""

    # Приводим к единому виду: всегда словарь {альтернатива: {'score': число, 'comment': текст}}
    if not isinstance(next(iter(results.values())), dict):
        results = {k: {'score': v, 'comment': ''} for k, v in results.items()}

    chart_path = f"output/charts/ahp_{method_name.lower().replace(' ', '_')}.png"
    generate_bar_chart(results, chart_path, f"Fuzzy AHP {method_name}")

    # Классификация по приоритету
    high, med, low = classify(results)

    pdf = UnicodePDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Заголовок
    pdf.set_font("DejaVu", "B", 14)
    safe_multicell(pdf, f"Отчет Fuzzy AHP ({method_name})", width=100, cell_height=8)
    pdf.ln(10)

    # Вставляем диаграмму
    try:
        if pdf.h - pdf.y > 100:
            pdf.image(chart_path, x=10, y=pdf.get_y(), w=180)
            pdf.ln(110)
        else:
            pdf.add_page()
            pdf.image(chart_path, x=10, y=20, w=180)
            pdf.ln(110)
    except Exception as e:
        safe_multicell(pdf, f"[Ошибка загрузки диаграммы: {str(e)}]")
        pdf.ln(10)

    # Секции с результатами
    write_section(pdf, "Высокий приоритет (≥ 0.6):", high)
    write_section(pdf, "Средний приоритет (0.4-0.6):", med)
    write_section(pdf, "Низкий приоритет (< 0.4):", low)

    # Таблица итогов
    pdf.ln(5)
    pdf.set_font("DejaVu", "B", 12)
    pdf.cell(0, 10, "Итоговые приоритеты:", ln=True)
    pdf.ln(5)

    from fpdf import FPDF
    # Строим простую таблицу
    col_widths = [100, 30, 60]  # Альтернатива / Приоритет / Комментарий
    pdf.set_font("DejaVu", "", 11)
    pdf.cell(col_widths[0], 8, "Альтернатива", border=1)
    pdf.cell(col_widths[1], 8, "Приоритет", border=1)
    pdf.cell(col_widths[2], 8, "Комментарий", border=1)
    pdf.ln()

    for alt, data in results.items():
        pdf.cell(col_widths[0], 8, alt, border=1)
        pdf.cell(col_widths[1], 8, f"{data['score']:.4f}", border=1)
        pdf.cell(col_widths[2], 8, data['comment'], border=1)
        pdf.ln()

    # Сохраняем PDF
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    pdf.output(filename)



def generate_combined_report(results_type1, results_type2, filename="output/fuzzy_ahp_report.pdf"):
    """Переименованная основная функция (бывшая generate_report)"""
    # Генерация графиков
    chart_type1 = "output/charts/ahp_type1.png"
    chart_type2 = "output/charts/ahp_type2.png"

    generate_bar_chart(results_type1, chart_type1, "Fuzzy AHP Type-1 (Приоритеты альтернатив)")
    generate_bar_chart(results_type2, chart_type2, "Fuzzy AHP Type-2 (Веса критериев)")

    # Классификация результатов
    high_t1, med_t1, low_t1 = classify(results_type1)
    high_t2, med_t2, low_t2 = classify(results_type2)

    # Создание PDF
    pdf = UnicodePDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Заголовок отчета
    pdf.set_font("DejaVu", "B", 14)
    safe_multicell(pdf, "Комбинированный отчет Fuzzy AHP", width=100, cell_height=8)
    pdf.ln(10)

    # Раздел Type-1
    pdf.set_font("DejaVu", "B", 12)
    safe_multicell(pdf, "Fuzzy AHP Type-1 (Приоритеты альтернатив)", width=100)
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
    safe_multicell(pdf, "Fuzzy AHP Type-2 (Веса критериев)", width=100)
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

    os.makedirs(os.path.dirname(filename), exist_ok=True)
    pdf.output(filename)