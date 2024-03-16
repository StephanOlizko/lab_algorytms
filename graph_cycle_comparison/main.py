import tkinter as tk
import networkx as nx
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import random
import tkinter.ttk as ttk
import matplotlib.pyplot as plt
import math
import time

class Ant:
    def __init__(self, graph):
        self.graph = graph
        self.current_node = random.choice(list(graph.nodes))
        self.path = [self.current_node]
        self.path_length = 0

    def can_visit(self, node):
        return node not in self.path and self.graph.has_edge(self.current_node, node)

    def visit(self, node):
        self.path.append(node)
        self.path_length += self.graph[self.current_node][node]['weight']
        self.current_node = node

    def get_cycle_length(self):
        if len(self.path) == len(self.graph.nodes) + 1 and self.path[0] == self.path[-1]:
            return self.path_length
        else:
            return float('inf')

    def __str__(self) -> str:
        return f'Ant({self.path}, {self.path_length}, {self.get_cycle_length()})'

class AntColony:
    def __init__(self, graph, num_ants, decay_rate, influence):
        self.graph = graph
        self.num_ants = num_ants
        self.decay_rate = decay_rate
        self.influence = influence
        self.pheromones = {(i, j): 1 for i in graph.nodes for j in graph.nodes if i != j}
        self.ants = [Ant(graph) for _ in range(num_ants)]

    def update_pheromones(self):
        for i, j in self.pheromones.keys():
            self.pheromones[(i, j)] *= (1 - self.decay_rate)
        for ant in self.ants:
            for i in range(len(ant.path) - 1):
                self.pheromones[(ant.path[i], ant.path[i+1])] += 1 / ant.get_cycle_length()

    def choose_next_node(self, ant):
        probabilities = []
        for node in self.graph.nodes:
            if ant.can_visit(node):
                pheromone = self.pheromones[(ant.current_node, node)] ** self.influence
                distance = self.graph[ant.current_node][node]['weight'] ** (-1)
                probabilities.append([node, pheromone * distance])
            else:
                probabilities.append([node, 0])

        total = sum(prob for node, prob in probabilities)
        if total == 0:
            return None

        probabilities = [[node, prob/total] for node, prob in probabilities]
        nodes, probs = zip(*probabilities)

        return random.choices(nodes, probs)[0]

    def search(self, iterations):
        #print()
        for _ in range(iterations):
            self.ants = [Ant(self.graph) for _ in range(self.num_ants)]

            for ant in self.ants:
                while len(ant.path) < len(self.graph.nodes):
                    next_node = self.choose_next_node(ant)
                    if next_node is None:
                        break
                    ant.visit(next_node)

                if ant.path[-1] != ant.path[0]:
                    if self.graph.has_edge(ant.path[-1], ant.path[0]) and len(ant.path) == len(self.graph.nodes):
                        ant.visit(ant.path[0])
                    else:
                        ant.path_length = float('inf')

            #print(*self.ants)
            self.update_pheromones()
            #print(self.pheromones)

        return min(self.ants, key=lambda ant: ant.path_length)


def ant_hamiltonian_cycle(graph, AntNum, Evaporation, Influence, Iterations):
    hamiltonian_cycle = None

    colony = AntColony(graph, AntNum, Evaporation, Influence)
    best_ant = colony.search(Iterations)

    hamiltonian_cycle = nx.DiGraph()

    if best_ant.get_cycle_length() == float('inf'):
        hamiltonian_cycle = None
    else:
        for i in range(len(best_ant.path) - 1):
            hamiltonian_cycle.add_edge(best_ant.path[i], best_ant.path[i+1], weight=graph[best_ant.path[i]][best_ant.path[i+1]]['weight'])    


    #Проверка на валидность гамильтонова цикла (все ребра присутствуют в исходном графе)
    if hamiltonian_cycle is not None:
        for edge in hamiltonian_cycle.edges:
            if not graph.has_edge(edge[0], edge[1]):
                hamiltonian_cycle = None
                break

    # Если гамильтонов цикл не найден, выводим сообщение
    if hamiltonian_cycle is None:
        return None
    
    else:
        return hamiltonian_cycle


