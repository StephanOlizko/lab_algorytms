import tkinter as tk
from tkinter import ttk, messagebox
from threading import Thread
import time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure



class Particle:
    def __init__(self, bounds):
        """
        Инициализация частицы.

        Args:
            bounds (list): Границы поиска для каждой переменной в виде списка пар (минимум, максимум).
        """
        # Инициализация частицы
        self.position = np.random.uniform(bounds[0][0], bounds[0][1], 2)  # Начальная позиция в пределах границ
        self.velocity = np.random.rand(2)  # Начальная скорость
        self.best_position = self.position.copy()  # Начальная лучшая позиция
        self.best_fitness = float('inf')  # Начальное лучшее значение функции

def objective_function(x, y):
    """
    Целевая функция для оптимизации.

    Args:
        x (float): Значение переменной x.
        y (float): Значение переменной y.

    Returns:
        float: Значение функции в заданных точках.
    """
    return 4 * (x - 5) ** 2 + (y - 6) ** 2

def update_velocity(particle, global_best_position, inertia_weight, c1, c2):
    """
    Обновление скорости частицы.

    Args:
        particle (Particle): Частица, для которой обновляется скорость.
        global_best_position (numpy.ndarray): Глобальная лучшая позиция в пространстве.
        inertia_weight (float): Коэффициент инерции.
        c1 (float): Коэффициент когнитивного влияния.
        c2 (float): Коэффициент социального влияния.

    Returns:
        numpy.ndarray: Новая скорость частицы.
    """
    inertia_term = inertia_weight * particle.velocity
    cognitive_term = c1 * np.random.rand() * (particle.best_position - particle.position)
    social_term = c2 * np.random.rand() * (global_best_position - particle.position)

    new_velocity = inertia_term + cognitive_term + social_term
    return new_velocity

def run_swarm_algorithm(population_size, generations, bounds, inertia_weight, c1, c2):
    """
    Запуск алгоритма роя частиц для оптимизации функции.

    Args:
        population_size (int): Размер популяции.
        generations (int): Количество поколений.
        bounds (list): Границы поиска для каждой переменной в виде списка пар (минимум, максимум).
        inertia_weight (float): Коэффициент инерции.
        c1 (float): Коэффициент когнитивного влияния.
        c2 (float): Коэффициент социального влияния.

    Returns:
        tuple: Глобальная лучшая позиция и соответствующее значение функции, поауляция (для вывода на график)
    """
    population = [Particle(bounds) for _ in range(population_size)]  # Инициализация популяции
    global_best_position = None
    global_best_fitness = float('inf')

    for _ in range(generations):
        for particle in population:
            x, y = particle.position
            fitness = objective_function(x, y)

            if fitness < particle.best_fitness:
                particle.best_fitness = fitness
                particle.best_position = particle.position.copy()

            if fitness < global_best_fitness:
                global_best_fitness = fitness
                global_best_position = particle.position.copy()

        for particle in population:
            particle.velocity = update_velocity(particle, global_best_position, inertia_weight, c1, c2)
            particle.position += particle.velocity
            particle.position = np.clip(particle.position, bounds[0][0], bounds[0][1])

    print(global_best_position, global_best_fitness)
    return global_best_position, global_best_fitness, population


class SwarmAlgorithmGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Swarm Algorithm Optimization")

        # Переменные для хранения параметров роевого алгоритма
        self.population_size_var = tk.IntVar(value=20)
        self.generations_var = tk.IntVar(value=100)
        self.inertia_weight_var = tk.DoubleVar(value=0.5)
        self.c1_var = tk.DoubleVar(value=1.5)
        self.c2_var = tk.DoubleVar(value=1.5)
        self.bounds_var = tk.StringVar(value="[(-10, 10), (-10, 10)]")
        self.iterations_var = tk.IntVar(value=10)

        # Переменные для хранения текущего состояния выполнения алгоритма
        self.running = False
        self.stop_requested = False

        # Создание и размещение элементов управления
        self.create_widgets()

    def create_widgets(self):
        # Фрейм для ввода параметров
        parameter_frame = ttk.LabelFrame(self.master, text="Параметры роевого алгоритма")
        parameter_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Label и Entry для размера популяции
        ttk.Label(parameter_frame, text="Размер популяции:").grid(row=0, column=0, sticky="w")
        population_entry = ttk.Entry(parameter_frame, textvariable=self.population_size_var)
        population_entry.grid(row=0, column=1, sticky="w")

        # Label и Entry для коэффициента инерции
        ttk.Label(parameter_frame, text="Коэффициент инерции:").grid(row=2, column=0, sticky="w")
        inertia_weight_entry = ttk.Entry(parameter_frame, textvariable=self.inertia_weight_var)
        inertia_weight_entry.grid(row=2, column=1, sticky="w")

        # Label и Entry для коэффициента когнитивного влияния
        ttk.Label(parameter_frame, text="Коэффициент когнитивного влияния:").grid(row=3, column=0, sticky="w")
        c1_entry = ttk.Entry(parameter_frame, textvariable=self.c1_var)
        c1_entry.grid(row=3, column=1, sticky="w")

        # Label и Entry для коэффициента социального влияния
        ttk.Label(parameter_frame, text="Коэффициент социального влияния:").grid(row=4, column=0, sticky="w")
        c2_entry = ttk.Entry(parameter_frame, textvariable=self.c2_var)
        c2_entry.grid(row=4, column=1, sticky="w")

        # Label и Entry для границ поиска
        ttk.Label(parameter_frame, text="Границы поиска:").grid(row=5, column=0, sticky="w")
        bounds_entry = ttk.Entry(parameter_frame, textvariable=self.bounds_var)
        bounds_entry.grid(row=5, column=1, sticky="w")

        # Фрейм для кнопок
        button_frame = ttk.Frame(self.master)
        button_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        # Entry и кнопка для количества итераций
        iterations_entry = ttk.Entry(button_frame, textvariable=self.iterations_var)
        iterations_entry.grid(row=0, column=2, padx=5)

        run_iterations_button = ttk.Button(button_frame, text="Выполнить итерации", command=self.run_iterations)
        run_iterations_button.grid(row=0, column=3, padx=5)

        # Фрейм для вывода результатов
        result_frame = ttk.LabelFrame(self.master, text="Результаты")
        result_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

        # Создание и размещение графика
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=result_frame)
        self.canvas.get_tk_widget().pack()

        # Фрейм для вывода лучшего результата
        best_result_frame = ttk.LabelFrame(self.master, text="Лучший результат")
        best_result_frame.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")

        # Label для координат лучшей точки
        ttk.Label(best_result_frame, text="Координаты точки:").grid(row=0, column=0, sticky="w")
        self.best_result_label = ttk.Label(best_result_frame, text="")
        self.best_result_label.grid(row=0, column=1, sticky="w")

        # Label для значения функции в лучшей точке
        ttk.Label(best_result_frame, text="Значение функции:").grid(row=1, column=0, sticky="w")
        self.best_fitness_label = ttk.Label(best_result_frame, text="")
        self.best_fitness_label.grid(row=1, column=1, sticky="w")

    def run_iterations(self):
        # Проверка, что алгоритм не выполняется в данный момент
        if not self.running:
            # Проверка ввода параметров
            try:
                population_size = int(self.population_size_var.get())
                inertia_weight = float(self.inertia_weight_var.get())
                c1 = float(self.c1_var.get())
                c2 = float(self.c2_var.get())
                bounds = eval(self.bounds_var.get())
                iterations = int(self.iterations_var.get())
            except ValueError:
                messagebox.showerror("Ошибка", "Пожалуйста, введите корректные значения параметров.")
                return

            # Запуск роевого алгоритма с указанным числом итераций
            self.running = True
            self.stop_requested = False
            Thread(target=self.run_specified_iterations, args=(iterations, population_size, inertia_weight, c1, c2, bounds)).start()

    def run_specified_iterations(self, iterations, population_size, inertia_weight, c1, c2, bounds):
        try:
            # Инициализация алгоритма роя частиц
            global_best_position, global_best_fitness, population = run_swarm_algorithm(population_size, iterations, bounds, inertia_weight, c1, c2)

            # Отображение результатов на графике
            self.display_results_on_graph(global_best_position, global_best_fitness, bounds, population)

            # Обновление лучшего результата
            self.update_best_result_label(global_best_position, global_best_fitness)

            # Алгоритм завершил выполнение
            self.running = False
        except Exception as e:
            # Обработка ошибок и вывод сообщения
            messagebox.showerror("Ошибка", f"Произошла ошибка: {str(e)}")
            self.running = False

    def display_results_on_graph(self, global_best_position, global_best_fitness, bounds, population):
        # Очистка графика
        self.ax.clear()

        # Отображение популяции
        x_values = [particle.position[0] for particle in population]
        y_values = [particle.position[1] for particle in population]
        self.ax.scatter(x_values, y_values, label="Population", alpha=0.6)

        # Отображение лучшей точки
        self.ax.scatter(global_best_position[0], global_best_position[1], color='red', label="Best Point")

        # Настройка графика
        self.ax.set_title("Swarm Algorithm Optimization")
        self.ax.set_xlabel("X-axis")
        self.ax.set_ylabel("Y-axis")
        self.ax.legend()

        # Обновление графика на tkCanvas
        self.canvas.draw()

    def update_best_result_label(self, global_best_position, global_best_fitness):
        # Обновление текста в Label для координат лучшей точки
        self.best_result_label.config(text=f"Координаты точки: {global_best_position}")
        # Обновление текста в Label для значения функции в лучшей точке
        self.best_fitness_label.config(text=f"Значение функции: {round(global_best_fitness, 6)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = SwarmAlgorithmGUI(root)
    root.mainloop()