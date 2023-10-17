import csv
import random
import Test_timetable
from person_gen import generate_person
from seat_gen import generate_random_seat

# Загрузка данных о рейсах из файла timetable.txt
def load_timetable(filename):
    timetable_data = []
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            parts = line.strip().split(';')
            # Проверяем наличие минимального количества данных
            train_number = parts[0]
            departure = parts[1]
            destination = parts[2]
            departure_date = parts[3]
            arrival_date = parts[4]
            ticket_price = float(parts[5])
            timetable_data.append((train_number, departure, destination, departure_date, arrival_date, ticket_price))
    return timetable_data

# Генерация базы данных билетов и сохранение в CSV
def generate_tickets_csv(timetable_data, num_tickets, output_filename):
    with open(output_filename, 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["ФИО", "Паспортные данные", "Откуда", "Куда", "Дата отъезда", "Дата приезда", "Рейс", "Выбор вагона и места", "Стоимость", "Карта оплаты"])
        seat_data = {}  # Словарь для отслеживания занятых мест по рейсу и дате отправления

        for _ in range(num_tickets):
            # Выбор случайного рейса
            train_info = random.choice(timetable_data)
            train_number, departure, destination, departure_date, arrival_date, ticket_price = train_info

            # Генерация случайного выбора вагона и места
            seat_choice, additional_pr = generate_random_seat(train_number)

            # Проверяем, что выбранное место на данном рейсе и дате отправления не занято
            while (train_number, departure_date, seat_choice) in seat_data:
                seat_choice, additional_pr = generate_random_seat(train_number)

            # Регистрируем место как занятое на этом рейсе и дате отправления
            seat_data[(train_number, departure_date, seat_choice)] = True

            # Генерация данных о пассажире
            person_data = generate_person()
            full_name = f"{person_data[0]} {person_data[1]} {person_data[2]}"
            passport_data = f"{person_data[3]} {person_data[4]}"

            # Запись данных в CSV
            csv_writer.writerow([full_name, passport_data, departure, destination, departure_date, arrival_date, train_number, seat_choice, ticket_price + additional_pr, person_data[5]])


timetable_data = load_timetable("timetable.txt")
print("Введите количество строк:")
with open("num_tickets.txt") as f:
    num_tickets = int(f.readline())
output_filename = "tickets.csv"
generate_tickets_csv(timetable_data, num_tickets, output_filename)
print(f"Сгенерировано {num_tickets} билетов и сохранено в файл {output_filename}.")