def nearest_neighbor_hamiltonian_cycle_add(graph):
    hamiltonian_cycle = []

    node = random.choice(list(graph.nodes()))

    hamiltonian_cycle_temp = nx.DiGraph()
    hamiltonian_cycle_temp.add_node(node)
    current_node = node
    visited_nodes = [node]

    # Пока не посетили все вершины графа
    while len(visited_nodes) < len(graph.nodes):
        min_lenght = np.inf
        next_node = None
        # Проходим по соседям текущей вершины
        for neighbor in graph.neighbors(current_node):
            lenght = graph[current_node][neighbor]['weight']
            # Если длина ребра меньше минимальной длины и соседняя вершина еще не посещена
            if lenght < min_lenght and neighbor not in visited_nodes:
                min_lenght = lenght
                next_node = neighbor
        # Если не удалось найти следующую вершину, прерываем цикл
        if next_node is None:
            break
        else:
            # Добавляем следующую вершину в гамильтонов цикл
            hamiltonian_cycle_temp.add_node(next_node)
            hamiltonian_cycle_temp.add_edge(current_node, next_node, weight=min_lenght)
            visited_nodes.append(next_node)
            current_node = next_node
    
    # Если посетили все вершины и есть ребро между последней и первой вершинами
    if len(visited_nodes) == len(graph.nodes) and graph.has_edge(visited_nodes[-1], visited_nodes[0]):
        lenght = graph[visited_nodes[-1]][visited_nodes[0]]['weight']
        hamiltonian_cycle_temp.add_edge(visited_nodes[-1], visited_nodes[0], weight=lenght)
        hamiltonian_cycle.append(hamiltonian_cycle_temp)
        

    if len(hamiltonian_cycle) > 0:
        min_lenght = np.inf
        min_cycle = None
        # Находим гамильтонов цикл с минимальной длиной
        for cycle in hamiltonian_cycle:
            lenght = 0
            for edge in cycle.edges:
                lenght += cycle[edge[0]][edge[1]]['weight']
            if lenght < min_lenght:
                min_lenght = lenght
                min_cycle = cycle
        hamiltonian_cycle = min_cycle
    else:
        hamiltonian_cycle = None

    return hamiltonian_cycle

def hamiltonian_cycle_annaeling(graph, T, T_min, alpha, mode):
    # Функция для вычисления длины пути
    def path_length(path):
        length = 0
        for i in range(len(path) - 1):
            if not graph.has_edge(path[i], path[i+1]):
                return float('inf')
            length += graph[path[i]][path[i+1]]['weight']
        
        if not graph.has_edge(path[-1], path[0]):
            return float('inf')
        length += graph[path[-1]][path[0]]['weight']
        return length

    # Начальное решение: случайный гамильтонов цикл
    #current_solution = random.sample(graph.nodes(), len(graph.nodes()))

    if mode == "default":
        current_solution = list(graph.nodes())
    else:
        nearest_neighbor_solution = nearest_neighbor_hamiltonian_cycle_add(graph)
        if nearest_neighbor_solution is None:
            current_solution = list(graph.nodes())
        else:
            current_solution = list(nearest_neighbor_solution.nodes())


    #print(current_solution)
    current_length = path_length(current_solution)


    best_solution = current_solution
    best_length = current_length

    while T > T_min:
        #print(T, T_min, alpha)
        #print(current_solution, current_length)
        # Генерация случайного ВАЛИДНОГО соседнего решения
        neighbor_solution = current_solution.copy()
        i, j = random.sample(range(len(neighbor_solution)), 2)
        neighbor_solution[i], neighbor_solution[j] = neighbor_solution[j], neighbor_solution[i]
        neighbor_length = path_length(neighbor_solution)
        #print(neighbor_solution, neighbor_length)
        #print()
        #проверка на валидность
        if neighbor_length == float('inf'):
            T *= alpha
            continue

        #print(neighbor_solution, neighbor_length)
        #print(current_solution, current_length)
        #print()
        # Определение, принимаем ли мы новое решение
        if neighbor_length < current_length or random.random() < math.exp((current_length - neighbor_length) / T):
            current_solution = neighbor_solution
            current_length = neighbor_length
        #Мы принимаем решение на основании температуры и разницы длин путей

        # Уменьшение температуры
        T *= alpha

        # Обновление лучшего решения
        if current_length < best_length:
            best_solution = current_solution
            best_length = current_length

    #print(current_solution, current_length, "current")
    #print(best_solution, best_length, "best")

    current_solution = best_solution
    # Создание графа из найденного гамильтонова цикла
    hamiltonian_cycle = nx.DiGraph()
    hamiltonian_cycle.add_nodes_from(current_solution)
    hamiltonian_cycle.add_edges_from([(current_solution[i], current_solution[i+1]) for i in range(len(current_solution) - 1)])
    hamiltonian_cycle.add_edge(current_solution[-1], current_solution[0])

    for edge in hamiltonian_cycle.edges:
        if not graph.has_edge(edge[0], edge[1]):
            hamiltonian_cycle = None
            break

    #Веса
    if hamiltonian_cycle is not None:
        for edge in hamiltonian_cycle.edges:
            hamiltonian_cycle[edge[0]][edge[1]]['weight'] = graph[edge[0]][edge[1]]['weight']

    #Проверка на валидность гамильтонова цикла (все ребра присутствуют в исходном графе)

    # Если гамильтонов цикл не найден, выводим сообщение
    if hamiltonian_cycle is None:
        return None
    
    else:
        return hamiltonian_cycle



