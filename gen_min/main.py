import tkinter as tk
from tkinter import ttk, messagebox
from functools import partial
from threading import Thread
import time
import random

class Individual:
    """
    Инициализация особи.

    Args:
        genotype (list): Генотип особи.
    """
    def __init__(self, genotype):
        self.genotype = genotype
        self.fitness = None  # Значение функции приспособленности

    # Определение строкового типа
    def __str__(self) -> str:
        return f"{self.genotype} | {self.fitness}"

    # Определение операторов сравнения
    def __lt__(self, other):
        if isinstance(other, Individual):
            return self.fitness < other.fitness
        return NotImplemented

    def __le__(self, other):
        if isinstance(other, Individual):
            return self.fitness <= other.fitness
        return NotImplemented

    def __eq__(self, other):
        if isinstance(other, Individual):
            return self.fitness == other.fitness
        return NotImplemented

    def __ne__(self, other):
        if isinstance(other, Individual):
            return self.fitness != other.fitness
        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, Individual):
            return self.fitness > other.fitness
        return NotImplemented

    def __ge__(self, other):
        if isinstance(other, Individual):
            return self.fitness >= other.fitness
        return NotImplemented


def initialize_population(population_size, encoding, search_space):
    """
    Инициализация начальной популяции.

    Args:
        population_size (int): Размер популяции.
        encoding (str): Тип кодировки ('binary' или 'real').
        search_space (list): Границы поиска для каждой переменной.

    Returns:
        list: Список особей (экземпляров класса Individual).
    """
    population = []
    for _ in range(population_size):
        genotype = generate_genotype(encoding, search_space)
        individual = Individual(genotype)
        calculate_fitness(individual, encoding)
        population.append(individual)
    return population


def generate_random_binary_for_objects(num_objects):
    """
    Генерация случайного бинарного числа для кодирования указанного числа объектов.

    Args:
        num_objects (int): Количество объектов.

    Returns:
        str: Случайное бинарное число.
    """
    if num_objects <= 0:
        raise ValueError("Количество объектов должно быть положительным числом.")

    num_bits = 1
    while 2 ** num_bits < num_objects:
        num_bits += 1

    return "".join(str(random.randint(0, 1)) for _ in range(num_bits))


def is_point_within_bounds(point, search_space):
    """
    Проверяет, находится ли точка в заданных границах.

    Args:
        point (tuple): Координаты точки.
        search_space (list): Границы поиска для каждой переменной.

    Returns:
        bool: True, если точка находится в границах, иначе False.
    """
    for coordinate, bounds in zip(point, search_space):
        if not bounds[0] <= coordinate <= bounds[1]:
            return False
    return True


def generate_genotype(encoding, search_space):
    """
    Генерация генотипа в соответствии с выбранной кодировкой.

    Args:
        encoding (str): Тип кодировки ('binary' или 'real').
        search_space (list): Границы поиска для каждой переменной.

    Returns:
        list: Сгенерированный генотип.
    """
    if encoding == 'binary':
        mxs = -10**10
        mns = 10**10
        flg = [mxs, mns]
        while not is_point_within_bounds(flg, search_space):
            for i in search_space:
                for j in i:
                    mxs = max(mxs, j)
                    mns = min(mns, j)

            genotype = [generate_random_binary_for_objects(mxs - mns), generate_random_binary_for_objects(mxs - mns)]
            flg = decode_genotype(genotype, encoding)

    elif encoding == 'real':
        genotype = [random.uniform(search_space[i][0], search_space[i][1]) for i in range(len(search_space))]
    else:
        raise ValueError("Неподдерживаемая кодировка")
    return genotype


def calculate_fitness(individual, encoding):
    """
    Вычисление значения функции приспособленности для особи.

    Args:
        individual (Individual): Особь, для которой вычисляется приспособленность.
        encoding (str): Тип кодировки ('binary' или 'real').
    """
    x, y = decode_genotype(individual.genotype, encoding)
    fitness = 4 * (x - 5)**2 + (y - 6)**2
    individual.fitness = fitness


def decode_genotype(genotype, encoding):
    """
    Декодирование генотипа в соответствии с выбранной кодировкой.

    Args:
        genotype (list): Генотип для декодирования.
        encoding (str): Тип кодировки ('binary' или 'real').

    Returns:
        tuple: Координаты точки.
    """
    if encoding == "real":
        x = genotype[0]
        y = genotype[1]
        return x, y
    elif encoding == "binary":
        x = int(genotype[0], 2) - int((len(genotype[0])-1)*"1", 2)
        y = int(genotype[1], 2) - int((len(genotype[0])-1)*"1", 2)
        return x, y


