#hashcat -m 0 -a 3 -O -o C:\Users\Пользователь\Documents\py\algor_lab\Lab-Algorytms\decryption\cracked.txt C:\Users\Пользователь\Documents\py\algor_lab\Lab-Algorytms\decryption\hashes.txt -1 89 ?1?d?d?d?d?d?d?d?d?d?d


# Чтение данных из файла
with open('cracked.txt', 'r') as file:
    lines = file.readlines()

known_numpers = [89867653009,
89167569880,
89161111524,
89866508295,
89859971245,
]


# Создание словаря для хранения хэшей и соответствующих чисел
numbers_salt = set()
for line in lines:
    parts = line.strip().split(':')
    number = int(parts[1])
    numbers_salt.add(number)
# Находим наибольшее известное число
max_known_number = max(known_numpers)

# Находим максимальное значение, которое может быть добавлено к числу, чтобы не изменить количество разрядов
max_possible_addition = 99999999999 - max_known_number

# Находим число, которое нужно добавить к каждому номеру
print(max_possible_addition)

global_salt = -1

for salt in range(0, max_possible_addition+1):
    flg = True
    n = 0
    if salt % 5000000 == 0:
        print(salt/max_possible_addition * 100)

    for num in known_numpers:
        if num + salt not in numbers_salt:
            flg = False
            break
        else:
            n += 1
            print("One is in!", salt, n)
            pass
    
    if flg:
        global_salt = salt
        break
result_numbers = [i - global_salt for i in numbers_salt]

print(global_salt)

# Записываем номера телефонов без прибавленного числа в output.txt
with open('output.txt', 'w') as output_file:
    for number in result_numbers:
        output_file.write(str(number) + '\n')