def nearest_neighbor_hamiltonian_cycle(graph):
    hamiltonian_cycle = []

    # Проходим по каждой вершине графа
    for node in graph.nodes:
        hamiltonian_cycle_temp = nx.DiGraph()
        hamiltonian_cycle_temp.add_node(node)
        current_node = node
        visited_nodes = [node]

        # Пока не посетили все вершины графа
        while len(visited_nodes) < len(graph.nodes):
            min_lenght = np.inf
            next_node = None
            # Проходим по соседям текущей вершины
            for neighbor in graph.neighbors(current_node):
                lenght = graph[current_node][neighbor]['weight']
                # Если длина ребра меньше минимальной длины и соседняя вершина еще не посещена
                if lenght < min_lenght and neighbor not in visited_nodes:
                    min_lenght = lenght
                    next_node = neighbor
            # Если не удалось найти следующую вершину, прерываем цикл
            if next_node is None:
                break
            else:
                # Добавляем следующую вершину в гамильтонов цикл
                hamiltonian_cycle_temp.add_node(next_node)
                hamiltonian_cycle_temp.add_edge(current_node, next_node, weight=min_lenght)
                visited_nodes.append(next_node)
                current_node = next_node
        
        # Если посетили все вершины и есть ребро между последней и первой вершинами
        if len(visited_nodes) == len(graph.nodes) and graph.has_edge(visited_nodes[-1], visited_nodes[0]):
            lenght = graph[visited_nodes[-1]][visited_nodes[0]]['weight']
            hamiltonian_cycle_temp.add_edge(visited_nodes[-1], visited_nodes[0], weight=lenght)
            hamiltonian_cycle.append(hamiltonian_cycle_temp)
        

    if len(hamiltonian_cycle) > 0:
        min_lenght = np.inf
        min_cycle = None
        # Находим гамильтонов цикл с минимальной длиной
        for cycle in hamiltonian_cycle:
            lenght = 0
            for edge in cycle.edges:
                lenght += cycle[edge[0]][edge[1]]['weight']
            if lenght < min_lenght:
                min_lenght = lenght
                min_cycle = cycle
        hamiltonian_cycle = min_cycle
    else:
        hamiltonian_cycle = None

    # Если гамильтонов цикл не найден, выводим сообщение
    if hamiltonian_cycle is None:
        return None
    else:
        return hamiltonian_cycle


def get_length(hamiltonian_cycle):
    length = 0
    if hamiltonian_cycle is None:
        return float('inf')
    for edge in hamiltonian_cycle.edges:
        length += hamiltonian_cycle[edge[0]][edge[1]]['weight']
    return length

