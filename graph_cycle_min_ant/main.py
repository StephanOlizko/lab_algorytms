import tkinter as tk
import networkx as nx
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import random
import tkinter.ttk as ttk
import matplotlib.pyplot as plt
import math

# Функция для закрытия приложения
def finish():
    root.destroy() 
    print("Закрытие приложения")

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


def ant_hamiltonian_cycle(graph, canvas, pos, entry1, entry2, entry3, entry4):
    canvas.delete('all')
    AntNum = int(entry1.get())
    Evaporation = float(entry2.get())
    Influence = float(entry3.get())
    Iterations = int(entry4.get())

    hamiltonian_cycle = None

    colony = AntColony(graph, AntNum, Evaporation, Influence)
    best_ant = colony.search(Iterations)

    update_tree_pheromones(colony.pheromones)
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
        text1.delete(1.0, tk.END)
        text1.insert(tk.END, 'Гамильтонов цикл не найден')
        return None
    
    else:
        # Выводим гамильтонов цикл и его длину
        text1.delete(1.0, tk.END)
        text1.insert(tk.END, 'Гамильтонов цикл: ')
        text1.insert(tk.END, hamiltonian_cycle.edges())
        text1.insert(tk.END, '\n')
        text1.insert(tk.END, 'Длина: ')
        
        length = 0
        for edge in hamiltonian_cycle.edges:
            length += graph[edge[0]][edge[1]]['weight']

        text1.insert(tk.END, length)
        text1.insert(tk.END, '\n')

        # Отображаем вершины гамильтонова цикла на холсте
        for node in hamiltonian_cycle.nodes:
            x, y = pos[node]
            canvas.create_oval(x-10, y-10, x+10, y+10, fill='red')
            canvas.create_text(x, y, text=str(node))

        # Отображаем ребра гамильтонова цикла на холсте
        for edge in hamiltonian_cycle.edges:
            x1, y1 = pos[edge[0]]
            x2, y2 = pos[edge[1]]
            canvas.create_line(x1, y1, x2, y2, arrow=tk.LAST)

        return hamiltonian_cycle

# Функция для создания графа по умолчанию
def Gdefault():
    global G1
    global pos

    # Очищаем холст и дерево
    canvas1.delete('all')
    tree.delete(*tree.get_children())
    
    Gdefault = nx.DiGraph()

    # Добавляем вершины
    Gdefault.add_node(1)
    Gdefault.add_node(2)
    Gdefault.add_node(3)
    Gdefault.add_node(4)
    Gdefault.add_node(5)
    Gdefault.add_node(6)
    
    # Отображаем вершины на холсте
    canvas1.create_oval(218-10, 67-10, 218+10, 67+10, fill='red')
    canvas1.create_text(218, 67, text=str(1))
    canvas1.create_oval(104-10, 129-10, 104+10, 129+10, fill='red')
    canvas1.create_text(104, 129, text=str(2))
    canvas1.create_oval(331-10, 123-10, 331+10, 123+10, fill='red')
    canvas1.create_text(331, 123, text=str(3))
    canvas1.create_oval(167-10, 239-10, 167+10, 239+10, fill='red')
    canvas1.create_text(167, 239, text=str(4))
    canvas1.create_oval(285-10, 237-10, 285+10, 237+10, fill='red')
    canvas1.create_text(285, 237, text=str(5))
    canvas1.create_oval(223-10, 155-10, 223+10, 155+10, fill='red')
    canvas1.create_text(223, 155, text=str(6))

    # Добавляем ребра
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

    # Отображаем ребра на холсте
    canvas1.create_line(218, 67, 104, 129, arrow=tk.LAST)
    canvas1.create_line(218, 67, 331, 123, arrow=tk.LAST)
    canvas1.create_line(104, 129, 218, 67, arrow=tk.LAST)
    canvas1.create_line(104, 129, 167, 239, arrow=tk.LAST)
    canvas1.create_line(104, 129, 223, 155, arrow=tk.LAST)
    canvas1.create_line(331, 123, 218, 67, arrow=tk.LAST)
    canvas1.create_line(331, 123, 285, 237, arrow=tk.LAST)
    canvas1.create_line(167, 239, 104, 129, arrow=tk.LAST)
    canvas1.create_line(167, 239, 285, 237, arrow=tk.LAST)
    canvas1.create_line(167, 239, 223, 155, arrow=tk.LAST)
    canvas1.create_line(285, 237, 167, 239, arrow=tk.LAST)
    canvas1.create_line(285, 237, 331, 123, arrow=tk.LAST)
    canvas1.create_line(223, 155, 104, 129, arrow=tk.LAST)
    canvas1.create_line(223, 155, 167, 239, arrow=tk.LAST)
    canvas1.create_line(223, 155, 218, 67, arrow=tk.LAST)
    canvas1.create_line(223, 155, 331, 123, arrow=tk.LAST)
    canvas1.create_line(223, 155, 285, 237, arrow=tk.LAST)

    # Добавляем ребра в дерево
    tree.insert('', 'end', values=(1, 2, 3, 1))
    tree.insert('', 'end', values=(1, 3, 1, 1))
    tree.insert('', 'end', values=(2, 1, 3, 1))
    tree.insert('', 'end', values=(2, 4, 8, 1))
    tree.insert('', 'end', values=(2, 6, 3, 1))
    tree.insert('', 'end', values=(3, 1, 3, 1))
    tree.insert('', 'end', values=(3, 5, 3, 1))
    tree.insert('', 'end', values=(4, 2, 3, 1))
    tree.insert('', 'end', values=(4, 5, 1, 1))
    tree.insert('', 'end', values=(4, 6, 1, 1))
    tree.insert('', 'end', values=(5, 4, 8, 1))
    tree.insert('', 'end', values=(5, 3, 1, 1))
    tree.insert('', 'end', values=(6, 2, 3, 1))
    tree.insert('', 'end', values=(6, 4, 3, 1))
    tree.insert('', 'end', values=(6, 1, 3, 1))
    tree.insert('', 'end', values=(6, 3, 4, 1))
    tree.insert('', 'end', values=(6, 5, 5, 1))

    G1 = Gdefault
    pos = {1: (218, 67), 2: (104, 129), 3: (331, 123), 4: (167, 239), 5: (285, 237), 6: (223, 155)}

