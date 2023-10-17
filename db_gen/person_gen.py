from faker import Faker
import random
import tkinter as tk
from tkinter import ttk


fake = Faker('ru_RU')


def generate_personal_data(gender = fake.random_int(min=0, max=1)):

    if gender == 0:  # Мужской пол
        last_name = fake.last_name_male()
        first_name = fake.first_name_male()
        middle_name = fake.middle_name_male()
    else:  # Женский пол
        last_name = fake.last_name_female()
        first_name = fake.first_name_female()
        middle_name = fake.middle_name_female()

    okato_region = fake.random_int(min=1, max=99)
    year_of_issue = fake.random_int(min=0, max=23)


    passport_series = f"{okato_region:02d}{year_of_issue:02d}"
    passport_number = f"{fake.random_int(min=1, max=999999):06d}"

            
    return first_name, middle_name, last_name,passport_series, passport_number


bin_codes_oper_1 = ["VISA", "MASTERCARD", "AMERICANEXPRESS", "UNIONPAY", "MIR"]
bin_codes_bank_1 = ["ALFA-BANK", "GAZPROMBANK", "QIWI-BANK", "OTKRITIE", "RAIFFEISENBANK",
                                  "TINKOFF", "SBERBANK", "BANKOFAMERICA", "BANKOFCHINA"]

# Создаем главное окно
root = tk.Tk()
root.title("Настройки")
root.geometry("700x700") 

# Переменные
probab_flag = tk.IntVar()
num_tickets = tk.IntVar()
bin_codes_oper_w = [tk.DoubleVar() for _ in range(5)]
bin_codes_bank_w = [tk.DoubleVar() for _ in range(9)]

#probab_flag = int(input())

def start_program():
    
    if (all(var.get() == 0 for var in bin_codes_oper_w) and probab_flag.get() == 1) or (all(var.get() == 0 for var in bin_codes_bank_w)and probab_flag.get() == 2):
        # Если все значения нулевые, уведомляем пользователя
        error_label.config(text="Введите ненулевые значения!", fg="red")
    else:
        root.destroy()  # Закрываем окно интерфейса


# Функция обновления интерфейса
def update_interface(*args):
    for slider in oper_sliders:
        slider.grid_forget()
    for slider in bank_sliders:
        slider.grid_forget()
    
    if probab_flag.get() == 1:
        for i in range(5):
            oper_sliders[i].grid(row=i + 3, column=1, padx=10, pady=5)
    elif probab_flag.get() == 2:
        for i in range(9):
            bank_sliders[i].grid(row=i + 3, column=1, padx=10, pady=5)

# Создаем элементы интерфейса
description_label = tk.Label(root, text="Настройки пользователя", font=("Helvetica", 16))
description_label.grid(row=0, column=0, columnspan=2)

welcome_label = tk.Label(root, text="Добро пожаловать!", font=("Helvetica", 14))
welcome_label.grid(row=1, column=0, columnspan=2)

instructions_label = tk.Label(root, text="Вы можете настроить следующие параметры:", font=("Helvetica", 12))
instructions_label.grid(row=2, column=0, columnspan=2)

probab_label = tk.Label(root, text="Выбор по:", font=("Helvetica", 12))
probab_label.grid(row=3, column=2)
probab_slider = tk.Scale(root, from_=0, to=2, variable=probab_flag, orient="horizontal", command=update_interface)
probab_slider.grid(row=3, column=3, padx=10, pady=5, columnspan=2)

kol_label = tk.Label(root, text="Количество записей", font=("Helvetica", 12))
kol_label.grid(row=5, column=2)
kol_slider = tk.Scale(root, from_=10, to=100000, variable=num_tickets, orient="horizontal")
kol_slider.grid(row=5, column=3, padx=10, pady=5, columnspan=2)

oper_label = tk.Label(root, text="1 - банковская система (веса)", font=("Helvetica", 12))
oper_label.grid(row=4, column=0)
oper_sliders = [tk.Scale(root, from_=0, to=100, variable=bin_codes_oper_w[i], orient="horizontal", label=bin_codes_oper_1[i]) for i in range(len(bin_codes_oper_1))]

bank_label = tk.Label(root, text="2 - банк (веса)", font=("Helvetica", 12))
bank_label.grid(row=5, column=0)
bank_sliders = [tk.Scale(root, from_=0, to=100, variable=bin_codes_bank_w[i], orient="horizontal", label=bin_codes_bank_1[i]) for i in range(len(bin_codes_bank_1))]

# Добавляем кнопку
start_button = tk.Button(root, text="Запустить программу", command=start_program)
start_button.grid(row=7, column=3, columnspan=2, pady=10)


error_label = tk.Label(root, text="", font=("Helvetica", 12))
error_label.grid(row=11, column=0, columnspan=2)
# Обновляем интерфейс при запуске
update_interface()


root.mainloop()

probab_flag = probab_flag.get()
bin_codes_oper_w = [var.get() for var in bin_codes_oper_w]
bin_codes_bank_w = [var.get() for var in bin_codes_bank_w]
num_tickets = num_tickets.get()


bin_codes = list()


bin_codes_oper = [list() for i in bin_codes_oper_1]
bin_codes_bank = [list() for i in bin_codes_bank_1]

#bin_codes_oper_w = [1 for i in bin_codes_oper_1]
#bin_codes_bank_w = [1 for i in bin_codes_bank_1]

match probab_flag:
    case 0:
        with open("BIN_CODES.txt", 'r') as file:
            for line in file:
                bin_code, card_type, card_category, bank_name = line.strip().split()

                bin_codes.append(bin_code)
        
        def generate_person():
            res = []
            for i in generate_personal_data(fake.random_int(min=0, max=1)):
                res.append(i)
            card_number = fake.random_int(min=1, max=10**10-1)
            res.append(f"{bin_codes[fake.random_int(min=0, max = len(bin_codes)-1)]}" + f"{card_number:010d}")
            return res
        

    case 1:
        with open("BIN_CODES.txt", 'r') as file:
            for line in file:
                bin_code, card_type, card_category, bank_name = line.strip().split()

                bin_codes_oper[bin_codes_oper_1.index(card_type)].append(bin_code)

                bin_codes = random.choices(bin_codes_oper, weights=bin_codes_oper_w, k=1000)


        def generate_person():
            res = []
            for i in generate_personal_data(fake.random_int(min=0, max=1)):
                res.append(i)
            card_number = fake.random_int(min=1, max=10**10-1)
            bin_i = fake.random_int(min=0, max = len(bin_codes)-1)
            res.append(f"{bin_codes[bin_i][fake.random_int(min=0, max=len(bin_codes[bin_i])-1)]}" + f"{card_number:010d}")
            return res
        
            
    case 2:
        with open("BIN_CODES.txt", 'r') as file:
            for line in file:
                bin_code, card_type, card_category, bank_name = line.strip().split()

                bin_codes_bank[bin_codes_bank_1.index(bank_name)].append(bin_code)

                bin_codes = random.choices(bin_codes_bank, weights=bin_codes_bank_w, k=1000)

        def generate_person():
            res = []
            for i in generate_personal_data(fake.random_int(min=0, max=1)):
                res.append(i)
            card_number = fake.random_int(min=1, max=10**10-1)
            bin_i = fake.random_int(min=0, max = len(bin_codes)-1)
            res.append(f"{bin_codes[bin_i][fake.random_int(min=0, max=len(bin_codes[bin_i])-1)]}" + f"{card_number:010d}")
            return res



with open("num_tickets.txt", "w") as f:
    f.write(str(num_tickets))

