
import tkinter as tk
from tkinter import filedialog
import pandas as pd
import random
from datetime import datetime

def calculate_k_anonymity():
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if not file_path:
        return

    data = pd.read_csv(file_path)

    k_values = data.groupby(data.columns.tolist()).size().reset_index(name='Count')
    kval = set()
    for i in k_values['Count']:
        kval.add(i)
    kper = {i: 0 for i in kval}
    for i in k_values['Count']:
        kper[i] += i

    kper_col = kper.copy()

    for i in kper.keys():
        kper[i] = kper[i] / len(data)* 100


    #result_label.config(text="5 наименьших значений К-анонимности")
    percentage_label.config(text="К-анонимность в %:")
    result_text.delete(1.0, tk.END)

    for v in sorted(kper.keys()):
        result_text.insert(tk.END, f"{v} ({kper[v]:.2f}%) - {kper_col[v]}\n")


def calculate_unique_rows():
    file_path = filedialog.askopenfilename()
    if file_path:
        df = pd.read_csv(file_path)

        lst_var = ['ФИО', 'Паспортные данные', 'Откуда', 'Куда', 'Дата отъезда', 'Дата приезда', 'Рейс', 'Выбор вагона и места', 'Стоимость', 'Карта оплаты']
        for i in lst_var:
            if i not in df.columns:
                var_list.remove(var_list[lst_var.index(i)])

        selected_quasi_identifiers = [var.get() for var in var_list]
        selected_columns = [column for column, is_selected in zip(df.columns, selected_quasi_identifiers) if is_selected]

        quasi_identifiers = df[selected_columns]

        unique_rows = quasi_identifiers.drop_duplicates().shape[0]

        result_label.config(text=f"Количество уникальных строк: {unique_rows}")


def replace_names_with_initials(data, name_column):
    # Разбиваем ФИО на отдельные слова
    name_parts = data[name_column].str.split()

    # Создаем список инициалов
    initials_list = []
    for name in name_parts:
        initials = '. '.join([name_part[0] for name_part in name]) + "."
        initials_list.append(initials)

    # Заменяем столбец с ФИО на инициалы
    data[name_column] = initials_list

    return data


def mask_num_data(data, passport_column, num_dontmask):
    data[passport_column] = data[passport_column].apply(lambda x: x[:num_dontmask] + '*' * (len(x) - num_dontmask))
    return data

def round_price_to_thousands(data, price_column):
    # Округляем значение в столбце до ближайшей тысячи
    data[price_column] = data[price_column].apply(lambda x: round(x, -2))

    return data

def remove_attributes(data, columns_to_remove):
    return data.drop(columns=columns_to_remove, axis=1)

def replace_names_with_gender(data, name_column):
    # Функция для определения пола по имени
    def determine_gender(name):
        vowels = 'АаУуЕеЫыОоЭэЮюИиЯя'
        return "Ж" if name[-1] in vowels else "М"

    # Определяем полы для ФИО
    data['Gender'] = data[name_column].apply(determine_gender)

    # Заменяем ФИО на пол
    data[name_column] = data['Gender']

    # Удаляем столбец с полами (если он больше не нужен)
    data = data.drop(columns=['Gender'], axis=1)

    return data

def date_to_season(date_str):
    # Преобразование строки в объект datetime
    date = datetime.strptime(date_str, ' %Y-%m-%d-%H:%M ')

    # Определение сезона года на основе месяца
    month = date.month
    if 3 <= month <= 5:
        return 'Весна'
    elif 6 <= month <= 8:
        return 'Лето'
    elif 9 <= month <= 11:
        return 'Осень'
    else:
        return 'Зима'

def local_generalization_date(data, arrival_date_column, departure_date_column):
    # Применяем функцию date_to_season к столбцам с датами приезда и отъезда
    data[arrival_date_column] = data[arrival_date_column].apply(date_to_season)
    data[departure_date_column] = data[departure_date_column].apply(date_to_season)

    return data

def price_to_category(price):
    if 0 <= price <= 6000:
        return 'Низкая'
    elif 5000 < price <= 13000:
        return 'Средняя'
    else:
        return 'Высокая'

def local_generalization_price(data, price_column):
    # Применяем функцию price_to_category к столбцу с ценой
    data[price_column] = data[price_column].apply(price_to_category)

    return data

def local_suppression(data, n):
    # Подсчитываем количество вхождений для каждой строки
    data['Count'] = data.duplicated(keep=False)

    # Группируем по строкам и считаем количество вхождений
    counts = data.groupby(data.columns.tolist())['Count'].transform('sum')

    # Оставляем только строки, у которых количество вхождений >= n
    data = data[counts >= n]

    # Удаляем столбец 'Count', так как он больше не нужен
    data = data.drop(columns=['Count'], axis=1)

    return data

def dataset_depersonalization():
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if not file_path:
        return

    data_types = {
    'ФИО': str,                  # Строковый тип данных
    'Паспортные данные': str,     # Строковый тип данных
    'Стоимость': float,          # Вещественное число
    'Карта оплаты': str          # Строковый тип данных
    }

    data = pd.read_csv(file_path, dtype=data_types)
    
    data = replace_names_with_gender(data, "ФИО")
    data = mask_num_data(data, "Паспортные данные", 0)
    data = local_generalization_date(data, "Дата отъезда", "Дата приезда")
    data = remove_attributes(data, "Выбор вагона и места")
    data = local_generalization_price(data, "Стоимость")
    data = mask_num_data(data, "Карта оплаты", 0)
    data = local_suppression(data, 10)


    data.to_csv('dep_tick.csv', index=False)

    print("Done")


root = tk.Tk()
root.geometry("600x350")
root.title("K-Anonymity Calculator")

file_button0 = tk.Button(root, text="Посчитать К-анонимити", command=calculate_k_anonymity)
file_button1 = tk.Button(root, text="Обезличить датасет", command=dataset_depersonalization)
file_button0.pack()
file_button1.pack()

select_file_button = tk.Button(root, text="Квази идентификаторы", command=calculate_unique_rows)
select_file_button.pack()


var_list = []
for column in ['ФИО', 'Паспортные данные', 'Откуда', 'Куда', 'Дата отъезда', 'Дата приезда', 'Рейс', 'Выбор вагона и места', 'Стоимость', 'Карта оплаты']:
    var = tk.IntVar()
    checkbox = tk.Checkbutton(root, text=column, variable=var)
    checkbox.pack()
    var_list.append(var)


result_label = tk.Label(root, text="")
result_label.pack()
percentage_label = tk.Label(root, text="")
percentage_label.pack()


root.geometry("600x550")
result_text = tk.Text(root, height=10, width=80)
result_text.pack()


root.mainloop()

