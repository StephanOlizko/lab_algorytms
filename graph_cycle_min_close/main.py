import tkinter as tk
import networkx as nx
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

import tkinter.ttk as ttk
import matplotlib.pyplot as plt

# Функция для закрытия приложения
def finish():
    root.destroy() 
    print("Закрытие приложения")

# Функция для построения гамильтонова цикла методом ближайшего соседа
def nearest_neighbor_hamiltonian_cycle(graph, canvas, pos):
    canvas.delete('all')

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
        
        lenght = 0
        for edge in hamiltonian_cycle.edges:
            lenght += hamiltonian_cycle[edge[0]][edge[1]]['weight']

        text1.insert(tk.END, lenght)
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
tree.heading('weight', text='Вес')

tree.bind('<Double-1>', edit)
tree.pack(fill='both', expand=True)

button1 = tk.Button(frame1, text='Построить гамильтонов цикл', command=lambda: nearest_neighbor_hamiltonian_cycle(G1, canvas2, pos))
button1.pack(fill='both')

button2 = tk.Button(frame1, text='Gdefault', command=lambda: Gdefault())
button2.pack(fill='both')

text1 = tk.Text(frame2, height=10, width=30)
text1.pack(fill='both', expand=True)

root.mainloop()