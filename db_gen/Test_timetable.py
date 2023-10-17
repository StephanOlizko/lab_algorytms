import random
import math
from datetime import datetime, timedelta


def calculate_the_distance( φA, λA, φB, λB ):
    EARTH_RADIUS = 6372795

    # Перевести координаты в радианы
    lat1 = math.radians(φA)
    lat2 = math.radians(φB)
    long1 = math.radians(λA)
    long2 = math.radians(λB)

    # Косинусы и синусы широт и разницы долгот
    cl1 = math.cos(lat1)
    cl2 = math.cos(lat2)
    sl1 = math.sin(lat1)
    sl2 = math.sin(lat2)
    delta = long2 - long1
    cdelta = math.cos(delta)
    sdelta = math.sin(delta)

    # Вычисления длины большого круга
    y = math.sqrt(math.pow(cl2 * sdelta, 2) + math.pow(cl1 * sl2 - sl1 * cl2 * cdelta, 2))
    x = sl1 * sl2 + cl1 * cl2 * cdelta

    ad = math.atan2(y, x)
    dist = ad * EARTH_RADIUS

    return dist


def determine_direction( lat1, lon1, lat2, lon2 ):
    if lat2 >= lat1 or lon2 >= lon1:
        return "Юго-Восток"
    else:
        return "Северо-Запад"


def determine_train_speed( train_number ):
    if 1 <= train_number <= 150:
        return 70  # Скорые поезда (70 км/ч)
    elif 151 <= train_number <= 300:
        return 70  # Скорые поезда сезонного/разового назначения (70 км/ч)
    elif 301 <= train_number <= 450:
        return 60  # Пассажирские круглогодичные поезда (60 км/ч)
    elif 451 <= train_number <= 700:
        return 60  # Пассажирские поезда сезонного/разового назначения (60 км/ч)
    elif 701 <= train_number <= 750:
        return 91  # Скоростные поезда (91 км/ч)
    elif 751 <= train_number <= 788:
        return 161  # Высокоскоростные поезда (161 км/ч)
    else:
        return 100  # Другие номера поездов (например, 0 км/ч)


def generate_odd_numbers( n, x ):
    odd_numbers = [num for num in range(1, x + 1) if num % 2 != 0]
    if x % 2 == 0:
        x -= 1
    if n > len(odd_numbers):
        raise ValueError("Заданное значение n больше количества доступных нечетных чисел.")
    selected_numbers = random.sample(odd_numbers, n)

    return selected_numbers


station_data = []
with open('RZD_stations1.txt', 'r', encoding='utf-8') as station_file:
    for line in station_file:
        parts = line.strip().split()
        if len(parts) >= 3:
            station_name = ' '.join(parts[:-2])
            latitude = float(parts[-2])
            longitude = float(parts[-1])
            station_data.append((station_name, latitude, longitude))

russian_alphabet = 'АБВГДЕЖЗИКЛМНОПРСТУФХЧШЭЮЯ'

# Генерация расписания
num_trains = 75  # Количество поездов
start_date = datetime(2023, 1, 1)  # Начальная дата
end_date = datetime(2023, 12, 31)  # Конечная дата
timetable = []
interval_between_trips = 3

# Скорость поезда (100 км/ч в метрах в секунду)
train_speed_mps = 100 * 1000 / 3600

for train_number in generate_odd_numbers(num_trains, 788):
    random_letter = random.choice(russian_alphabet)
    random_letter_rev = random.choice(russian_alphabet)

    train_speed_mps = determine_train_speed(train_number)

    # Выбор случайных точек из stations_data
    station1, lat1, lon1 = random.choice(station_data)
    station2, lat2, lon2 = random.choice(station_data)

    # Определение направления между точками
    direction = determine_direction(lat1, lon1, lat2, lon2)

    # Проверка на конфликт направления с номером поезда
    is_even = train_number % 2 == 0
    if (is_even and direction == "Северо-Запад") or (not is_even and direction == "Юго-Восток"):
        # Если есть конфликт, меняем точки местами
        station1, lat1, lon1, station2, lat2, lon2 = station2, lat2, lon2, station1, lat1, lon1

    # Вычисление расстояния между станциями
    distance = calculate_the_distance(lat1, lon1, lat2, lon2)

    # Вычисление времени в пути
    travel_time_seconds = distance / train_speed_mps
    cost = distance // 1000 * 2
    # Случайное время отправления
    if 151 <= train_number <= 300 or 451 <= train_number <= 700:
        rnmonth = random.randint(1, 9)
        start_date = datetime(2023, rnmonth, 1)
        departure_time = start_date + timedelta(
            seconds=random.randint(0, 24 * 60 * 60))
        end_date = datetime(2023, rnmonth + 2, 30)
    else:
        departure_time = start_date + timedelta(days=random.randint(0, 30),
                                                seconds=random.randint(0, 24 * 60 * 60))

    while departure_time <= end_date:
        arrival_time = departure_time + timedelta(seconds=travel_time_seconds)

        # Создание строки расписания с датой и временем
        timetable_line = f"{train_number}{random_letter} ; {station1}" \
                         f" ; {station2} ;" \
                         f" {departure_time.strftime('%Y-%m-%d-%H:%M')} ; {arrival_time.strftime('%Y-%m-%d-%H:%M')} ;" \
                         f" {cost}"

        timetable.append(timetable_line)

        # Создание строки расписания для маршрута B->A (обратного)
        reverse_train_number = train_number + 1 if train_number % 2 == 1 else train_number - 1
        reverse_departure_time = arrival_time + timedelta(minutes=random.randint(30, 180))
        reverse_arrival_time = reverse_departure_time + timedelta(seconds=travel_time_seconds)

        reverse_timetable_line = f"{reverse_train_number}{random_letter_rev} ; {station2}" \
                                 f" ; {station1} ;" \
                                 f" {reverse_departure_time.strftime('%Y-%m-%d-%H:%M')} ; {reverse_arrival_time.strftime('%Y-%m-%d-%H:%M')} ;" \
                                 f" {cost}"

        timetable.append(reverse_timetable_line)

        # Увеличиваем время отправления на интервал между рейсами
        departure_time += timedelta(days=interval_between_trips)

    end_date = datetime(2023, 12, 31)

# Запись расписания в файл
output_file = open('timetable.txt', 'w', encoding='utf-8')
for line in timetable:
    output_file.write(line + '\n')
output_file.close()

print("Годовое расписание поездов сгенерировано и записано в файл 'timetable.txt'.")
