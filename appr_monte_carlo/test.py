import random
import sympy
import matplotlib.pyplot as plt
import numpy as np
from sympy import symbols


# Функция создания условия которая возвращает функцию проверки на принадлежность точки фигуре
def inequality_to_lambda(inequality_str):
    # Парсинг неравенства
    inequality = sympy.sympify(inequality_str)

    # Получение переменных из неравенства
    variables = ["x", "y"]
    variables_str = [str(var) for var in variables]

    # Преобразование неравенства в лямбда-функцию
    inequality_lambda = sympy.lambdify(variables_str, inequality)

    return inequality_lambda

def is_inside_figure(x, y, conditions):
    return all(condition(x, y) for condition in conditions)

def calculate_area(n, conditions=[], x_border=(-2, 2), y_border=(-2, 2)):
    x_min, x_max = x_border
    y_min, y_max = y_border

    area = 0
    for _ in range(n):
        x = random.uniform(x_min, x_max)
        y = random.uniform(y_min, y_max)

        if is_inside_figure(x, y, conditions):
            area += 1

    area /= n
    area *= (x_max - x_min) * (y_max - y_min)

    return area

# Example usage
n = 1000000  # Number of random points

conditions = ["-x**2 + y**3 <2", "x - y < 1", "-2 < x", "x < 2", "-2 < y", "y < 2"]
conditions = [inequality_to_lambda(condition) for condition in conditions]

#area = calculate_area(n, conditions)

# Построим фигуру на плоскости
# Функция для построения графика 

def plot_figure(conditions, x_border=(-2, 2), y_border=(-2, 2)):
    x_min, x_max = x_border
    y_min, y_max = y_border

    x = np.linspace(x_min, x_max, 100)
    y = np.linspace(y_min, y_max, 100)
    X, Y = np.meshgrid(x, y)

    Z = np.zeros_like(X, dtype=bool)
    for i in range(len(x)):
        for j in range(len(y)):
            Z[j, i] = is_inside_figure(x[i], y[j], conditions)

    plt.contourf(X, Y, Z, levels=[0, 0.5, 1], colors=["white", "black"])
    plt.xlim(x_min, x_max)
    plt.ylim(y_min, y_max)
    plt.gca().set_aspect("equal")

    plt.show()

# Вычисление определенного интеграла методом Монте-Карло
def monte_carlo_integrate(f, a, b, n):
    x = np.random.uniform(a, b, n)
    y = np.random.uniform(0, f(x).max(), n)

    area = (b - a) * f(x).max()
    integral = area * (y < f(x)).sum() / n

    return integral

# Example usage
x = symbols('x')
# int from -pi/2, pi/2  cos(x) dx
f = lambda x: np.cos(x)
a = -np.pi / 2
b = np.pi / 2
n = 1000000

integral = monte_carlo_integrate(f, a, b, n)
print(integral)

# ВЫчисление той же функции аналитически
integral_analytic = sympy.integrate(sympy.cos(x), (x, a, b))
print(integral_analytic)

# Выразить относительную погрешность
relative_error = abs(integral - integral_analytic) / integral_analytic

print(relative_error)