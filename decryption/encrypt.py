import hashlib

def hash_phone_numbers(phone_numbers, algorithm):
    hashed_numbers = []
    for phone_number in phone_numbers:
        # Преобразование номера телефона в байтовую строку перед хэшированием
        phone_number_bytes = phone_number.encode('utf-8')

        # Создание объекта хэша с выбранным алгоритмом
        hash_algorithm = hashlib.new(algorithm)
        hash_algorithm.update(phone_number_bytes)
        hashed_number = hash_algorithm.hexdigest()

        hashed_numbers.append(hashed_number)

    return hashed_numbers

def read_phone_numbers_from_file(file_path):
    with open(file_path, 'r') as file:
        phone_numbers = file.read().splitlines()
    return phone_numbers

def write_to_file(file_path, data):
    with open(file_path, 'w') as file:
        for item in data:
            file.write("%s\n" % item)

if __name__ == "__main__":
    # Чтение номеров телефонов из файла
    input_file_path = "output_ws_abc.txt"
    phone_numbers = read_phone_numbers_from_file(input_file_path)

    # Шифрование номеров телефонов с использованием разных алгоритмов
    sha1_hashed_numbers = hash_phone_numbers(phone_numbers, 'sha1')
    sha256_hashed_numbers = hash_phone_numbers(phone_numbers, 'sha256')
    sha512_hashed_numbers = hash_phone_numbers(phone_numbers, 'sha512')

    # Сохранение зашифрованных номеров в разные файлы
    write_to_file("sha1_hashed_numbers_salt.txt", sha1_hashed_numbers)
    write_to_file("sha256_hashed_numbers_salt.txt", sha256_hashed_numbers)
    write_to_file("sha512_hashed_numbers_salt.txt", sha512_hashed_numbers)

    print("Шифрование завершено. Результат сохранен в файлах.")
