
# Автоматизированная приоритизация требований к ПО

## Описание проекта

Данный проект предоставляет приложение для **автоматизированной приоритизации требований** к программному обеспечению, используя как классические (MoSCoW, Kano, TOPSIS), так и различные **нечёткие методы** (Fuzzy TOPSIS, Fuzzy Delphi, Fuzzy AHP).  
Цель — упростить процесс принятия решений при планировании функциональности систем, учитывая **многокритериальность** и **экспертную неопределённость**.

### Ключевые особенности

1. **Графический интерфейс** с подсказками (на базе `tkinter`).  
2. Работа с разнообразными **форматами входных данных** (CSV-файлы).  
3. Генерация **PDF-отчётов** (с помощью `fpdf`).  
4. Возможность **масштабирования** под различные методы нечёткого анализа.

---

## Архитектура проекта

```
prioritization_tool/
├── main.py
├── requirements.txt
├── README.md
├── output/
│   └── charts/
├── assets/
│   ├── Fuzzy AHP example/
│   ├── Fuzzy Delphi example/
│   ├── Fuzzy TOPSIS example/
│   ├── MoSCoW example/
│   ├── Kano example/
│   └── TOPSIS example/
├── fonts/
├── logic/
│   ├── Fuzzy AHP/                   
│   ├── Fuzzy Delphi/               
│   ├── Fuzzy_TOPSIS/               
│   ├── Kano/
│   │   ├── kano.py                 
│   │   └── kano_report.py          
│   ├── MoSCoW/
│   │   ├── moscow.py               
│   │   ├── moscow_report.py      
│   │   └── parser.py              
│   ├── TOPSIS/
│   │   ├── topsis.py               
│   │   └── topsis_report.py        
│
│   ├── delphi_report.py            
│   ├── fuzzy_delphi.py             
│   ├── intuitionistic_delphi.py    
│
│   ├── fuzzy_ahp.py                
│   ├── fuzzy_ahp_report.py         
│
│   ├── fuzzy_topsis.py             
│   ├── fuzzy_topsis_report.py      
│   ├── intuitionistic_topsis.py    
├── data/
```

---

## Установка и запуск

1. **Склонировать проект**:
```bash
git clone https://github.com/username/prioritization_tool.git
cd prioritization_tool
```

2. **Установить зависимости**:
```bash
pip install -r requirements.txt
```
Если файл `requirements.txt` отсутствует, можно установить вручную:
```bash
pip install pandas numpy matplotlib fpdf
```
> В Linux может потребоваться:
```bash
sudo apt-get install python3-tk
```

3. **Запустить приложение**:
```bash
python main.py
```

---

## Как пользоваться

1. Выберите метод приоритизации в главном окне.
2. Ознакомьтесь с форматом файлов (отображается автоматически).
3. Загрузите необходимые CSV-файлы.
4. Нажмите "Рассчитать".
5. Сохраните результат в PDF, нажав соответствующую кнопку.

Результаты сохраняются в папке `output`.

---

## Форматы входных данных

Примеры файлов находятся в папке `assets/`:
- **Fuzzy AHP**: `criteria.csv`, `alternatives.csv`, `weights.csv`, `type2.csv`
- **Fuzzy Delphi**: `fuzzy_delphi_example.csv`, `intuitionistic_delphi_example.csv`
- **Fuzzy TOPSIS**: `fuzzy_type1_example.csv`, `intuitionistic_example.csv`, шкалы
- **MoSCoW**: `moscow_example.csv`, `weights_example.csv`
- **Kano**: `kano_example.csv`
- **TOPSIS**: `topsis_example.csv`
