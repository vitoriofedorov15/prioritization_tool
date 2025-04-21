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

        # Основной стиль для кнопок (меньший размер)
        style.configure("TButton",
                        font=("Segoe UI", 10),  # Уменьшен размер шрифта
                        padding=6,  # Уменьшен padding
                        foreground="#ffffff",
                        background="#2980b9")

        style.map("TButton",
                  foreground=[('active', '#ffffff')],
                  background=[('active', '#1abc9c')])

        # Стиль для заголовков
        style.configure("Header.TLabel",
                        font=("Segoe UI", 26, "bold"),
                        foreground="#2c3e50")

        # Стиль для информационных сообщений
        style.configure("Info.TLabel",
                        font=("Segoe UI", 12),
                        foreground="#2f3640",
                        wraplength=800,
                        justify="center")

        # Стиль для статуса
        style.configure("Status.TLabel",
                        font=("Segoe UI", 12),
                        foreground="#27ae60")

        # Стиль для кнопки выхода
        style.configure("Exit.TButton",
                        font=("Segoe UI", 9, "bold"),  # Уменьшен размер шрифта
                        padding=4,  # Уменьшен padding
                        foreground="#ffffff",
                        background="#7f8c8d")

        style.map("Exit.TButton",
                  background=[('active', '#95a5a6')])

        # Новый стиль для маленьких кнопок
        style.configure("Small.TButton",
                        font=("Segoe UI", 9),
                        padding=4,  # Маленький padding
                        foreground="#ffffff",
                        background="#2980b9")

        style.map("Small.TButton",
                  foreground=[('active', '#ffffff')],
                  background=[('active', '#1abc9c')])

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

        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(fill="both", expand=True)

        ttk.Label(main_frame, text="Метод MoSCoW", style="Header.TLabel").pack(pady=(0, 20))

        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill="both", expand=True)

        # Левая колонка
        left_frame = ttk.Frame(content_frame)
        left_frame.pack(side="left", fill="both", expand=True, padx=10)

        requirements_description = (
            "ФОРМАТ ФАЙЛА ТРЕБОВАНИЙ (CSV)\n\n"
            "Обязательные требования:\n"
            "• Первая строка - названия столбцов в кавычках\n"
            "• Должны быть столбцы: \"Альтернатива\", \"Критерий\", \"Стейкхолдер\", \"Оценка\"\n"
            "• Оценка — например: \"100% M\" или \"60% S, 40% C\"\n"
            "• Разрешены только комбинации оценок: M/S, S/C, C/W\n"
            "• Значения должны быть в кавычках\n"
            "• Разделитель - запятая\n"
        )

        req_msg = tk.Message(left_frame, text=requirements_description, width=380, font=("Segoe UI", 9),
                             justify="left")
        req_msg.pack(pady=(0, 10))
        ttk.Button(left_frame, text="📁 Загрузить данные", command=self.load_requirements).pack()

        # Правая колонка
        right_frame = ttk.Frame(content_frame)
        right_frame.pack(side="left", fill="both", expand=True, padx=10)

        weights_description = (
            "ФОРМАТ ФАЙЛА ВЕСОВ (CSV)\n\n"
            "Обязательные требования:\n"
            "• Первая строка - названия столбцов в кавычках\n"
            "• Должны быть столбцы: \"Стейкхолдер\" и \"Вес\"\n"
            "• Пример строки: \"S1\",\"1.5\"\n"
            "• Значения должны быть в кавычках\n"
            "• Разделитель - запятая\n"
        )

        weights_msg = tk.Message(right_frame, text=weights_description, width=380, font=("Segoe UI", 9),
                                 justify="left")
        weights_msg.pack(pady=(0, 10))
        ttk.Button(right_frame, text="📁 Загрузить данные", command=self.load_weights).pack()

        # Фрейм для кнопок внизу
        bottom_frame = ttk.Frame(main_frame)
        bottom_frame.pack(fill="x", side="bottom", pady=(10, 5))
        center_frame = ttk.Frame(bottom_frame)
        center_frame.pack(side="left", padx=(20, 0))

        ttk.Button(
            center_frame,
            text="✅ Сформировать отчет",
            command=self.run_moscow,
            style="TButton"
        ).pack(side="left", expand=True, padx=8, pady=5)

        ttk.Button(
            bottom_frame,
            text="🔙 Вернуться назад",
            command=self.show_method_selection_screen,
            style="Exit.TButton"
        ).pack(side="right", padx=5, pady=5)

        self.status = ttk.Label(main_frame, text="", style="Status.TLabel")
        self.status.pack(side="bottom", pady=(5, 0))

    def show_kano_screen(self):
        self.clear_window()
        frame = ttk.Frame(self.root, padding=20)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Модель Кано", style="Header.TLabel").pack(pady=(0, 10))

        description = (
            "ФОРМАТ ФАЙЛА ТРЕБОВАНИЙ ДЛЯ МЕТОДА КАНО (CSV)\n\n"
            "Файл требований (CSV): должен содержать 5 столбцов:\n"
            "  - Альтернатива\n"
            "  - Стейкхолдер\n"
            "  - Функциональный ответ (например: \"Must-be\", \"Attractive\")\n"
            "  - Дисфункциональный ответ (например: \"Indifferent\", \"Reverse\")\n"
            "  - Вес (например: \"1.0\", \"1.5\")\n\n"
            "Первая строка в каждом файле — названия столбцов в кавычках, разделитель — запятая.\n"
            "Значение, соответствующее каждому столбцу, должно быть заключено в кавычки, разделитель — запятая.\n\n"
            "Допустимые категории ответов:\n"
            "Must-be, One-dimensional, Attractive, Indifferent, Reverse, Questionable.\n"
        )

        msg = tk.Message(frame, text=description, width=800, font=("Segoe UI", 9), justify="left")
        msg.pack(pady=(0, 15))

        ttk.Button(frame, text="📁 Загрузить данные", command=self.load_kano_file).pack(pady=5)
        # Фрейм для кнопок внизу
        bottom_frame = ttk.Frame(frame)
        bottom_frame.pack(fill="x", side="bottom", pady=(10, 5))
        center_frame = ttk.Frame(bottom_frame)
        center_frame.pack(side="left", padx=(20, 0))

        ttk.Button(
            center_frame,
            text="✅ Сформировать отчет",
            command=self.run_kano,
            style="TButton"
        ).pack(side="left", expand=True, padx=5, pady=5)

        ttk.Button(
            bottom_frame,
            text="🔙 Вернуться назад",
            command=self.show_method_selection_screen,
            style="Exit.TButton"
        ).pack(side="right", padx=5, pady=5)

        self.status = ttk.Label(frame, text="", style="Status.TLabel")
        self.status.pack(side="bottom", pady=(5, 0))

    def load_kano_file(self):
        path = filedialog.askopenfilename(title="Выберите CSV-файл с анкетой Кано", filetypes=[("CSV файлы", "*.csv")])
        if path:
            self.kano_csv_path = path
            self.status.config(text="✅ Файл требований загружен.")

    def run_kano(self):
        if not self.kano_csv_path:
            messagebox.showwarning("⚠️ Внимание", "Пожалуйста, загрузите CSV-файл перед расчетом.")
            return

        try:
            results = kano.process_kano_csv(self.kano_csv_path)
            kano_report.generate_kano_report(results, filename="output/kano_report.pdf")
            self.status.config(text="📄 Отчет сохранен в output/kano_report.pdf")
        except Exception as e:
            messagebox.showerror("❌ Ошибка", str(e))

    def show_topsis_screen(self):
        self.clear_window()
        frame = ttk.Frame(self.root, padding=20)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Метод TOPSIS", style="Header.TLabel").pack(pady=(0, 10))

        description = (
            "ФОРМАТ ФАЙЛА ТРЕБОВАНИЙ ДЛЯ ЧИСЛЕННОЙ ОЦЕНКИ (CSV)\n\n"
            "Файл требований (CSV): должен содержать численные оценки альтернатив по критериям и вес стейкхолдера:\n"
            "  - Альтернатива (например: \"Авторизация через соцсети\")\n"
            "  - Безопасность (например: \"7\")\n"
            "  - Удобство (например: \"8\")\n"
            "  - Бизнес-ценность (например: \"6\")\n"
            "  - Вес стейкхолдера (например: \"0.3\")\n\n"
            "Первая строка в каждом файле — названия столбцов в кавычках, разделитель — запятая.\n"
            "Значение, соответствующее каждому столбцу, должно быть заключено в кавычки, разделитель — запятая.\n"
            "Все числовые значения должны быть заданы в единой шкале (например, от 1 до 10).\n"
        )

        msg = tk.Message(frame, text=description, width=800, font=("Segoe UI", 9), justify="left")
        msg.pack(pady=(0, 15))

        ttk.Button(frame, text="📁 Загрузить данные", command=self.load_topsis_file, style="Small.TButton").pack(pady=3)

        # Фрейм для кнопок внизу
        bottom_frame = ttk.Frame(frame)
        bottom_frame.pack(fill="x", side="bottom", pady=(10, 5))
        center_frame = ttk.Frame(bottom_frame)
        center_frame.pack(side="left", padx=(20, 0))

        ttk.Button(
            center_frame,
            text="✅ Сформировать отчет",
            command=self.run_topsis,
            style="TButton"
        ).pack(side="left", expand=True, padx=5, pady=5)

        ttk.Button(
            bottom_frame,
            text="🔙 Вернуться назад",
            command=self.show_method_selection_screen,
            style="Exit.TButton"
        ).pack(side="right", padx=5, pady=5)

        self.status = ttk.Label(frame, text="", style="Status.TLabel")
        self.status.pack(side="bottom", pady=(5, 0))


    def load_topsis_file(self):
        path = filedialog.askopenfilename(title="Выберите CSV-файл для TOPSIS", filetypes=[("CSV файлы", "*.csv")])
        if path:
            self.topsis_file_path = path
            self.status.config(text="✅ Файл требований загружен.")

    def load_requirements(self):
        path = filedialog.askopenfilename(title="Выберите CSV с требованиями", filetypes=[("CSV файлы", "*.csv")])
        if path:
            self.requirements_path = path
            self.status.config(text="✅ Файл требований загружен.")

    def load_weights(self):
        path = filedialog.askopenfilename(title="Выберите CSV с весами", filetypes=[("CSV файлы", "*.csv")])
        if path:
            self.weights_path = path
            self.status.config(text="✅ Файл весов загружен.")

    def run_moscow(self):
        if not self.requirements_path or not self.weights_path:
            messagebox.showwarning("⚠️ Внимание", "Пожалуйста, загрузите оба CSV-файла перед расчетом.")
            return

        try:
            req_data = parser.load_requirements(self.requirements_path)
            weights = parser.load_weights(self.weights_path)
            results = moscow.calculate(req_data, weights)
            moscow_report.generate_pdf(results, filename="output/moscow_report.pdf")
            self.status.config(text="📄 Отчет сохранен в output/moscow_report.pdf")
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
            self.status.config(text="📄 Отчет сохранен в output/topsis_report.pdf")
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def show_fuzzy_topsis_screen(self):
        self.clear_window()
        frame = ttk.Frame(self.root, padding=20)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Метод Fuzzy TOPSIS", style="Header.TLabel").pack(pady=(0, 10))
        container = ttk.Frame(frame)
        container.pack(fill="both", expand=True)

        # Левая колонка — Fuzzy TOPSIS Type-1
        left = ttk.Frame(container, padding=10)
        left.pack(side="left", fill="both", expand=True)
        ttk.Label(left, text="Fuzzy TOPSIS Type-1", style="SubHeader.TLabel").pack(pady=(0, 5))

        msg1 = tk.Message(
            left,
            text=(
                "ФОРМАТ ФАЙЛА ТРЕБОВАНИЙ (CSV)\n\n"
                "Обязательные требования:\n"
                "• Первая строка - названия столбцов в кавычках\n"
                "• Первый столбец - \"Альтернатива\" (названия требований)\n"
                "• Последующие столбцы - критерии оценки\n"
                "• Все значения - текстовые оценки в кавычках\n"
                "• Разделитель - запятая\n\n"
                "ДОПУСТИМЫЕ ТЕКСТОВЫЕ ОЦЕНКИ:\n"
                "Определяются загруженной шкалой (например: \"Очень низко\", \"Низко\",\n"
                "\"Средне\", \"Высоко\", \"Очень высоко\")\n"
            ),
            width=500,
            font=("Segoe UI", 9),
            justify="left"
        )
        msg1.pack(pady=(0, 5))
        ttk.Button(left, text="📁 Загрузить данные", command=self.load_fuzzy_type1_file).pack(pady=5)

        msg_scale = tk.Message(
            left,
            text=(
                "ФОРМАТ ФАЙЛА СООТВЕТСТВИЙ (CSV)\n\n"
                "Обязательные столбцы:\n"
                "1. \"Оценка эксперта\" - текстовая оценка\n"
                "2. \"Трапециевидное число\" - в формате \"(a,b,c,d)\"\n"
            ),
            width=500,
            font=("Segoe UI", 9),
            justify="left"
        )
        msg_scale.pack(pady=(5, 5))
        ttk.Button(left, text="📁 Загрузить данные", command=self.load_fuzzy_scale_file).pack(pady=5)
        ttk.Button(left, text="✅ Сформировать отчет 1", command=self.run_fuzzy_topsis_type1).pack(pady=(10, 0))

        # Правая колонка — Intuitionistic TOPSIS
        right = ttk.Frame(container, padding=10)
        right.pack(side="left", fill="both", expand=True)
        ttk.Label(right, text="Intuitionistic Fuzzy TOPSIS", style="SubHeader.TLabel").pack(pady=(0, 5))

        msg2 = tk.Message(
            right,
            text=(
                "ФОРМАТ ФАЙЛА ТРЕБОВАНИЙ (CSV)\n\n"
                "Обязательные требования:\n"
                "• Первая строка - названия столбцов в кавычках\n"
                "• Первый столбец - \"Альтернатива\" (названия требований)\n"
                "• Последующие столбцы - критерии оценки\n"
                "• Все значения - текстовые оценки в кавычках\n"
                "• Разделитель - запятая\n\n"
                "ДОПУСТИМЫЕ ТЕКСТОВЫЕ ОЦЕНКИ:\n"
                "• Очень важно, и я уверен(a) "
                "• Очень важно, но есть сомнения "
                "• Важно, и я уверен(a)\n"
                "• Важно, но есть сомнения "
                "• Средне, но я уверен(a) "
                "• Средне, и есть сомнения\n"
                "• Маловажно, но я уверен(a) "
                "• Маловажно, и я уверен(a) "
                "• Неважно, но я уверен(a)\n"
                "• Неважно, и есть сомнения\n"
            ),
            width=500,
            font=("Segoe UI", 9),
            justify="left"
        )
        msg2.pack(pady=(0, 5))
        ttk.Button(right, text="📁 Загрузить данные", command=self.load_intuitionistic_file).pack(pady=5)

        msg_ifs_scale = tk.Message(
            right,
            text=(
                "ФОРМАТ ФАЙЛА СООТВЕТСТВИЙ (CSV)\n\n"
                "Обязательные столбцы:\n"
                "1. \"Оценка эксперта\" - текстовая оценка\n"
                "2. \"Степень принадлежности\" - число 0.0-1.0\n"
                "3. \"Степень непринадлежности\" - число 0.0-1.0\n"
                "4. \"Степень неопределённости\" - число 0.0-1.0\n\n"
                "ТРЕБОВАНИЯ:\n"
                "Все значения в кавычках, разделитель - запятая\n"
                "Первая строка - заголовки столбцов, Сумма (μ + ν + π) ≤ 1.0 для каждой строки\n"
            ),
            width=500,
            font=("Segoe UI", 9),
            justify="left"
        )
        msg_ifs_scale.pack(pady=(5, 5))
        ttk.Button(right, text="📁 Загрузить данные", command=self.load_ifs_scale_file).pack(pady=5)
        ttk.Button(right, text="✅ Сформировать отчет 2", command=self.run_fuzzy_topsis_type2).pack(pady=(10, 0))

        # Фрейм для кнопок внизу
        bottom_frame = ttk.Frame(frame)
        bottom_frame.pack(fill="x", pady=(15, 0))
        center_frame = ttk.Frame(bottom_frame)
        center_frame.pack(side="left", padx=(20, 0))

        # Кнопка "Сформировать комбинированный отчет" по центру
        ttk.Button(
            center_frame,
            text="✅ Сформировать комбинированный отчет",
            command=self.run_fuzzy_topsis_combined,
            style="TButton"
        ).pack(side="left", expand=True, padx=5, pady=5)

        # Кнопка "Назад" справа
        ttk.Button(
            bottom_frame,
            text="🔙 Вернуться назад",
            command=self.show_method_selection_screen,
            style="Exit.TButton"
        ).pack(side="right", padx=5, pady=5)

        # Статус
        self.status = ttk.Label(frame, text="", style="Status.TLabel")
        self.status.pack(pady=(10, 0))

    def run_fuzzy_topsis_type1(self):
        if not self.fuzzy_type1_path or not hasattr(self, 'fuzzy_scale_path'):
            messagebox.showwarning("⚠️ Внимание", "Загрузите оба файла для Fuzzy TOPSIS Type-1")
            return

        try:
            from prioritization_tool.logic.fuzzy_topsis import calculate_fuzzy_topsis
            from prioritization_tool.logic.fuzzy_topsis_report import generate_single_report

            results = calculate_fuzzy_topsis(self.fuzzy_type1_path, self.fuzzy_scale_path)
            generate_single_report(results, "Fuzzy TOPSIS Type-1", "output/fuzzy_topsis_type1_report.pdf")
            self.status.config(text="📄 Отчет сохранен: output/fuzzy_topsis_type1_report.pdf")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка обработки: {str(e)}")

    def run_fuzzy_topsis_type2(self):
        if not self.topsis_intuitionistic_path or not hasattr(self, 'ifs_scale_path'):
            messagebox.showwarning("⚠️ Внимание", "Загрузите оба файла для Intuitionistic Fuzzy TOPSIS")
            return

        try:
            from prioritization_tool.logic.intuitionistic_topsis import calculate_ifs_topsis
            from prioritization_tool.logic.fuzzy_topsis_report import generate_single_report

            results = calculate_ifs_topsis(self.topsis_intuitionistic_path, self.ifs_scale_path)
            generate_single_report(results, "Intuitionistic Fuzzy TOPSIS", "output/fuzzy_topsis_type2_report.pdf")
            self.status.config(text="📄 Отчет сохранен: output/fuzzy_topsis_type2_report.pdf")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка обработки: {str(e)}")

    def run_fuzzy_topsis_combined(self):
        if not all([hasattr(self, 'fuzzy_type1_path'),
                    hasattr(self, 'fuzzy_scale_path'),
                    hasattr(self, 'topsis_intuitionistic_path'),
                    hasattr(self, 'ifs_scale_path')]):
            messagebox.showwarning("⚠️ Внимание", "Загрузите все файлы для формирования комбинированного отчета")
            return

        try:
            from prioritization_tool.logic.fuzzy_topsis import calculate_fuzzy_topsis
            from prioritization_tool.logic.intuitionistic_topsis import calculate_ifs_topsis
            from prioritization_tool.logic.fuzzy_topsis_report import generate_combined_report

            results_type1 = calculate_fuzzy_topsis(self.fuzzy_type1_path, self.fuzzy_scale_path)
            results_type2 = calculate_ifs_topsis(self.topsis_intuitionistic_path, self.ifs_scale_path)

            generate_combined_report(results_type1, results_type2)
            self.status.config(text="📄 Комбинированный отчет сохранен: output/fuzzy_topsis_report.pdf")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка обработки: {str(e)}")

    def load_fuzzy_type1_file(self):
        path = filedialog.askopenfilename(
            title="Загрузите файл для Fuzzy TOPSIS Type-1",
            filetypes=[("CSV файлы", "*.csv")]
        )
        if path:
            self.fuzzy_type1_path = path
            self.status.config(text="✅ Файл требований 1 загружен.")

    def load_ifs_scale_file(self):
        path = filedialog.askopenfilename(
            title="Загрузите шкалу значений для Intuitionistic Fuzzy TOPSIS",
            filetypes=[("CSV файлы", "*.csv")]
        )
        if path:
            self.ifs_scale_path = path
            self.status.config(text="✅ Файл соответствий 2 загружен.")

    def load_intuitionistic_file(self):
        path = filedialog.askopenfilename(
            title="Загрузите файл для Intuitionistic TOPSIS",
            filetypes=[("CSV файлы", "*.csv")]
        )
        if path:
            self.topsis_intuitionistic_path = path
            self.status.config(text="✅ Файл требований 2 загружен.")
    def load_fuzzy_scale_file(self):
        path = filedialog.askopenfilename(
            title="Загрузите файл шкалы значений для Fuzzy TOPSIS",
            filetypes=[("CSV файлы", "*.csv")]
        )
        if path:
            self.fuzzy_scale_path = path
            self.status.config(text="✅ Файл соответствий 1 загружен.")

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

        ttk.Label(frame, text="Метод Fuzzy Delphi", style="Header.TLabel").pack(pady=(0, 10))

        container = ttk.Frame(frame)
        container.pack(fill="both", expand=True)

        # Левая колонка — Fuzzy Delphi Type-2
        left = ttk.Frame(container, padding=10)
        left.pack(side="left", fill="both", expand=True)

        ttk.Label(left, text="Fuzzy Delphi Type-2", style="SubHeader.TLabel").pack(pady=(0, 5))

        msg1 = tk.Message(
            left,
            text=(
                "ФОРМАТ ФАЙЛА ТРЕБОВАНИЙ (CSV)\n\n"
                "Обязательные столбцы:\n"
                "• Альтернатива\n"
                "• Эксперт\n"
                "• Вес эксперта\n"
                "• Критерии оценки (один или несколько)\n\n"
                "Оценки должны быть в формате:\n"
                "\"Степень уверенности – Лингвистическая оценка\"\n"
                "Пример: \"Высокая уверенность – Высокая\"\n\n"
                "Допустимые оценки:\n"
                "• Степень уверенности: Очень высокая, Высокая, Средняя, Низкая\n"
                "• Лингвистические оценки: Очень низкая, Низкая, Средняя, Высокая, Очень высокая\n"
            ),
            width=380,
            font=("Segoe UI", 9),
            justify="left"
        )
        msg1.pack(pady=(0, 5))
        ttk.Button(left, text="📁 Загрузить данные", command=self.load_fuzzy_delphi_file, style="Small.TButton").pack(
            pady=5)
        ttk.Button(left, text="✅ Сформировать отчет 1", command=self.run_fuzzy_delphi_type2).pack(pady=(10, 0))

        # Правая колонка — Delphi Intuitionistic
        right = ttk.Frame(container, padding=10)
        right.pack(side="left", fill="both", expand=True)

        ttk.Label(right, text="Intuitionistic Delphi", style="SubHeader.TLabel").pack(pady=(0, 5))

        msg2 = tk.Message(
            right,
            text=(
                "ФОРМАТ ФАЙЛА ТРЕБОВАНИЙ (CSV)\n\n"
                "Обязательные столбцы:\n"
                "• Альтернатива\n"
                "• Эксперт\n"
                "• Вес эксперта\n"
                "• Критерии оценки (один или несколько)\n\n"
                "Оценки должны быть в формате:\n"
                "\"(μ, ν, π)\" где:\n"
                "• μ - степень принадлежности (0-1)\n"
                "• ν - степень непринадлежности (0-1)\n"
                "• π - степень неопределенности (0-1)\n\n"
                "Пример: \"(0.7, 0.2, 0.1)\"\n"
                "Сумма (μ + ν + π) должна быть ≤ 1.0\n"
            ),
            width=380,
            font=("Segoe UI", 9),
            justify="left"
        )
        msg2.pack(pady=(0, 5))
        ttk.Button(right, text="📁 Загрузить данные", command=self.load_delphi_ifs_file, style="Small.TButton").pack(
            pady=5)
        ttk.Button(right, text="✅ Сформировать отчет 2", command=self.run_fuzzy_delphi_ifs).pack(pady=(10, 0))

        # Фрейм для кнопок внизу
        bottom_frame = ttk.Frame(frame)
        bottom_frame.pack(fill="x", pady=(15, 0))
        center_frame = ttk.Frame(bottom_frame)
        center_frame.pack(side="left", padx=(20, 0))

        # Кнопка "Сформировать комбинированный отчет" по центру
        ttk.Button(
            center_frame,
            text="✅ Сформировать комбинированный отчет",
            command=self.run_fuzzy_delphi_combined,
            style="TButton"
        ).pack(side="left", expand=True, padx=5, pady=5)

        # Кнопка "Назад" справа
        ttk.Button(
            bottom_frame,
            text="🔙 Вернуться назад",
            command=self.show_method_selection_screen,
            style="Exit.TButton"
        ).pack(side="right", padx=5, pady=5)

        # Статус
        self.status = ttk.Label(frame, text="", style="Status.TLabel")
        self.status.pack(pady=(10, 0))


    def load_fuzzy_delphi_file(self):
        path = filedialog.askopenfilename(title="Загрузите файл Fuzzy Delphi Type-2",
                                          filetypes=[("CSV файлы", "*.csv")])
        if path:
            self.fuzzy_delphi_path = path
            self.status.config(text="✅ Файл требований 1 загружен.")

    def load_delphi_ifs_file(self):
        path = filedialog.askopenfilename(title="Загрузите файл Delphi Intuitionistic",
                                          filetypes=[("CSV файлы", "*.csv")])
        if path:
            self.delphi_ifs_path = path
            self.status.config(text="✅ Файл требований 2 загружен.")

    def run_fuzzy_delphi_type2(self):
        if not self.fuzzy_delphi_path:
            messagebox.showwarning("⚠️ Внимание", "Загрузите файл для Fuzzy Delphi Type-2")
            return

        try:
            from prioritization_tool.logic.fuzzy_delphi import process_fuzzy_delphi
            from prioritization_tool.logic.delphi_report import generate_single_report

            results = process_fuzzy_delphi(self.fuzzy_delphi_path)
            generate_single_report(results, "Fuzzy Delphi Type-2", "output/delphi_type2_report.pdf")
            self.status.config(text="📄 Отчет сохранен: output/delphi_type2_report.pdf")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка обработки: {str(e)}")

    def run_fuzzy_delphi_ifs(self):
        if not self.delphi_ifs_path:
            messagebox.showwarning("⚠️ Внимание", "Загрузите файл для Delphi Intuitionistic")
            return

        try:
            from prioritization_tool.logic.fuzzy_delphi import process_delphi_ifs
            from prioritization_tool.logic.delphi_report import generate_single_report

            results = process_delphi_ifs(self.delphi_ifs_path)
            generate_single_report(results, "Delphi Intuitionistic", "output/delphi_ifs_report.pdf")
            self.status.config(text="📄 Отчет сохранен: output/delphi_ifs_report.pdf")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка обработки: {str(e)}")

    def run_fuzzy_delphi_combined(self):
        if not self.fuzzy_delphi_path or not self.delphi_ifs_path:
            messagebox.showwarning("⚠️ Внимание", "Загрузите оба файла для формирования комбинированного отчета")
            return

        try:
            from prioritization_tool.logic.fuzzy_delphi import process_fuzzy_delphi, process_delphi_ifs
            from prioritization_tool.logic.delphi_report import generate_combined_report

            results_type2 = process_fuzzy_delphi(self.fuzzy_delphi_path)
            results_ifs = process_delphi_ifs(self.delphi_ifs_path)

            generate_combined_report(results_type2, results_ifs)
            self.status.config(text="📄 Комбинированный отчет сохранен: output/fuzzy_delphi_report.pdf")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка обработки: {str(e)}")

    def show_fuzzy_ahp_screen(self):
        self.clear_window()
        frame = ttk.Frame(self.root, padding=20)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Метод Fuzzy AHP", style="Header.TLabel").pack(pady=(0, 10))

        container = ttk.Frame(frame)
        container.pack(fill="both", expand=True)

        # Левая колонка — Fuzzy AHP Type-1
        left = ttk.Frame(container, padding=10)
        left.pack(side="left", fill="both", expand=True)

        ttk.Label(left, text="Fuzzy AHP Type-1", style="SubHeader.TLabel").pack(pady=(0, 5))

        # Описание для критериев
        msg_criteria = tk.Message(
            left,
            text=(
                "ФОРМАТ ФАЙЛА КРИТЕРИЕВ (CSV)\n\n"
                "• Матрица попарных сравнений критериев\n"
                "• Значения: \"1\", \"2\", ..., \"9\" или \"1/2\", \"1/3\", ..., \"1/9\""
            ),
            width=380,
            font=("Segoe UI", 10),
            justify="left"
        )
        msg_criteria.pack(pady=(0, 5))

        ttk.Button(left, text="📁 Загрузить данные 1", command=self.load_fuzzy_ahp_criteria_file,
                   style="Small.TButton").pack(pady=(0, 10))

        # Описание для альтернатив
        msg_alternatives = tk.Message(
            left,
            text=(
                "ФОРМАТ ФАЙЛА АЛЬТЕРНАТИВ (CSV)\n\n"
                "• Оценки альтернатив по критериям\n"
                "• Формат значений: \"(a, b, c)\" (тройки чисел)"
            ),
            width=380,
            font=("Segoe UI", 10),
            justify="left"
        )
        msg_alternatives.pack(pady=(0, 5))

        ttk.Button(left, text="📁 Загрузить данные 2", command=self.load_fuzzy_ahp_alternatives_file,
                   style="Small.TButton").pack(pady=(0, 10))

        # Описание для весов экспертов
        msg_weights = tk.Message(
            left,
            text=(
                "ФОРМАТ ФАЙЛА ВЕСОВ ЭКСПЕРТОВ (CSV)\n\n"
                "• Столбцы: Эксперт, Вес\n"
                "• Сумма весов должна быть равна 1.0"
            ),
            width=380,
            font=("Segoe UI", 10),
            justify="left"
        )
        msg_weights.pack(pady=(0, 5))

        ttk.Button(left, text="📁 Загрузить данные 3", command=self.load_fuzzy_ahp_weights_file,
                   style="Small.TButton").pack(pady=(0, 10))

        # Кнопка формирования отчета Type-1
        ttk.Button(left, text="✅ Сформировать отчет 1", command=self.run_fuzzy_ahp_type1, style="TButton").pack(
            pady=(10, 0))

        # Правая колонка — Fuzzy AHP Type-2
        right = ttk.Frame(container, padding=10)
        right.pack(side="left", fill="both", expand=True)

        ttk.Label(right, text="Fuzzy AHP Type-2", style="SubHeader.TLabel").pack(pady=(0, 5))

        msg2 = tk.Message(
            right,
            text=(
                "ФОРМАТ ФАЙЛА КРИТЕРИЕВ (CSV)\n\n"
                "• Оценки попарных сравнений от экспертов\n"
                "• Столбцы: Эксперт, Вес, Критерий1>Критерий2, ...\n"
                "• Лингвистические оценки:\n"
                "  \"Одинаково\", \"Слабо\", \"Умеренно\",\n"
                "  \"Сильно\", \"Абсолютно\"\n\n"
                "Пример:\n"
                "\"Эксперт1\",\"0.3\",\"Слабо\",\"Умеренно\",..."
            ),
            width=380,
            font=("Segoe UI", 9),
            justify="left"
        )
        msg2.pack(pady=(0, 5))
        ttk.Button(right, text="📁 Загрузить данные", command=self.load_fuzzy_ahp_type2_file,
                   style="Small.TButton").pack(pady=5)
        ttk.Button(right, text="✅ Сформировать отчет 2", command=self.run_fuzzy_ahp_type2, style="TButton").pack(
            pady=(10, 0))

        # Фрейм для кнопок внизу
        bottom_frame = ttk.Frame(frame)
        bottom_frame.pack(fill="x", pady=(15, 0))
        center_frame = ttk.Frame(bottom_frame)
        center_frame.pack(side="left", padx=(20, 0))

        # Кнопка "Сформировать комбинированный отчет" по центру
        ttk.Button(
            center_frame,
            text="✅ Сформировать комбинированный отчет",
            command=self.run_fuzzy_ahp_combined,
            style="TButton"
        ).pack(side="left", expand=True, padx=5, pady=5)

        # Кнопка "Назад" справа
        ttk.Button(
            bottom_frame,
            text="🔙 Вернуться назад",
            command=self.show_method_selection_screen,
            style="Exit.TButton"
        ).pack(side="right", padx=5, pady=5)

        # Статус
        self.status = ttk.Label(frame, text="", style="Status.TLabel")
        self.status.pack(pady=(10, 0))

    def load_fuzzy_ahp_criteria_file(self):
        path = filedialog.askopenfilename(
            title="Загрузите файл с матрицей попарных сравнений критериев (Fuzzy AHP Type-1)",
            filetypes=[("CSV файлы", "*.csv")])
        if path:
            self.ahp_type1_criteria_path = path
            self.status.config(text="✅ Файл критериев 1 загружен.")

    def load_fuzzy_ahp_alternatives_file(self):
        path = filedialog.askopenfilename(title="Загрузите файл с оценками альтернатив (Fuzzy AHP Type-1)",
                                          filetypes=[("CSV файлы", "*.csv")])
        if path:
            self.ahp_type1_alternatives_path = path
            self.status.config(text="✅ Файл альтернатив загружен.")

    def load_fuzzy_ahp_weights_file(self):
        path = filedialog.askopenfilename(title="Загрузите файл с весами экспертов (Fuzzy AHP Type-1)",
                                          filetypes=[("CSV файлы", "*.csv")])
        if path:
            self.ahp_type1_weights_path = path
            self.status.config(text="✅ Файл весов загружен.")

    def load_fuzzy_ahp_type2_file(self):
        path = filedialog.askopenfilename(title="Загрузите файл попарных сравнений экспертов (Fuzzy AHP Type-2)",
                                          filetypes=[("CSV файлы", "*.csv")])
        if path:
            self.ahp_type2_path = path
            self.status.config(text="✅ Файл критериев 2 загружен.")

    def run_fuzzy_ahp_type1(self):
        try:
            from prioritization_tool.logic.fuzzy_ahp import process_fuzzy_ahp_type1
            from prioritization_tool.logic.fuzzy_ahp_report import generate_single_report

            if not all([self.ahp_type1_criteria_path,
                        self.ahp_type1_alternatives_path,
                        self.ahp_type1_weights_path]):
                raise ValueError("Не все файлы загружены")

            results = process_fuzzy_ahp_type1(
                self.ahp_type1_criteria_path,
                self.ahp_type1_alternatives_path,
                self.ahp_type1_weights_path
            )

            generate_single_report(results, "Fuzzy AHP Type-1", "output/fuzzy_ahp_type1_report.pdf")
            self.status.config(text="📄 Отчет сохранен: output/fuzzy_ahp_type1_report.pdf")

        except Exception as e:
            error_msg = f"Ошибка: {str(e)}\nПроверьте:\n1. Формат файлов\n2. Заполнение данных"
            messagebox.showerror("Ошибка обработки", error_msg)
            self.status.config(text="❌ Ошибка при генерации отчета")


    def run_fuzzy_ahp_type2(self):
        if not self.ahp_type2_path:
            messagebox.showwarning("⚠️ Внимание", "Загрузите файл для Fuzzy AHP Type-2")
            return

        try:
            from prioritization_tool.logic.fuzzy_ahp import process_fuzzy_ahp_type2
            from prioritization_tool.logic.fuzzy_ahp_report import generate_single_report

            results = process_fuzzy_ahp_type2(self.ahp_type2_path)
            generate_single_report(results, "Fuzzy AHP Type-2", "output/fuzzy_ahp_type2_report.pdf")
            self.status.config(text="📄 Отчет сохранен: output/fuzzy_ahp_type2_report.pdf")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка обработки: {str(e)}")

    def run_fuzzy_ahp_combined(self):
        if not all([self.ahp_type1_criteria_path,
                    self.ahp_type1_alternatives_path,
                    self.ahp_type1_weights_path,
                    self.ahp_type2_path]):
            messagebox.showwarning("⚠️ Внимание", "Загрузите все файлы для формирования комбинированного отчета")
            return

        try:
            from prioritization_tool.logic.fuzzy_ahp import process_fuzzy_ahp_type1, process_fuzzy_ahp_type2
            from prioritization_tool.logic.fuzzy_ahp_report import generate_combined_report

            results_type1 = process_fuzzy_ahp_type1(
                self.ahp_type1_criteria_path,
                self.ahp_type1_alternatives_path,
                self.ahp_type1_weights_path
            )
            results_type2 = process_fuzzy_ahp_type2(self.ahp_type2_path)

            generate_combined_report(results_type1, results_type2)
            self.status.config(text="📄 Комбинированный отчет сохранен: output/fuzzy_ahp_report.pdf")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка обработки: {str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = PrioritizationTool(root)
    root.mainloop()