def get_time(func, graph, *args):
    start = time.time()
    result = get_length(func(graph, *args))
    end = time.time()
    return result, end - start

#Генерация полносвязного графа с случайными весами
def generate_full_graph(n):
    G = nx.DiGraph()
    for i in range(n):
        for j in range(n):
            if i != j:
                G.add_edge(i, j, weight=random.randint(1, 10))
    return G

#генерация слабосвязного графа с случайными весами
def generate_weakly_connected_graph(n):
    G = nx.DiGraph()
    for i in range(n):
        for j in range(n):
            if i != j and random.random() > 0.5:
                G.add_edge(i, j, weight=random.randint(1, 10))
    return G





#Построй ступенчатую диаграмму, на которой будут отображены результаты сравнения алгоритмов из файла log_final.txt
'''
Файл log_final.txt

Ant colony optimization
Standard
Converge full - 1.0
Converge weak - 1.0
Mean length, time full - 65.78 0.3666716694831848
Mean length, time weak - 73.0 0.07451198577880859
Optimized param
Converge full - 1.0
Converge weak - 1.0
Mean length, time full - 63.88 0.5857323408126831
Mean length, time weak - 67.38 0.0867431664466858

Simulated annealing
Standard
Converge full - 1.0
Converge weak - 0.1
Mean length, time full - 73.79 0.0011199331283569336
Mean length, time weak - 67.6 0.000151824951171875
Optimized param
Converge full - 1.0
Converge weak - 0.15
Mean length, time full - 73.27 0.0011443018913269043
Mean length, time weak - 62.93333333333333 0.0007688681284586589

Nearest neighbor
Converge full - 1.0
Converge weak - 0.86
Mean length, time full - 61.97 0.04311347007751465
Mean length, time weak - 60.33720930232558 0.004102152447367824

'''

#Открываем файл и считываем данные
with open("log_final.txt", "r") as file:
    data = file.readlines()

for i in range(len(data)):
    if data[i].startswith("Ant colony optimization"):
        ant_st_full = float(data[i+2].split()[-1])
        ant_st_weak = float(data[i+3].split()[-1])
        ant_st_full_mean = float(data[i+4].split()[-2])
        ant_st_full_time = float(data[i+4].split()[-1])
        ant_st_weak_mean = float(data[i+5].split()[-2])
        ant_st_weak_time = float(data[i+5].split()[-1])

        ant_mod_full = float(data[i+7].split()[-1])
        ant_mod_weak = float(data[i+8].split()[-1])
        ant_mod_full_mean = float(data[i+9].split()[-2])
        ant_mod_full_time = float(data[i+9].split()[-1])
        ant_mod_weak_mean = float(data[i+10].split()[-2])
        ant_mod_weak_time = float(data[i+10].split()[-1])

    if data[i].startswith("Simulated annealing"):
        ann_st_full = float(data[i+2].split()[-1])
        ann_st_weak = float(data[i+3].split()[-1])
        ann_st_full_mean = float(data[i+4].split()[-2])
        ann_st_full_time = float(data[i+4].split()[-1])
        ann_st_weak_mean = float(data[i+5].split()[-2])
        ann_st_weak_time = float(data[i+5].split()[-1])

        ann_mod_full = float(data[i+7].split()[-1])
        ann_mod_weak = float(data[i+8].split()[-1])
        ann_mod_full_mean = float(data[i+9].split()[-2])
        ann_mod_full_time = float(data[i+9].split()[-1])
        ann_mod_weak_mean = float(data[i+10].split()[-2])
        ann_mod_weak_time = float(data[i+10].split()[-1])
    
    if data[i].startswith("Nearest neighbor"):
        nn_full = float(data[i+1].split()[-1])
        nn_weak = float(data[i+2].split()[-1])
        nn_full_mean = float(data[i+3].split()[-2])
        nn_full_time = float(data[i+3].split()[-1])
        nn_weak_mean = float(data[i+4].split()[-2])
        nn_weak_time = float(data[i+4].split()[-1])