# Функция для редактирования ребра в дереве
def edit(event):
    row_id = tree.focus()
    column_id = tree.identify_column(event.x)
    cell_value = tree.item(row_id)['values'][int(column_id[1]) - 1]

    def save_edit(event):
        tree.set(row_id, column_id, edit_entry.get())
        edit_entry.destroy()

    edit_entry = tk.Entry(tree, text=cell_value)
    edit_entry.insert(0, cell_value)
    edit_entry.bind('<Return>', save_edit)
    edit_entry.place(x=event.x, y=event.y)

    G1.remove_edge(tree.item(row_id)['values'][0], tree.item(row_id)['values'][1])

    source = tree.item(row_id)['values'][0]
    target = tree.item(row_id)['values'][1]
    lenght = tree.item(row_id)['values'][2]
    weight = tree.item(row_id)['values'][3]

    G1.add_edge(source, target, weight=lenght, label=weight)

def update_tree_pheromones(pheromones):
    for edge in pheromones:
        source = edge[0]
        target = edge[1]

        for row in tree.get_children():
            if tree.item(row)['values'][0] == source and tree.item(row)['values'][1] == target:
                tree.set(row, 'weight', round(pheromones[edge], 5))

# Функция для обновления дерева
def update_tree():
    for edge in G1.edges:
        source = edge[0]
        target = edge[1]
        flg = False

        for row in tree.get_children():
            if tree.item(row)['values'][0] == source and tree.item(row)['values'][1] == target:
                flg = True
                
        if not flg:
            lenght = ((G1.nodes[source]['pos'][0] - G1.nodes[target]['pos'][0])**2 + (G1.nodes[source]['pos'][1] - G1.nodes[target]['pos'][1])**2)**0.5
            weight = 1
            tree.insert('', 'end', values=(source, target, round(lenght, 2), weight))

# Функция для добавления вершины на холсте
def add_node(event):
    global pos

    node_id = len(G1.nodes) + 1
    G1.add_node(node_id, pos=(event.x, event.y))
    canvas1.create_oval(event.x-10, event.y-10, event.x+10, event.y+10, fill='red')
    canvas1.create_text(event.x, event.y, text=str(node_id))
    update_tree()

    node_coords = (event.x, event.y)
    pos[node_id] = node_coords

