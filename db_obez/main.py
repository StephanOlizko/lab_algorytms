
import tkinter as tk
from tkinter import filedialog
import pandas as pd

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

    for i in kper.keys():
        kper[i] = kper[i] / len(data)* 100


    result_label.config(text="5 наименьших значений К-анонимности")
    percentage_label.config(text="К-анонимность в %:")
    result_text.delete(1.0, tk.END)

    for v in sorted(kper.keys()):
        result_text.insert(tk.END, f"{v} ({kper[v]:.2f}%)\n")


def calculate_unique_rows():
    file_path = filedialog.askopenfilename()
    if file_path:
        df = pd.read_csv(file_path)
        
        selected_quasi_identifiers = [var.get() for var in var_list]
        selected_columns = [column for column, is_selected in zip(df.columns, selected_quasi_identifiers) if is_selected]

        quasi_identifiers = df[selected_columns]

        unique_rows = quasi_identifiers.drop_duplicates().shape[0]

        result_label.config(text=f"Количество уникальных строк: {unique_rows}")


root = tk.Tk()
root.geometry("600x350")
root.title("K-Anonymity Calculator")

file_button0 = tk.Button(root, text="Посчитать К-анонимити", command=calculate_k_anonymity)
file_button1 = tk.Button(root, text="Обезличить датасет")
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