#Строим график для полносвязного графа
fig, ax = plt.subplots()
ax.set_title("Full graph")
ax.set_xlabel("Algorithm")
ax.set_ylabel("Time")
ax.bar(["ACO", "SA", "NN"], [ant_st_full_time, ann_st_full_time, nn_full_time], label="Standard")
ax.bar(["ACO_O", "SA_O", "NN_O"], [ant_mod_full_time, ann_mod_full_time, nn_full_time], label="Optimized")
ax.legend()
plt.show()

fig, ax = plt.subplots()
ax.set_title("Full graph")
ax.set_xlabel("Algorithm")
ax.set_ylabel("Length")
ax.bar(["ACO", "SA", "NN"], [ant_st_full_mean, ann_st_full_mean, nn_full_mean], label="Standard")
ax.bar(["ACO_O", "SA_O", "NN_O"], [ant_mod_full_mean, ann_mod_full_mean, nn_full_mean], label="Optimized")
ax.legend()
plt.show()

#Строим график для слабосвязного графа
fig, ax = plt.subplots()
ax.set_title("Weakly connected graph")
ax.set_xlabel("Algorithm")
ax.set_ylabel("Time")
ax.bar(["ACO", "SA", "NN"], [ant_st_weak_time, ann_st_weak_time, nn_weak_time], label="Standard")
ax.bar(["ACO_O", "SA_O", "NN_O"], [ant_mod_weak_time, ann_mod_weak_time, nn_weak_time], label="Optimized")
ax.legend()
plt.show()

fig, ax = plt.subplots()
ax.set_title("Weakly connected graph")
ax.set_xlabel("Algorithm")
ax.set_ylabel("Length")
ax.bar(["ACO", "SA", "NN"], [ant_st_weak_mean, ann_st_weak_mean, nn_weak_mean], label="Standard")
ax.bar(["ACO_O", "SA_O", "NN_O"], [ant_mod_weak_mean, ann_mod_weak_mean, nn_weak_mean], label="Optimized")
ax.legend()
plt.show()

#Сравнение сходимости
fig, ax = plt.subplots()
ax.set_title("Convergence")
ax.set_xlabel("Algorithm")
ax.set_ylabel("Convergence")
ax.bar(["ACO_F", "SA_F", "NN_F"], [ant_st_full, ann_st_full, nn_full], label="Full")
ax.bar(["ACO_W", "SA_W", "NN_W"], [ant_st_weak, ann_st_weak, nn_weak], label="Weak")
ax.legend()
plt.show()

#Сравнение сходимости
fig, ax = plt.subplots()
ax.set_title("Convergence")
ax.set_xlabel("Algorithm")
ax.set_ylabel("Convergence")
ax.bar(["ACO_F", "SA_F", "NN_F"], [ant_mod_full, ann_mod_full, nn_full], label="Full")
ax.bar(["ACO_W", "SA_W", "NN_W"], [ant_mod_weak, ann_mod_weak, nn_weak], label="Weak")
ax.legend()
plt.show()