# Функция для добавления ребра при правом клике на холсте
def add_edge_on_right_click(event):
    global node_id

    if node_id is None:
        for node in G1.nodes:
            x, y = G1.nodes[node]['pos']
            if (x - event.x)**2 + (y - event.y)**2 < 100:
                node_id = node
                update_tree()
                break

    else:
        for node in G1.nodes:
            x, y = G1.nodes[node]['pos']
            if (x - event.x)**2 + (y - event.y)**2 < 100:
                if node_id == node:
                    x1, y1 = G1.nodes[node_id]['pos']
                    canvas1.create_oval(x1, y1, x1+15, y1+15, width=2)
                    update_tree()
                    break
                else:
                    lenght = ((G1.nodes[node_id]['pos'][0] - G1.nodes[node]['pos'][0])**2 + (G1.nodes[node_id]['pos'][1] - G1.nodes[node]['pos'][1])**2)**0.5
                    weight = 1
                    G1.add_edge(node_id, node, weight=lenght, label=weight)

                    x1, y1 = G1.nodes[node_id]['pos']
                    x2, y2 = G1.nodes[node]['pos']

                    canvas1.create_line(x1, y1, x2, y2, arrow=tk.LAST)
                    node_id = None
                    update_tree()
                    break

# Создаем главное окно
root = tk.Tk()
root.geometry('1200x600')
root.protocol("WM_DELETE_WINDOW", finish)
root.resizable(False, False)

frame1 = tk.Frame(root, bd=2, relief='groove', width=200)
frame2 = tk.Frame(root, bd=2, relief='groove')
frame3 = tk.Frame(root, bd=2, relief='groove', width=100)

frame1.grid(row=0, column=0, sticky='nsew')
frame2.grid(row=1, column=0, sticky='nsew')
frame3.grid(row=0, column=2, rowspan=2, sticky='nsew')

root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=3)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=3)

G1 = nx.DiGraph()
pos = {}

node_id = None
node_coords = None

canvas1 = tk.Canvas(root, width=400, height=400, bg='white', bd=2, relief='groove')
canvas1.grid(row=0, column=1, sticky='nsew')

canvas1.bind('<Button-1>', add_node)
canvas1.bind('<Button-3>', add_edge_on_right_click)

canvas2 = tk.Canvas(root, width=400, height=400, bg='white', bd=2, relief='groove')
canvas2.grid(row=1, column=1, sticky='nsew')

tree = ttk.Treeview(frame3, columns=('source', 'target', 'lenght', 'weight'), height=15, show='headings')
tree.column('source', width=100, anchor='center')
tree.column('target', width=100, anchor='center')
tree.column('lenght', width=100, anchor='center')
tree.column('weight', width=100, anchor='center')
tree.heading('source', text='Источник')
tree.heading('target', text='Цель')
tree.heading('lenght', text='Длина')
tree.heading('weight', text='Феромон')

tree.bind('<Double-1>', edit)
tree.pack(fill='both', expand=True)

button1 = tk.Button(frame1, text='Построить гамильтонов цикл', command=lambda: ant_hamiltonian_cycle(G1, canvas2, pos, entry1, entry2, entry3, entry4))
button1.pack(fill='both')

button2 = tk.Button(frame1, text='Gdefault', command=lambda: Gdefault())
button2.pack(fill='both')

#Добавь поле для ввода нчальной температуры на фрейме frame1, добавь надпись "начальная температура" рядом с полем

text1 = tk.Label(frame1, text='количество муравьев', anchor='sw', height=2)
text1.pack(fill='both')
entry1 = tk.Entry(frame1, width=10)
entry1.pack(fill='both')
entry1.insert(0, '10')

#Добавь поле для ввода коэффициента охлаждения на фрейме frame1
text2 = tk.Label(frame1, text='испарение феромона', anchor='sw', height=2)
text2.pack(fill='both')
entry2 = tk.Entry(frame1, width=10)
entry2.pack(fill='both')
entry2.insert(0, '0.5')

text3 = tk.Label(frame1, text= 'коэффицент влияния феромона', anchor='sw', height=2)
text3.pack(fill='both')
entry3 = tk.Entry(frame1, width=10)
entry3.pack(fill='both')
entry3.insert(0, '2')

text4 = tk.Label(frame1, text='количество итераций', anchor='sw', height=2)
text4.pack(fill='both')
entry4 = tk.Entry(frame1, width=10)
entry4.pack(fill='both')
entry4.insert(0, '20')


text1 = tk.Text(frame2, height=10, width=30)
text1.pack(fill='both', expand=True)

root.mainloop()