def tournament_selection(population, tournament_size):
    """
    Турнирная селекция для выбора особей для скрещивания.

    Args:
        population (list): Популяция особей.
        tournament_size (int): Размер турнира.

    Returns:
        tuple: Выбранные особи для скрещивания.
    """
    selected_individuals = random.sample(population, tournament_size)
    selected_individuals.sort()
    return selected_individuals[0], selected_individuals[1]


def crossover(parent1, parent2, encoding):
    """
    Скрещивание двух особей.

    Args:
        parent1 (Individual): Родитель 1.
        parent2 (Individual): Родитель 2.
        encoding (str): Тип кодировки ('binary' или 'real').

    Returns:
        Individual: Потомок после скрещивания.
    """
    if encoding == "real":
        child_genotype = [(parent1.genotype[0] + parent2.genotype[0])/2, (parent1.genotype[1] + parent2.genotype[1])/2] 
        return Individual(child_genotype)
    else:
        crossover_point = random.randint(1, len(parent1.genotype) - 1)
        child_genotype = parent1.genotype[:crossover_point] + parent2.genotype[crossover_point:]
        return Individual(child_genotype)


def mutate(individual, mutation_rate, search_space, encoding):
    """
    Мутация генотипа особи.

    Args:
        individual (Individual): Особь, для которой происходит мутация.
        mutation_rate (float): Вероятность мутации.
        search_space (list): Границы поиска для каждой переменной.
    """
    if random.random() < mutation_rate:
        if encoding == 'binary':
            mutated_gene = random.randint(0, len(individual.genotype) - 1)
            while True:
                ind = list(individual.genotype[mutated_gene])
                mutated_gene_index = random.randint(0, len(ind) - 1)
                ind[mutated_gene_index] = '0' if ind[mutated_gene_index] == '1' else '1'
                tmp = individual
                tmp.genotype[mutated_gene] = ''.join(ind)
                decoded_values = decode_genotype(tmp.genotype, 'binary')
                if is_point_within_bounds(decoded_values, search_space):
                    individual = tmp
                    break
            
        elif encoding == 'real':
            mutated_gene = random.randint(0, len(individual.genotype) - 1)
            individual.genotype[mutated_gene] += random.uniform(-0.1, 0.1)
            individual.genotype[mutated_gene] = max(search_space[mutated_gene][0],
                                                    min(search_space[mutated_gene][1], individual.genotype[mutated_gene]))
        else:
            raise ValueError("Неподдерживаемая кодировка")