'''
Gdefault = nx.DiGraph()

Gdefault.add_edge(1, 2, weight=3, label=1)
Gdefault.add_edge(1, 3, weight=1, label=1)
Gdefault.add_edge(2, 1, weight=3, label=1)
Gdefault.add_edge(2, 4, weight=8, label=1)
Gdefault.add_edge(2, 6, weight=3, label=1)
Gdefault.add_edge(3, 1, weight=3, label=1)
Gdefault.add_edge(3, 5, weight=3, label=1)
Gdefault.add_edge(4, 2, weight=3, label=1)
Gdefault.add_edge(4, 5, weight=1, label=1)
Gdefault.add_edge(4, 6, weight=1, label=1)
Gdefault.add_edge(5, 4, weight=8, label=1)
Gdefault.add_edge(5, 3, weight=1, label=1)
Gdefault.add_edge(6, 2, weight=3, label=1)
Gdefault.add_edge(6, 4, weight=3, label=1)
Gdefault.add_edge(6, 1, weight=3, label=1)
Gdefault.add_edge(6, 3, weight=4, label=1)
Gdefault.add_edge(6, 5, weight=5, label=1)


#Сравнение алгоритмов на случайных графах, сбор статистики

ant_st_full = {}
ant_st_weak = {}
ant_mod_full = {}
ant_mod_weak = {}
ann_st_full = {}
ann_st_weak = {}
ann_mod_full = {}
ann_mod_weak = {}
nn_full = {}
nn_weak = {}

for i in range(100):
    Gfull = generate_full_graph(50)
    Gweak = generate_weakly_connected_graph(25)

    ant_st_full[i] = get_time(ant_hamiltonian_cycle, Gfull, 10, 0.5, 2, 20)
    ant_st_weak[i] = get_time(ant_hamiltonian_cycle, Gweak, 10, 0.5, 2, 20)
    ant_mod_full[i] = get_time(ant_hamiltonian_cycle, Gfull, 19, 0.58, 2.8, 17)
    ant_mod_weak[i] = get_time(ant_hamiltonian_cycle, Gweak, 17, 0.54, 2.4, 14)
    ann_st_full[i] = get_time(hamiltonian_cycle_annaeling, Gfull, 1000, 1, 0.1, "mod")
    ann_st_weak[i] = get_time(hamiltonian_cycle_annaeling, Gweak, 1000, 1, 0.1, "mod")
    ann_mod_full[i] = get_time(hamiltonian_cycle_annaeling, Gfull, 897, 1.1, 0.42, "mod")
    ann_mod_weak[i] = get_time(hamiltonian_cycle_annaeling, Gweak, 959, 1.6, 0.65, "mod")
    nn_full[i] = get_time(nearest_neighbor_hamiltonian_cycle, Gfull)
    nn_weak[i] = get_time(nearest_neighbor_hamiltonian_cycle, Gweak)
    print(i)
    
#Сводка статистики

print("Ant colony optimization")
print("Standard")
#Процент сходимости
print("Converge full - " ,len([x for x in ant_st_full.values() if x[0] != float('inf')]) / len(ant_st_full), sep = "")
print("Converge weak - " ,len([x for x in ant_st_weak.values() if x[0] != float('inf')]) / len(ant_st_weak), sep = "")
print(np.mean([x[0] for x in ant_st_full.values() if x[0] != float('inf')]), np.mean([x[1] for x in ant_st_full.values() if x[0] != float('inf')]))
print(np.mean([x[0] for x in ant_st_weak.values() if x[0] != float('inf')]), np.mean([x[1] for x in ant_st_weak.values() if x[0] != float('inf')]))

print("Modified")
print("Converge full - " ,len([x for x in ant_mod_full.values() if x[0] != float('inf')]) / len(ant_mod_full), sep = "")
print("Converge weak - " ,len([x for x in ant_mod_weak.values() if x[0] != float('inf')]) / len(ant_mod_weak), sep = "")
print(np.mean([x[0] for x in ant_mod_full.values() if x[0] != float('inf')]), np.mean([x[1] for x in ant_mod_full.values() if x[0] != float('inf')]))
print(np.mean([x[0] for x in ant_mod_weak.values() if x[0] != float('inf')]), np.mean([x[1] for x in ant_mod_weak.values() if x[0] != float('inf')]))

print()
print("Simulated annealing")
print("Standard")
print("Converge full - " ,len([x for x in ann_st_full.values() if x[0] != float('inf')]) / len(ann_st_full), sep = "")
print("Converge weak - " ,len([x for x in ann_st_weak.values() if x[0] != float('inf')]) / len(ann_st_weak), sep = "")
print(np.mean([x[0] for x in ann_st_full.values() if x[0] != float('inf')]), np.mean([x[1] for x in ann_st_full.values() if x[0] != float('inf')]))
print(np.mean([x[0] for x in ann_st_weak.values() if x[0] != float('inf')]), np.mean([x[1] for x in ann_st_weak.values() if x[0] != float('inf')]))

print("Modified")
print("Converge full - " ,len([x for x in ann_mod_full.values() if x[0] != float('inf')]) / len(ann_mod_full), sep = "")
print("Converge weak - " ,len([x for x in ann_mod_weak.values() if x[0] != float('inf')]) / len(ann_mod_weak), sep = "")
print(np.mean([x[0] for x in ann_mod_full.values() if x[0] != float('inf')]), np.mean([x[1] for x in ann_mod_full.values() if x[0] != float('inf')]))
print(np.mean([x[0] for x in ann_mod_weak.values() if x[0] != float('inf')]), np.mean([x[1] for x in ann_mod_weak.values() if x[0] != float('inf')]))

print()
print("Nearest neighbor")
print("Converge full - " ,len([x for x in nn_full.values() if x[0] != float('inf')]) / len(nn_full), sep = "")
print("Converge weak - " ,len([x for x in nn_weak.values() if x[0] != float('inf')]) / len(nn_weak), sep = "")
print(np.mean([x[0] for x in nn_full.values() if x[0] != float('inf')]), np.mean([x[1] for x in nn_full.values() if x[0] != float('inf')]))
print(np.mean([x[0] for x in nn_weak.values() if x[0] != float('inf')]), np.mean([x[1] for x in nn_weak.values() if x[0] != float('inf')]))


#Логирование результатов
with open("log_ant_st_full.txt", "w") as file:
    for key, value in ant_st_full.items():
        file.write(f"{key} {value[0]} {value[1]}\n")

with open("log_ant_st_weak.txt", "w") as file:
    for key, value in ant_st_weak.items():
        file.write(f"{key} {value[0]} {value[1]}\n")

with open("log_ant_mod_full.txt", "w") as file:
    for key, value in ant_mod_full.items():
        file.write(f"{key} {value[0]} {value[1]}\n")

with open("log_ant_mod_weak.txt", "w") as file:
    for key, value in ant_mod_weak.items():
        file.write(f"{key} {value[0]} {value[1]}\n")

with open("log_ann_st_full.txt", "w") as file:
    for key, value in ann_st_full.items():
        file.write(f"{key} {value[0]} {value[1]}\n")

with open("log_ann_st_weak.txt", "w") as file:
    for key, value in ann_st_weak.items():
        file.write(f"{key} {value[0]} {value[1]}\n")

with open("log_ann_mod_full.txt", "w") as file:
    for key, value in ann_mod_full.items():
        file.write(f"{key} {value[0]} {value[1]}\n")

with open("log_ann_mod_weak.txt", "w") as file:
    for key, value in ann_mod_weak.items():
        file.write(f"{key} {value[0]} {value[1]}\n")

with open("log_nn_full.txt", "w") as file:
    for key, value in nn_full.items():
        file.write(f"{key} {value[0]} {value[1]}\n")

with open("log_nn_weak.txt", "w") as file:
    for key, value in nn_weak.items():
        file.write(f"{key} {value[0]} {value[1]}\n")

'''

