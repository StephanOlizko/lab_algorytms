import random

seat_prices = {
    # Поезда «Сапсан»
    'Сапсан': {
        '1Р': 1000,
        '1В': 800,
        '1С': 1200,
        '2С': 500,
        '2В': 600,
        '2E': 0,  # Цена включена в стоимость билета
    },
    # Поезда «Стриж»
    'Стриж': {
        '1Е': 1500,
        '1Р': 700,
        '2С': 400,
    },
    # Поезда стандартного типа
    'Стандарт': {
        '1С': 300,
        '1Р': 350,
        '1В': 400,
        '2Р': 450,
        '2Е': 200,
        '3Э': 250,
        '2Э': 600,
        '1Б': 1000,
        '1Л': 1100,
        '1А': 1200,
        '1И': 1200,
    }
}

def generate_random_seat(train_number):
    # Извлекаем тип поезда из номера поезда
    train_type = None
    train_number = int(train_number[:-2:])
    if 1 <= train_number <= 750:
        train_type = 'Стандарт'
    elif 751 <= train_number <= 770:
        train_type = 'Сапсан'
    elif 771 <= train_number <= 788:
        train_type = 'Стриж'

    if train_type:
        # Выбираем случайный тип вагона из доступных для данного типа поезда
        available_seats = list(seat_prices[train_type].keys())
        selected_seat = random.choice(available_seats)

        # Генерируем случайный номер вагона
        wagon_number = random.randint(1, 50)

        # Вычисляем стоимость места
        seat_price = seat_prices[train_type][selected_seat]

        return f"{wagon_number}-{selected_seat}", seat_price

    return None, None  # В случае неправильного номера