def genetic_algorithm(population_size, generations, mutation_rate, tournament_size, encoding, search_space):
    """
    Генетический алгоритм для оптимизации функции приспособленности.

    Args:
        population_size (int): Размер популяции.
        generations (int): Количество поколений.
        mutation_rate (float): Вероятность мутации.
        tournament_size (int): Размер турнира для селекции.
        encoding (str): Тип кодировки ('binary' или 'real').
        search_space (list): Границы поиска для каждой переменной.

    Returns:
        tuple: Лучший результат и его значение функции приспособленности.
    """
    population = initialize_population(population_size, encoding, search_space)

    for generation in range(generations):
        new_population = []

        population = sorted(population)[:len(population)//2]

        for _ in range(population_size // 2):
            parent1, parent2 = tournament_selection(population, tournament_size)
            child1 = crossover(parent1, parent2, encoding)
            child2 = crossover(parent1, parent2, encoding)

            calculate_fitness(child1, encoding)
            calculate_fitness(child2, encoding)

            mutate(child1, mutation_rate, search_space)
            mutate(child2, mutation_rate, search_space)

            new_population.extend([child1, child2])

        population = new_population
        
        for individual in population:
            calculate_fitness(individual, encoding)

    best_individual = min(population)
    return decode_genotype(best_individual.genotype, encoding), best_individual.fitness


class GeneticAlgorithmGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Genetic Algorithm Optimization")

        # Переменные для хранения параметров генетического алгоритма
        self.population_size_var = tk.IntVar(value=100)
        self.mutation_rate_var = tk.DoubleVar(value=0.2)
        self.tournament_size_var = tk.IntVar(value=10)
        self.encoding_var = tk.StringVar(value='real')
        self.search_space_var = tk.StringVar(value='[(-10, 10), (-10, 10)]')
        self.iterations_entry = tk.IntVar(value=10)
        self.iteration_count = 0

        # Переменные для хранения текущего состояния выполнения алгоритма
        self.running = False
        self.stop_requested = False

        # Создание и размещение элементов управления
        self.create_widgets()

    def create_widgets(self):
        # Фрейм для ввода параметров
        parameter_frame = ttk.LabelFrame(self.master, text="Параметры генетического алгоритма")
        parameter_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        ttk.Label(parameter_frame, text="Размер популяции:").grid(row=0, column=0, sticky="w")
        population_entry = ttk.Entry(parameter_frame, textvariable=self.population_size_var)
        population_entry.grid(row=0, column=1, sticky="w")

        ttk.Label(parameter_frame, text="Вероятность мутации:").grid(row=2, column=0, sticky="w")
        mutation_rate_entry = ttk.Entry(parameter_frame, textvariable=self.mutation_rate_var)
        mutation_rate_entry.grid(row=2, column=1, sticky="w")

        ttk.Label(parameter_frame, text="Размер турнира:").grid(row=3, column=0, sticky="w")
        tournament_size_entry = ttk.Entry(parameter_frame, textvariable=self.tournament_size_var)
        tournament_size_entry.grid(row=3, column=1, sticky="w")

        ttk.Label(parameter_frame, text="Тип кодировки:").grid(row=4, column=0, sticky="w")
        encoding_combobox = ttk.Combobox(parameter_frame, textvariable=self.encoding_var, values=['real', 'binary'])
        encoding_combobox.grid(row=4, column=1, sticky="w")

        ttk.Label(parameter_frame, text="Границы поиска:").grid(row=5, column=0, sticky="w")
        search_space_entry = ttk.Entry(parameter_frame, textvariable=self.search_space_var)
        search_space_entry.grid(row=5, column=1, sticky="w")

        # Фрейм для кнопок
        button_frame = ttk.Frame(self.master)
        button_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        start_button = ttk.Button(button_frame, text="Старт", command=self.start_algorithm)
        start_button.grid(row=0, column=0, padx=5)

        stop_button = ttk.Button(button_frame, text="Стоп", command=self.stop_algorithm)
        stop_button.grid(row=0, column=1, padx=5)

        iterations_entry = ttk.Entry(button_frame, textvariable=self.iterations_entry)
        iterations_entry.grid(row=0, column=2, padx=5)

        run_iterations_button = ttk.Button(button_frame, text="Выполнить итерации", command=self.run_iterations)
        run_iterations_button.grid(row=0, column=3, padx=5)

        # Фрейм для вывода результатов
        result_frame = ttk.LabelFrame(self.master, text="Результаты")
        result_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

        # Создание таблицы для отображения популяции
        columns = ("Номер особи", "Геном особи", "Значение приспособленности")
        self.population_tree = ttk.Treeview(result_frame, columns=columns, show="headings")
        for col in columns:
            self.population_tree.heading(col, text=col)
        self.population_tree.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Скроллбар для таблицы
        scrollbar = ttk.Scrollbar(result_frame, orient="vertical", command=self.population_tree.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.population_tree.configure(yscrollcommand=scrollbar.set)

        # Фрейм для вывода лучшего результата
        best_result_frame = ttk.LabelFrame(self.master, text="Лучший результат")
        best_result_frame.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")

        ttk.Label(best_result_frame, text="Координаты точки:").grid(row=0, column=0, sticky="w")
        self.best_result_label = ttk.Label(best_result_frame, text="")
        self.best_result_label.grid(row=0, column=1, sticky="w")

        ttk.Label(best_result_frame, text="Значение функции:").grid(row=1, column=0, sticky="w")
        self.best_fitness_label = ttk.Label(best_result_frame, text="")
        self.best_fitness_label.grid(row=1, column=1, sticky="w")

        iteration_frame = ttk.Frame(self.master)
        iteration_frame.grid(row=4, column=0, padx=10, pady=10, sticky="nsew")

        ttk.Label(iteration_frame, text="Количество итераций:").grid(row=0, column=0, sticky="w")
        self.iteration_label = ttk.Label(iteration_frame, text="0")
        self.iteration_label.grid(row=0, column=1, sticky="w")

    def start_algorithm(self):
        if not self.running:
            # Проверка ввода параметров
            try:
                population_size = int(self.population_size_var.get())
                generations = int(self.generations_var.get())
                mutation_rate = float(self.mutation_rate_var.get())
                tournament_size = int(self.tournament_size_var.get())
                encoding = self.encoding_var.get()
                search_space = eval(self.search_space_var.get())
            except ValueError:
                messagebox.showerror("Ошибка", "Пожалуйста, введите корректные значения параметров.")
                return

            # Запуск генетического алгоритма в отдельном потоке
            self.running = True
            self.stop_requested = False
            Thread(target=self.run_genetic_algorithm, args=(population_size, generations, mutation_rate,
                                                            tournament_size, encoding, search_space)).start()
    
    def run_genetic_algorithm(self, population_size, generations, mutation_rate, tournament_size, encoding, search_space):
        try:
            # Инициализация популяции
            population = initialize_population(population_size, encoding, search_space)

            for generation in range(generations):
                if self.stop_requested:
                    break

                new_population = []

                population = sorted(population)[:len(population)//2]

                for _ in range(population_size // 2):
                    parent1, parent2 = tournament_selection(population, tournament_size)
                    child1 = crossover(parent1, parent2, encoding)
                    child2 = crossover(parent1, parent2, encoding)

                    calculate_fitness(child1, encoding)
                    calculate_fitness(child2, encoding)

                    mutate(child1, mutation_rate, search_space, encoding)
                    mutate(child2, mutation_rate, search_space, encoding)

                    new_population.extend([child1, child2])

                population = new_population

                # Обновление таблицы с популяцией
                self.update_population_table(population, encoding)

                # Обновление лучшего результата
                best_individual = min(population)
                decoded_result = decode_genotype(best_individual.genotype, encoding)
                self.update_best_result_label(decoded_result, best_individual.fitness)

                # Пауза для обновления интерфейса
                time.sleep(0.01)

                self.iteration_count += 1
                self.iteration_label.config(text=str(self.iteration_count))

            # Алгоритм завершил выполнение
            self.running = False
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка: {str(e)}")
            self.running = False

    def stop_algorithm(self):
        # Запрос остановки алгоритма
        self.stop_requested = True

    def run_iterations(self):
        if not self.running:
            # Проверка ввода параметров
            try:
                population_size = int(self.population_size_var.get())
                mutation_rate = float(self.mutation_rate_var.get())
                tournament_size = int(self.tournament_size_var.get())
                encoding = self.encoding_var.get()
                search_space = eval(self.search_space_var.get())
                iterations = int(self.iterations_entry.get())
            except ValueError:
                messagebox.showerror("Ошибка", "Пожалуйста, введите корректные значения параметров.")
                return

            # Запуск генетического алгоритма в отдельном потоке
            self.running = True
            self.stop_requested = False
            Thread(target=self.run_specified_iterations_thread, args=(iterations, population_size, mutation_rate,
                                                                      tournament_size, encoding, search_space)).start()

    def run_specified_iterations_thread(self, iterations, population_size, mutation_rate, tournament_size, encoding, search_space):
        try:
            # Инициализация популяции
            population = initialize_population(population_size, encoding, search_space)

            for _ in range(iterations):
                if self.stop_requested:
                    break

                new_population = []

                population = sorted(population)[:len(population)//2]

                for _ in range(population_size // 2):
                    parent1, parent2 = tournament_selection(population, tournament_size)
                    child1 = crossover(parent1, parent2, encoding)
                    child2 = crossover(parent1, parent2, encoding)

                    calculate_fitness(child1, encoding)
                    calculate_fitness(child2, encoding)

                    mutate(child1, mutation_rate, search_space, encoding)
                    mutate(child2, mutation_rate, search_space, encoding)

                    new_population.extend([child1, child2])

                population = new_population

                # Обновление таблицы с популяцией

                # Обновление лучшего результата
                best_individual = min(population)
                decoded_result = decode_genotype(best_individual.genotype, encoding)
                self.update_best_result_label(decoded_result, best_individual.fitness)

                # Пауза для обновления интерфейса

                self.iteration_count += 1
                self.iteration_label.config(text=str(self.iteration_count))

            # Алгоритм завершил выполнение
            self.update_population_table(population, encoding)
            print(decode_genotype(best_individual.genotype, encoding), best_individual.fitness)
            self.running = False
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка: {str(e)}")
            self.running = False

    def update_population_table(self, population, encoding):
        # Очистка таблицы
        for item in self.population_tree.get_children():
            self.population_tree.delete(item)

        # Заполнение таблицы
        for i, individual in enumerate(population, start=1):
            decoded_genome = decode_genotype(individual.genotype, encoding)
            fitness_value = round(individual.fitness, 6)
            self.population_tree.insert("", "end", values=(i, decoded_genome, fitness_value))

    def update_best_result_label(self, decoded_result, fitness):
        self.best_result_label.config(text=f"Координаты точки: {decoded_result}")
        self.best_fitness_label.config(text=f"Значение функции: {round(fitness, 6)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = GeneticAlgorithmGUI(root)
    root.mainloop()
