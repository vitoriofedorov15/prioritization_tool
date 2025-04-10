import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from prioritization_tool.logic.MoSCoW import parser, moscow, moscow_report
from prioritization_tool.logic.Kano import kano, kano_report
import os



class PrioritizationTool:
    def __init__(self, root):
        self.root = root
        self.root.title("Система приоритизации требований")
        self.root.geometry("1000x720")
        self.root.resizable(False, False)

        self.requirements_path = None
        self.weights_path = None
        self.kano_csv_path = None
        self.topsis_file_path = None
        self.fuzzy_type1_path = None
        self.topsis_intuitionistic_path = None
        self.fuzzy_delphi_type2_path = None
        self.delphi_intuitionistic_path = None
        self.ahp_type1_criteria_path = None
        self.ahp_type1_alternatives_path = None
        self.ahp_type1_weights_path = None
        self.ahp_type2_path  = None

        self.setup_style()
        self.show_method_selection_screen()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def setup_style(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("TButton",
                        font=("Segoe UI", 13, "bold"),
                        padding=12,
                        foreground="#ffffff",
                        background="#2980b9")

        style.map("TButton",
                  foreground=[('active', '#ffffff')],
                  background=[('active', '#1abc9c')])

        style.configure("Header.TLabel",
                        font=("Segoe UI", 26, "bold"),
                        foreground="#2c3e50")
        style.configure("Exit.TButton",
                        font=("Segoe UI", 12, "bold"),
                        padding=10,
                        foreground="#ffffff",
                        background="#c0392b")

        style.map("Exit.TButton",
                  background=[('active', '#e74c3c')])

        style.configure("Info.TLabel",
                        font=("Segoe UI", 12),
                        foreground="#2f3640",
                        wraplength=800,
                        justify="center")

        style.configure("Status.TLabel",
                        font=("Segoe UI", 12),
                        foreground="#27ae60")

    def setup_style(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("TButton",
                        font=("Segoe UI", 13, "bold"),
                        padding=12,
                        foreground="#ffffff",
                        background="#2980b9")

        style.map("TButton",
                  foreground=[('active', '#ffffff')],
                  background=[('active', '#1abc9c')])

        style.configure("Header.TLabel",
                        font=("Segoe UI", 26, "bold"),
                        foreground="#2c3e50")

        style.configure("Info.TLabel",
                        font=("Segoe UI", 12),
                        foreground="#2f3640",
                        wraplength=800,
                        justify="center")

        style.configure("Status.TLabel",
                        font=("Segoe UI", 12),
                        foreground="#27ae60")

        # Отдельный стиль для кнопки выхода
        style.configure("Exit.TButton",
                        font=("Segoe UI", 10, "bold"),
                        padding=6,
                        foreground="#ffffff",
                        background="#7f8c8d")

        style.map("Exit.TButton",
                  background=[('active', '#95a5a6')])

    def show_method_selection_screen(self):
        self.clear_window()

        frame = ttk.Frame(self.root, padding=40)
        frame.pack(fill="both", expand=True)

        ttk.Label(
            frame,
            text="Система автоматической приоритизации требований",
            style="Header.TLabel"
        ).pack(pady=(0, 30))

        description = (
            "Данное приложение предназначено для автоматизированной приоритизации требований "
            "в проектах разработки программного обеспечения. Оно помогает определить, какие "
            "требования стоит реализовать в первую очередь, а какие можно отложить.\n\n"
            "В системе реализованы 6 методов анализа требований:\n"
            "• MoSCoW — быстрое разделение по критичности\n"
            "• Кано — учет восприятия пользователей\n"
            "• TOPSIS — метод ближайшего идеала\n"
            "• Fuzzy TOPSIS — расширенный метод с нечёткими данными\n"
            "• Fuzzy Delphi — консенсусная экспертная оценка\n"
            "• Fuzzy AHP — иерархическое ранжирование с нечёткостью\n\n"
            "Выберите подходящий метод и загрузите ваши данные для анализа:"
        )

        ttk.Label(frame, text=description, style="Info.TLabel").pack(pady=(0, 40))

        # Фрейм с кнопками методов
        methods_frame = ttk.Frame(frame)
        methods_frame.pack()

        buttons = [
            ("📊 Метод MoSCoW", self.show_moscow_screen),
            ("📈 Метод Кано", self.show_kano_screen),
            ("📐 Метод TOPSIS", self.show_topsis_screen),
            ("🌫️ Fuzzy TOPSIS", self.show_fuzzy_topsis_screen),
            ("⚙️ Fuzzy Delphi", self.show_fuzzy_delphi_screen),
            ("📑 Fuzzy AHP", self.show_fuzzy_ahp_screen)
        ]

        for i, (text, command) in enumerate(buttons):
            btn = ttk.Button(methods_frame, text=text, command=command)
            btn.grid(row=i // 2, column=i % 2, padx=20, pady=12, ipadx=10, ipady=6, sticky="ew")
            methods_frame.columnconfigure(i % 2, weight=1)

        # Отдельный фрейм для кнопки "Выход"
        exit_frame = ttk.Frame(frame)
        exit_frame.pack(anchor="se", pady=(30, 0))  # Привязка к правому нижнему краю

        exit_btn = ttk.Button(exit_frame,
                              text="❌ Завершить программу",
                              command=self.root.quit,
                              style="Exit.TButton")
        exit_btn.pack(side="right", padx=10, pady=10)

    def show_moscow_screen(self):
        self.clear_window()
        frame = ttk.Frame(self.root, padding=20)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="MoSCoW Prioritization", style="Header.TLabel").pack(pady=(0, 10))

        description = (
            "Файл требований (CSV): должен содержать 4 столбца:\n"
            "  - Альтернатива\n"
            "  - Критерий\n"
            "  - Стейкхолдер\n"
            "  - Оценка (например: \"100% M\" или \"60% S, 40% C\")\n\n"
            "Первая строка в каждом файле - названия столбцов в кавычках, разделитель - запятая.\n"
            "Значение, соответствующее каждому столбцу, должно быть заключено в кавычки, разделитель - запятая.\n"
            "Разрешены только такие комбинации оценок: M/S, S/C, C/W.\n\n"
            "Файл весов (CSV): должен содержать столбцы \"Стейкхолдер\" и \"Вес\" :\n"
            "Например \"S1\",\"1.5\""
        )

        msg = tk.Message(frame, text=description, width=800, font=("Segoe UI", 10), justify="left")
        msg.pack(pady=(0, 15))

        ttk.Button(frame, text="📁 Загрузить файл требований", command=self.load_requirements).pack(pady=4)
        ttk.Button(frame, text="📁 Загрузить файл весов стейкхолдеров", command=self.load_weights).pack(pady=4)
        ttk.Button(frame, text="✅ Выполнить приоритизацию (MoSCoW)", command=self.run_moscow).pack(pady=12)

        ttk.Button(frame, text="🔙 Вернуться назад", command=self.show_method_selection_screen).pack(pady=10)

        self.status = ttk.Label(frame, text="", style="Status.TLabel")
        self.status.pack()

    def show_kano_screen(self):
        self.clear_window()
        frame = ttk.Frame(self.root, padding=20)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Kano Model Prioritization", style="Header.TLabel").pack(pady=(0, 10))

        description = (
            "Файл требований (CSV): должен содержать 5 столбцов:\n"
            "  - Альтернатива\n"
            "  - Стейкхолдер\n"
            "  - Функциональный ответ (например: \"Must-be\", \"Attractive\")\n"
            "  - Дисфункциональный ответ (например: \"Indifferent\", \"Reverse\")\n"
            "  - Вес (например: \"1.0\", \"1.5\")\n\n"
            "Первая строка в каждом файле — названия столбцов в кавычках, разделитель — запятая.\n"
            "Значение, соответствующее каждому столбцу, должно быть заключено в кавычки, разделитель — запятая.\n"
            "Допустимые категории ответов: Must-be, One-dimensional, Attractive, Indifferent, Reverse, Questionable.\n\n"
        )

        msg = tk.Message(frame, text=description, width=800, font=("Segoe UI", 10), justify="left")
        msg.pack(pady=(0, 15))

        ttk.Button(frame, text="📁 Загрузить CSV-файл для Кано", command=self.load_kano_file).pack(pady=5)
        ttk.Button(frame, text="✅ Выполнить приоритизацию (Кано)", command=self.run_kano).pack(pady=12)
        ttk.Button(frame, text="🔙 Вернуться назад", command=self.show_method_selection_screen).pack(pady=10)

        self.status = ttk.Label(frame, text="", style="Status.TLabel")
        self.status.pack()

    def load_kano_file(self):
        path = filedialog.askopenfilename(title="Выберите CSV-файл с анкетой Кано", filetypes=[("CSV файлы", "*.csv")])
        if path:
            self.kano_csv_path = path
            self.status.config(text="✅ Загружен файл для модели Кано")

    def run_kano(self):
        if not self.kano_csv_path:
            messagebox.showwarning("⚠️ Внимание", "Пожалуйста, загрузите CSV-файл перед расчетом.")
            return

        try:
            results = kano.process_kano_csv(self.kano_csv_path)
            kano_report.generate_kano_report(results, filename="output/kano_report.pdf")
            self.status.config(text="📄 Расчет завершен. Отчет сохранен в output/kano_report.pdf")
        except Exception as e:
            messagebox.showerror("❌ Ошибка", str(e))

    def show_topsis_screen(self):
        self.clear_window()
        frame = ttk.Frame(self.root, padding=20)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="TOPSIS Prioritization", style="Header.TLabel").pack(pady=(0, 10))

        description = (
            "Файл требований (CSV): должен содержать численные оценки альтернатив по критериям и вес стейкхолдера:\n"
            "  - Альтернатива (например: \"Авторизация через соцсети\")\n"
            "  - Безопасность (например: \"7\")\n"
            "  - Удобство (например: \"8\")\n"
            "  - Бизнес-ценность (например: \"6\")\n"
            "  - Вес стейкхолдера (например: \"0.3\")\n\n"
            "Первая строка в каждом файле — названия столбцов в кавычках, разделитель — запятая.\n"
            "Значение, соответствующее каждому столбцу, должно быть заключено в кавычки, разделитель — запятая.\n"
            "Все числовые значения должны быть заданы в единой шкале (например, от 1 до 10).\n\n"
        )

        msg = tk.Message(frame, text=description, width=800, font=("Segoe UI", 10), justify="left")
        msg.pack(pady=(0, 15))

        ttk.Button(frame, text="📁 Загрузить CSV-файл (включая веса стейкхолдеров)", command=self.load_topsis_file).pack(
            pady=5)
        ttk.Button(frame, text="✅ Выполнить приоритизацию (TOPSIS)", command=self.run_topsis).pack(pady=12)
        ttk.Button(frame, text="🔙 Вернуться назад", command=self.show_method_selection_screen).pack(pady=10)

        self.status = ttk.Label(frame, text="", style="Status.TLabel")
        self.status.pack()

    def load_topsis_file(self):
        path = filedialog.askopenfilename(title="Выберите CSV-файл для TOPSIS", filetypes=[("CSV файлы", "*.csv")])
        if path:
            self.topsis_file_path = path
            self.status.config(text="✅ Файл загружен: " + os.path.basename(path))

    def load_requirements(self):
        path = filedialog.askopenfilename(title="Выберите CSV с требованиями", filetypes=[("CSV файлы", "*.csv")])
        if path:
            self.requirements_path = path
            self.status.config(text="✅ Файл требований загружен.")

    def load_weights(self):
        path = filedialog.askopenfilename(title="Выберите CSV с весами", filetypes=[("CSV файлы", "*.csv")])
        if path:
            self.weights_path = path
            self.status.config(text="✅ Весы стейкхолдеров загружены.")

    def run_moscow(self):
        if not self.requirements_path or not self.weights_path:
            messagebox.showwarning("⚠️ Внимание", "Пожалуйста, загрузите оба CSV-файла перед расчетом.")
            return

        try:
            req_data = parser.load_requirements(self.requirements_path)
            weights = parser.load_weights(self.weights_path)
            results = moscow.calculate(req_data, weights)
            moscow_report.generate_pdf(results, filename="output/moscow_report.pdf")
            self.status.config(text="📄 Расчёт завершён. Отчёт сохранён в output/moscow_report.pdf")
        except Exception as e:
            messagebox.showerror("❌ Ошибка", str(e))

    def run_topsis(self):
        if not self.topsis_file_path:
            messagebox.showwarning("⚠️ Внимание", "Сначала загрузите CSV-файл.")
            return

        try:
            from prioritization_tool.logic.TOPSIS import topsis_report
            from prioritization_tool.logic.TOPSIS import topsis
            results = topsis.process_topsis(self.topsis_file_path)
            topsis_report.generate_topsis_report(results)
            self.status.config(text="📄 Отчет TOPSIS сохранен в output/topsis_report.pdf")
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def show_fuzzy_topsis_screen(self):
        self.clear_window()
        frame = ttk.Frame(self.root, padding=20)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Нечеткая приоритизация требований (Fuzzy TOPSIS)", style="Header.TLabel").pack(
            pady=(0, 10))

        container = ttk.Frame(frame)
        container.pack(fill="both", expand=True)

        # Левая колонка — Fuzzy TOPSIS Type-1
        left = ttk.Frame(container, padding=10)
        left.pack(side="left", fill="both", expand=True)

        ttk.Label(left, text="Fuzzy TOPSIS Type-1 (трапециевидные числа)", style="SubHeader.TLabel").pack(pady=(0, 5))

        msg1 = tk.Message(
            left,
            text=(
                "Файл требований (CSV): должен содержать текстовые оценки по критериям:\n"
                "  - Альтернатива (например: \"Авторизация через соцсети\")\n"
                "  - Один или несколько критериев с оценками из шкалы (например: \"Высоко\", \"Средне\")\n\n"
                "Первая строка в каждом файле — названия столбцов в кавычках, разделитель — запятая.\n"
                "Все значения должны быть заключены в кавычки.\n"
                "Допустимые текстовые оценки определяются загруженной шкалой (например: \"Очень низко\", \"Низко\", \"Средне\", \"Высоко\", \"Очень высоко\")\n\n"
                "Пример строки:\n"
                "  \"Авторизация через соцсети\",\"Высоко\",\"Средне\",\"Низко\"\n"
                "  \"Двухфакторная аутентификация\",\"Очень высоко\",\"Высоко\",\"Средне\"\n\n"
                "Для работы необходимо загрузить файл шкалы соответствия текстовых оценок трапециевидным числам"
            ),
            width=380,
            font=("Segoe UI", 8),
            justify="left"
        )

        msg1.pack(pady=(0, 5))
        msg_scale = tk.Message(
            left,
            text=(
                "Файл шкалы (CSV): должен содержать соответствие между текстовыми оценками и трапециевидными числами:\n"
               "Пример файла:\n"
                "\"Очень низко\",\"(1,1,2,3)\"\n"
                "\"Низко\",\"(2,3,4,5)\"\n"
                "\"Средне\",\"(4,5,6,7)\"\n"
                "..."
            ),
            width=380,
            font=("Segoe UI", 8),
            justify="left"
        )
        msg_scale.pack(pady=(0, 5))
        ttk.Button(left, text="📁 Загрузить файл Type-1", command=self.load_fuzzy_type1_file).pack(pady=5)

        # Правая колонка — Intuitionistic TOPSIS
        right = ttk.Frame(container, padding=10)
        right.pack(side="left", fill="both", expand=True)

        ttk.Label(right, text="Intuitionistic Fuzzy TOPSIS", style="SubHeader.TLabel").pack(pady=(0, 5))

        msg2 = tk.Message(
            right,
            text=(
                "ФОРМАТ ВХОДНОГО ФАЙЛА ДЛЯ INTUITIONISTIC FUZZY TOPSIS (CSV)\n\n"
                "Обязательные требования:\n"
                "• Первая строка - названия столбцов в кавычках\n"
                "• Первый столбец - \"Альтернатива\" (названия требований)\n"
                "• Последующие столбцы - критерии оценки\n"
                "• Все значения - текстовые оценки в кавычках; "
                "• Разделитель - запятая\n\n"
                "ДОПУСТИМЫЕ ТЕКСТОВЫЕ ОЦЕНКИ: "
                "• Очень важно, и я уверен(a) "
                "• Очень важно, но есть сомнения "
                "• Важно, и я уверен(a) "
                "• Важно, но есть сомнения "
                "• Средне, но я уверен(a) "
                "• Средне, и есть сомнения "
                "• Маловажно, но я уверен(a) "
                "• Маловажно, и есть сомнения "
                "• Неважно, но я уверен(a) "
                "• Неважно, и есть сомнения "
                "ПРИМЕР ФАЙЛА:\n"
                "\"Альтернатива\",\"Безопасность\",\"Удобство\"\n"
                "\"Авторизация\",\"Важно, и я уверен(a)\",\"Средне, но есть сомнения\"\n"
                "\"Резервное копирование\",\"Очень важно, но есть сомнения\",\"Маловажно, и я уверен(a)\""
            ),
            width=380,
            font=("Segoe UI", 8),
            justify="left"
        )

        msg2.pack(pady=(0, 5))
        msg_ifs_scale = tk.Message(
            right,
            text=(
                "ФОРМАТ ФАЙЛА ШКАЛЫ ДЛЯ INTUITIONISTIC FUZZY TOPSIS (CSV):\n\n"
                "Обязательные столбцы (точное соответствие названий):\n"
                "1. \"Оценка эксперта\" - текстовая оценка\n"
                "2. \"Степень принадлежности\" - число 0.0-1.0\n"
                "3. \"Степень непринадлежности\" - число 0.0-1.0\n"
                "4. \"Степень неопределённости\" - число 0.0-1.0\n\n"
                "Допустимые текстовые оценки перечислены выше в необходимом порядке"
                "ТРЕБОВАНИЯ:\n"
                "1. Все значения в кавычках "
                "2. Разделитель - запятая "
                "3. Первая строка - заголовки столбцов "
                "4. Сумма (μ + ν + π) ≤ 1.0 для каждой строки\n"
                "ПРИМЕР СОДЕРЖИМОГО ФАЙЛА ШКАЛЫ:\n"
                "\"Оценка эксперта\",\"Степ.принадлеж.\",\"Степ.непринадл.\",\"Степ.неопред.\"\n"
                "\"Очень важно, и я уверен(a)\",\"0.9\",\"0.05\",\"0.05\"\n"
            ),
            width=380,
            font=("Segoe UI", 8),
            justify="left"
        )
        msg_ifs_scale.pack(pady=(10, 5))
        ttk.Button(right, text="📁 Загрузить файл Intuitionistic", command=self.load_intuitionistic_file).pack(pady=5)
        # Кнопка загрузки шкалы
        ttk.Button(left, text="📁 Загрузить шкалу значений", command=self.load_fuzzy_scale_file).pack(pady=(10, 5))
        ttk.Button(right, text="📁 Загрузить шкалу IFS", command=self.load_ifs_scale_file).pack(pady=(10, 5))
        # Кнопки запуска и возврата

        self.status = ttk.Label(frame, text="", style="Status.TLabel")
        self.status.pack()

        ttk.Button(frame, text="✅ Сформировать отчёт", command=self.run_fuzzy_topsis).pack(pady=(15, 5))
        ttk.Button(frame, text="🔙 Назад", command=self.show_method_selection_screen).pack(pady=(0, 10))



    def load_fuzzy_type1_file(self):
        path = filedialog.askopenfilename(
            title="Загрузите файл для Fuzzy TOPSIS Type-1",
            filetypes=[("CSV файлы", "*.csv")]
        )
        if path:
            self.fuzzy_type1_path = path
            self.status.config(text="✅ Загружен файл Type-1: " + os.path.basename(path))

    def load_ifs_scale_file(self):
        path = filedialog.askopenfilename(
            title="Загрузите шкалу значений для Intuitionistic Fuzzy TOPSIS",
            filetypes=[("CSV файлы", "*.csv")]
        )
        if path:
            self.ifs_scale_path = path
            self.status.config(text="✅ Загружена шкала IFS: " + os.path.basename(path))

    def load_intuitionistic_file(self):
        path = filedialog.askopenfilename(
            title="Загрузите файл для Intuitionistic TOPSIS",
            filetypes=[("CSV файлы", "*.csv")]
        )
        if path:
            self.topsis_intuitionistic_path = path
            self.status.config(text="✅ Загружен файл Intuitionistic: " + os.path.basename(path))
    def load_fuzzy_scale_file(self):
        path = filedialog.askopenfilename(
            title="Загрузите файл шкалы значений для Fuzzy TOPSIS",
            filetypes=[("CSV файлы", "*.csv")]
        )
        if path:
            self.fuzzy_scale_path = path
            self.status.config(text="✅ Загружена шкала значений: " + os.path.basename(path))

    def run_fuzzy_topsis(self):
        if not self.fuzzy_type1_path or not hasattr(self, 'fuzzy_scale_path'):
            messagebox.showwarning("⚠️ Внимание", "Загрузите файлы для Fuzzy TOPSIS")
            return

        if not self.topsis_intuitionistic_path or not hasattr(self, 'ifs_scale_path'):
            messagebox.showwarning("⚠️ Внимание", "Загрузите файлы для Intuitionistic TOPSIS")
            return

        try:
            from logic.fuzzy_topsis import calculate_fuzzy_topsis
            from logic.intuitionistic_topsis import calculate_ifs_topsis
            from logic.fuzzy_topsis_report import generate_combined_report

            results_type1 = calculate_fuzzy_topsis(self.fuzzy_type1_path, self.fuzzy_scale_path)
            results_ifs = calculate_ifs_topsis(self.topsis_intuitionistic_path, self.ifs_scale_path)

            generate_combined_report(
                fuzzy_results=results_type1,  # Исправлено имя параметра
                ifs_results=results_ifs
            )

            self.status.config(text="📄 Отчет сохранен: output/fuzzy_topsis_report.pdf")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка обработки: {str(e)}")


    def show_fuzzy_delphi_screen(self):
        self.clear_window()
        frame = ttk.Frame(self.root, padding=20)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Метод нечеткого Делфи (Fuzzy Delphi)", style="Header.TLabel").pack(pady=(0, 10))

        container = ttk.Frame(frame)
        container.pack(fill="both", expand=True)

        # Левая колонка — Fuzzy Delphi Type-2
        left = ttk.Frame(container, padding=10)
        left.pack(side="left", fill="both", expand=True)

        ttk.Label(left, text="Fuzzy Delphi Type-2 (IT2FS)", style="SubHeader.TLabel").pack(pady=(0, 5))

        msg1 = tk.Message(
            left,
            text=("Файл требований (CSV): должен содержать словесные оценки с указанием степени уверенности:\n"
        "  - Альтернатива\n"
        "  - Эксперт\n"
        "  - Один или несколько критериев (например: Безопасность, Удобство)\n"
        "  - Вес эксперта\n\n"
        "Первая строка в каждом файле — названия столбцов в кавычках, разделитель — запятая.\n"
        "Значение, соответствующее каждому столбцу, должно быть заключено в кавычки.\n"
        "Оценки должны быть в формате: \"Степень уверенности – Лингвистическая оценка\"\n"
        "Например: \"Высокая уверенность – Высокая\"\n\n"
        "Пример строки:\n"
        "\"Авторизация через соцсети\",\"Эксперт 1\",\"Высокая уверенность – Высокая\",\"Средняя уверенность – Средняя\",\"Низкая уверенность – Низкая\",\"0.6\""
     ),
            width=380,
            justify="left"
        )
        msg1.pack(pady=(0, 5))
        ttk.Button(left, text="📁 Загрузить файл Type-2", command=self.load_fuzzy_delphi_file).pack(pady=5)

        # Правая колонка — Delphi Intuitionistic
        right = ttk.Frame(container, padding=10)
        right.pack(side="left", fill="both", expand=True)

        ttk.Label(right, text="Delphi Intuitionistic (IFS)", style="SubHeader.TLabel").pack(pady=(0, 5))

        msg2 = tk.Message(
            right,
            text=(
                "Файл требований (CSV): должен содержать оценки по критериям в виде троек (μ, ν, π):\n"
        "  - Альтернатива\n"
        "  - Эксперт\n"
        "  - Один или несколько критериев (например: Безопасность, Удобство)\n"
        "  - Вес эксперта\n\n"
        "Первая строка в каждом файле — названия столбцов в кавычках, разделитель — запятая.\n"
        "Значение, соответствующее каждому столбцу, должно быть заключено в кавычки.\n"
        "Оценки должны быть в формате: \"(μ, ν, π)\", где каждое значение от 0 до 1.\n"
        "Например: \"(0.7, 0.2, 0.1)\"\n\n"
        "Пример строки:\n"
        "\"Авторизация через соцсети\",\"Эксперт 1\",\"(0.7, 0.2, 0.1)\",\"(0.6, 0.3, 0.1)\",\"(0.5, 0.4, 0.1)\",\"0.6\""
    ),
            width=380,
            justify="left"
        )
        msg2.pack(pady=(0, 5))
        ttk.Button(right, text="📁 Загрузить файл IFS", command=self.load_delphi_ifs_file).pack(pady=5)

        # Кнопки запуска и возврата
        ttk.Button(frame, text="✅ Сформировать отчёт", command=self.run_fuzzy_delphi).pack(pady=(15, 5))
        ttk.Button(frame, text="🔙 Назад", command=self.show_method_selection_screen).pack(pady=(0, 10))

        self.status = ttk.Label(frame, text="", style="Status.TLabel")
        self.status.pack()

    def load_fuzzy_delphi_file(self):
        path = filedialog.askopenfilename(title="Загрузите файл Fuzzy Delphi Type-2",
                                          filetypes=[("CSV файлы", "*.csv")])
        if path:
            self.fuzzy_delphi_path = path
            self.status.config(text="✅ Загружен файл Type-2: " + os.path.basename(path))

    def load_delphi_ifs_file(self):
        path = filedialog.askopenfilename(title="Загрузите файл Delphi Intuitionistic",
                                          filetypes=[("CSV файлы", "*.csv")])
        if path:
            self.delphi_ifs_path = path
            self.status.config(text="✅ Загружен файл IFS: " + os.path.basename(path))

    def run_fuzzy_delphi(self):
        if not self.fuzzy_delphi_path or not self.delphi_ifs_path:
            messagebox.showwarning("⚠️ Внимание", "Загрузите оба CSV-файла перед запуском анализа.")
            return

        try:
            from logic import fuzzy_delphi, delphi_report

            results_type2 = fuzzy_delphi.process_fuzzy_delphi(self.fuzzy_delphi_path)
            results_ifs = fuzzy_delphi.process_delphi_ifs(self.delphi_ifs_path)

            delphi_report.generate_combined_report(results_type2, results_ifs)
            self.status.config(text="📄 Объединённый отчет создан: output/fuzzy_delphi_report.pdf")

        except Exception as e:
            messagebox.showerror("Ошибка", str(e))


    def show_fuzzy_ahp_screen(self):
        self.clear_window()
        frame = ttk.Frame(self.root, padding=20)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Нечеткая приоритизация требований (Fuzzy AHP)", style="Header.TLabel").pack(pady=(0, 10))

        container = ttk.Frame(frame)
        container.pack(fill="both", expand=True)

        # Левая колонка — Fuzzy AHP Type-1
        left = ttk.Frame(container, padding=10)
        left.pack(side="left", fill="both", expand=True)

        ttk.Label(left, text="Fuzzy AHP Type-1", style="SubHeader.TLabel").pack(pady=(0, 5))

        msg1 = tk.Message(
            left,
            text=(

        "Требования должны быть представлены в виде трёх отдельных CSV-файлов:\n"
        "1. Оценки попарных сравнений критериев:\n"
        "  - Первая строка — названия критериев (заголовки)\n"
        "  - Каждая последующая строка — оценки сравнений одного критерия с остальными\n"
        "  - Значения — в формате \"3\" или \"1/3\" из шкалы \"1\", \"2\", \"3\", \"5\", \"7\", \"9\", \"1/2\", \"1/3\", \"1/5\", \"1/7\", \"1/9\"\n"
        "2. Оценки альтернатив по критериям:\n"
        "  - Столбцы: Альтернатива, Эксперт, Критерий 1, Критерий 2, ...\n"
        "  - Значения — тройки вида (a, b, c), например: \"(1.5, 2.0, 2.5)\"\n"
        "3. Весовые коэффициенты экспертов:\n"
        "  - Два столбца: Эксперт, Вес\n"
        "  - Вес — число от 0 до 1, сумма всех весов должна равняться 1.0\n"
        "Первая строка в каждом файле — названия столбцов в кавычках, разделитель — запятая. Значение, соответствующее каждому столбцу, должно быть заключено в кавычки."

            ),
            width=420,
            justify="left"
        )
        msg1.pack(pady=(0, 5))

        ttk.Button(left, text="📁 Загрузить критерии", command=self.load_fuzzy_ahp_criteria_file).pack(pady=3)
        ttk.Button(left, text="📁 Загрузить альтернативы", command=self.load_fuzzy_ahp_alternatives_file).pack(pady=3)
        ttk.Button(left, text="📁 Загрузить веса экспертов", command=self.load_fuzzy_ahp_weights_file).pack(pady=3)

        # Правая колонка — Fuzzy AHP Type-2
        right = ttk.Frame(container, padding=10)
        right.pack(side="left", fill="both", expand=True)

        ttk.Label(right, text="Fuzzy AHP Type-2", style="SubHeader.TLabel").pack(pady=(0, 5))

        msg2 = tk.Message(
            right,
            text=(
        "Файл требований (CSV): должен содержать оценки попарных сравнений критериев от нескольких экспертов:\n"
        "  - Столбцы: Эксперт, Вес, Критерий 1 > Критерий 2, Критерий 1 > Критерий 3, ...\n"
        "  - Значения — словесные оценки предпочтения: \"Одинаково\", \"Слабо\", \"Умеренно\", \"Сильно\", \"Абсолютно\"\n"
        "  - Все значения должны быть заключены в кавычки\n\n"
        "Пример строки:\n"
        "  \"Эксперт 1\",\"0.3\",\"Слабо\",\"Одинаково\",\"Сильно\",... \n"
    ),
            width=380,
            justify="left"
        )
        msg2.pack(pady=(0, 5))

        ttk.Button(right, text="📁 Загрузить файл Type-2", command=self.load_fuzzy_ahp_type2_file).pack(pady=5)

        # Кнопки запуска и возврата
        ttk.Button(frame, text="✅ Сформировать отчёт", command=self.run_fuzzy_ahp).pack(pady=(15, 5))
        ttk.Button(frame, text="🔙 Назад", command=self.show_method_selection_screen).pack(pady=(0, 10))

        self.status = ttk.Label(frame, text="", style="Status.TLabel")
        self.status.pack()

    def load_fuzzy_ahp_criteria_file(self):
        path = filedialog.askopenfilename(
            title="Загрузите файл с матрицей попарных сравнений критериев (Fuzzy AHP Type-1)",
            filetypes=[("CSV файлы", "*.csv")])
        if path:
            self.ahp_type1_criteria_path = path
            self.status.config(text="✅ Загружен файл критериев: " + os.path.basename(path))

    def load_fuzzy_ahp_alternatives_file(self):
        path = filedialog.askopenfilename(title="Загрузите файл с оценками альтернатив (Fuzzy AHP Type-1)",
                                          filetypes=[("CSV файлы", "*.csv")])
        if path:
            self.ahp_type1_alternatives_path = path
            self.status.config(text="✅ Загружен файл альтернатив: " + os.path.basename(path))

    def load_fuzzy_ahp_weights_file(self):
        path = filedialog.askopenfilename(title="Загрузите файл с весами экспертов (Fuzzy AHP Type-1)",
                                          filetypes=[("CSV файлы", "*.csv")])
        if path:
            self.ahp_type1_weights_path = path
            self.status.config(text="✅ Загружен файл весов: " + os.path.basename(path))

    def load_fuzzy_ahp_type2_file(self):
        path = filedialog.askopenfilename(title="Загрузите файл попарных сравнений экспертов (Fuzzy AHP Type-2)",
                                          filetypes=[("CSV файлы", "*.csv")])
        if path:
            self.ahp_type2_path = path
            self.status.config(text="✅ Загружен файл Type-2: " + os.path.basename(path))

    def run_fuzzy_ahp(self):
        if not self.ahp_type1_criteria_path or not self.ahp_type1_alternatives_path or not self.ahp_type1_weights_path or not self.ahp_type2_path:
            messagebox.showwarning("⚠️ Внимание", "Загрузите все четыре файла: три для Type-1 и один для Type-2.")
            return

        try:
            from logic import fuzzy_ahp, fuzzy_ahp_report

            # Передаём все три пути для Type-1
            results_type1 = fuzzy_ahp.process_fuzzy_ahp_type1(
                criteria_path=self.ahp_type1_criteria_path,
                alternatives_path=self.ahp_type1_alternatives_path,
                weights_path=self.ahp_type1_weights_path
            )

            # Один путь для Type-2
            results_type2 = fuzzy_ahp.process_fuzzy_ahp_type2(self.ahp_type2_path)

            # Генерируем единый отчёт
            fuzzy_ahp_report.generate_report(results_type1, results_type2)

            self.status.config(text="📄 Объединённый отчет создан: output/fuzzy_ahp_report.pdf")

        except Exception as e:
            messagebox.showerror("Ошибка", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = PrioritizationTool(root)
    root.mainloop()
