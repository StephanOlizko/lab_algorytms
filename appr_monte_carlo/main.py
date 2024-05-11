import random
import sympy
import matplotlib.pyplot as plt
import numpy as np
from sympy import symbols
import streamlit as st
import pandas

# Игнорирование предупреждений от pyplot
import warnings
warnings.filterwarnings("ignore")

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

conditions = ["-x**2 + y**3 <2", "x - y < 1", "-2 < x", "x < 2", "-2 < y", "y < 2"]

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

    return plt

# Вычисление определенного интеграла методом Монте-Карло
def monte_carlo_integrate(f, a, b, n):
    x = np.random.uniform(a, b, n)
    y = np.random.uniform(0, f(x).max(), n)

    area = (b - a) * f(x).max()
    integral = area * (y < f(x)).sum() / n

    return integral



def main():
    st.title("Monte Carlo Simulation")

    tab = st.sidebar.selectbox("Choose a tab", ["Area", "Integral"])

    if tab == "Area":
        conditions_input = st.text_input("Enter conditions (comma separated):", "-x**2 + y**3 <2, x - y < 1, -2 < x, x < 2, -2 < y, y < 2")

        n = st.number_input("Enter number of random points:", min_value=1000, max_value=1000000, step=1000)

        if st.button("Calculate"):
            conditions = conditions_input.split(',')
            conditions = [inequality_to_lambda(condition) for condition in conditions]

            # Выбор n

            # Вычисление площади фигуры
            area = calculate_area(n, conditions)
            st.write(f"Area of the figure:", area)

            # Отображение графика
            st.pyplot(plot_figure(conditions))

    if tab == "Integral":

        n = st.number_input("Enter number of random points:", min_value=1000, max_value=1000000, step=1000)

        # Напиши какой интеграл вычисляется
        st.write("Calculating integral of cos(x) from -pi/2 to pi/2")

        if st.button("Calculate"):
            # Вычисление интеграла
            x = symbols('x')
            f = lambda x: np.cos(x)
            a = -np.pi / 2
            b = np.pi / 2
            integral = monte_carlo_integrate(f, a, b, n)
            st.write(f"Integral:", integral)
            st.write(f"Analytic integral:", float(sympy.integrate(sympy.cos(x), (x, a, b))))
            # Вывод относительной погрешности
            integral_analytic = sympy.integrate(sympy.cos(x), (x, a, b))
            relative_error = abs(integral - integral_analytic) / integral_analytic
            st.write(f"Relative error:", float(relative_error))

            # Сравните результат со значением, полученным аналитическим путем при значениях N=10, 100, 1000, 10000, 100000, 1000000. Выразите относительную погрешность метода Монте-Карло при каждом значении N.
            n_values = [10, 100, 1000, 10000, 100000, 1000000]
            results = []
            for n in n_values:
                integral = monte_carlo_integrate(f, a, b, n)
                relative_error = abs(integral - integral_analytic) / integral_analytic
                results.append([n, integral, integral_analytic, relative_error])

            df = pandas.DataFrame(results, columns=["n", "Monte Carlo integral", "Analytic integral", "Relative error"])
            st.write(df)
            

if __name__ == "__main__":
    main()