#Сравнение алгоритмов на стандартном графе
'''
print("Ant colony optimization")
print(get_time(ant_hamiltonian_cycle, Gdefault, 17, 0.54, 2.4, 14))
print("Nearest neighbor")
print(get_time(nearest_neighbor_hamiltonian_cycle, Gdefault))
print("Simulated annealing")
print(get_time(hamiltonian_cycle_annaeling, Gdefault, 959, 1.6, 0.65, "mod"))
'''

#Подбери оптимальные параметры для алгоритма муравьиной колонии с помощью перебора. Время работы алгоритма не должно превышать 1 секунды, а отклонение от оптимального решения(с помощью алгоритма ближайшего соседа) не должно превышать 10%.
'''
etalon_length, etalon_time = get_time(nearest_neighbor_hamiltonian_cycle, Gdefault)
print(etalon_length, etalon_time)

x = input()

best = {}

#Логирование результатов
with open("log_ant_ants.txt", "w") as file:
    for AntNum in range(1, 20):
        for Evaporation in np.arange(0.1, 1, 0.1):
            for Influence in np.arange(0.001, 4, 0.33):
                length, tm = get_time(ant_hamiltonian_cycle, Gdefault, AntNum, Evaporation, Influence, 10)
                print(AntNum, Evaporation, Influence, tm, length, etalon_length/length * 100)
                file.write(f"{AntNum} {Evaporation} {Influence} {tm} {length} {etalon_length/length * 100}\n")
                if tm < 1:
                    best[etalon_length/length * 100] = (AntNum, Evaporation, Influence, tm, length)

print(best[max(best.keys())], max(best.keys()))


best = {}
with open("log_ant_it.txt", "w") as file:
    for ItNum in range(1, 20):
        for Evaporation in np.arange(0.1, 1, 0.1):
            for Influence in np.arange(0.001, 4, 0.33):
                length, tm = get_time(ant_hamiltonian_cycle, Gdefault, 10, Evaporation, Influence, ItNum)
                print(ItNum, Evaporation, Influence, tm, length, etalon_length/length * 100)
                file.write(f"{ItNum} {Evaporation} {Influence} {tm} {length} {etalon_length/length * 100}\n")
                if tm < 1:
                    best[etalon_length/length * 100] = (ItNum, Evaporation, Influence, tm, length)

print(best[max(best.keys())], max(best.keys()))


best1 = {}
with open("log_ant_ants.txt", "r") as file:
    for line in file:
        line = line.split()
        best1[float(line[-1])] = (int(line[0]), float(line[1]), float(line[2]), float(line[3]), float(line[4]))

best2 = {}
with open("log_ant_it.txt", "r") as file:
    for line in file:
        line = line.split()
        best2[float(line[-1])] = (int(line[0]), float(line[1]), float(line[2]), float(line[3]), float(line[4]))
#Возьмем 5 лучших результатов из каждого лога и найдем среднее значение параметров
best1 = sorted(best1.items(), key=lambda x: x[0], reverse=True)
best2 = sorted(best2.items(), key=lambda x: x[0], reverse=True)

best1 = best1[:5]
best2 = best2[:5]

print(best1)

best_antnum = sum([x[1][0] for x in best1]) / 5
best_evaporation = sum([x[1][1] for x in best1] + [x[1][1] for x in best2]) / 10
best_influence = sum([x[1][2] for x in best1] + [x[1][2] for x in best2]) / 10
best_iterations = sum([x[1][0] for x in best2]) / 5

print(best_antnum, best_evaporation, best_influence, best_iterations)
with open("best_params_ant.txt", "w") as file:
    file.write(f"{best_antnum} {best_evaporation} {best_influence} {best_iterations}")



#Подбери оптимальные параметры для алгоритма имитации отжига с помощью перебора. Время работы алгоритма не должно превышать 1 секунды, а отклонение от оптимального решения(с помощью алгоритма ближайшего соседа) не должно превышать 10%.

etalon_length, etalon_time = get_time(nearest_neighbor_hamiltonian_cycle, Gdefault)
print(etalon_length, etalon_time)

best = {}

#Логирование результатов
with open("log_annealing.txt", "w") as file:
    for T in range(0, 1000, 10):
        for T_min in np.arange(0.01, 2, 0.1):
            for alpha in np.arange(0.1, 1, 0.1):
                length, tm = get_time(hamiltonian_cycle_annaeling, Gdefault, T, T_min, alpha, "mod")
                print(T, T_min, alpha, tm, length, etalon_length/length * 100)
                file.write(f"{T} {T_min} {alpha} {tm} {length} {etalon_length/length * 100}\n")
                if tm < 1:
                    best[etalon_length/length * 100] = (T, T_min, alpha, tm, length)

print(best[max(best.keys())], max(best.keys()))


best1 = {}
with open("log_annealing.txt", "r") as file:
    for line in file:
        line = line.split()
        best1[float(line[-1])] = (int(line[0]), float(line[1]), float(line[2]), float(line[3]), float(line[4]))

best1 = sorted(best1.items(), key=lambda x: x[0], reverse=True)

best1 = best1[:10]

print(best1)

best_T = sum([x[1][0] for x in best1]) / 10
best_T_min = sum([x[1][1] for x in best1]) / 10
best_alpha = sum([x[1][2] for x in best1]) / 10

print(best_T, best_T_min, best_alpha)

with open("best_params_annealing.txt", "w") as file:
    file.write(f"{best_T} {best_T_min} {best_alpha}")
'''

    