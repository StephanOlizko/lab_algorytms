import tkinter as tk
import tkinter.ttk as ttk
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

def finish():
    root.destroy() 
    print("Закрытие приложения")

root = tk.Tk()
root.geometry('1200x600')
root.protocol("WM_DELETE_WINDOW", finish)
root.resizable(False, False)

frame1 = tk.Frame(root, bd=2, relief='groove', width=200)
#frame2 = tk.Frame(root, bd=2, relief='groove', width=10)
frame2 = tk.Frame(root, bd=2, relief='groove')
#frame4 = tk.Frame(root, bd=2, relief='groove', width=10)
frame3 = tk.Frame(root, bd=2, relief='groove', width=100)

frame1.grid(row=0, column=0, sticky='nsew')
frame2.grid(row=1, column=0, sticky='nsew')
frame3.grid(row=0, column=2, rowspan=2, sticky='nsew')

root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=3)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=3)

def nearest_neighbor_hamiltonian_cycle(graph):
    
    #Вывод информации о ребрах графа и их весах
    for edge in graph.edges:
        print('Ребро:', edge, 'Вес:', graph[edge[0]][edge[1]]['weight'])

    # Создаем пустой граф для хранения кратчайшего гамильтонова цикла
    hamiltonian_cycle = nx.DiGraph()

    # Выбираем случайную начальную вершину
    current_node = np.random.choice(list(graph.nodes()))

    # Список для отслеживания посещенных вершин
    visited_nodes = [current_node]

    # Пока есть непосещенные вершины
    while len(visited_nodes) < len(graph.nodes()):
        # Находим ближайшую непосещенную вершину к текущей
        nearest_neighbor = min(graph[current_node], key=lambda x: graph[current_node][x]['weight'])
        # Добавляем ребро кратчайшего пути к новой вершине в подграф
        hamiltonian_cycle.add_edge(current_node, nearest_neighbor, weight=graph[current_node][nearest_neighbor]['weight'])
        # Переходим к следующей вершине
        current_node = nearest_neighbor
        # Отмечаем вершину как посещенную
        visited_nodes.append(current_node)

    # Добавляем ребро от последней вершины к первой если оно существует иначе выводим сообщение об ошибке
    if graph.has_edge(current_node, visited_nodes[0]):
        hamiltonian_cycle.add_edge(current_node, visited_nodes[0], weight=graph[current_node][visited_nodes[0]]['weight'])
    else:
        print('Гамильтонов цикл не существует')
        #Запись информации о гамильтоновом цикле в текстовое поле
        text1.delete(1.0, tk.END)
        text1.insert(tk.END, 'Гамильтонов цикл не существует')
        return None

    #Запись информации о гамильтоновом цикле в текстовое поле
    text1.delete(1.0, tk.END)
    text1.insert(tk.END, 'Гамильтонов цикл: ')
    text1.insert(tk.END, hamiltonian_cycle.edges())
    text1.insert(tk.END, '\n')
    text1.insert(tk.END, 'Длина: ')
    
    lenght = 0
    for edge in hamiltonian_cycle.edges:
        print('Ребро:', edge, 'Вес:', hamiltonian_cycle[edge[0]][edge[1]]['weight'])
        lenght += hamiltonian_cycle[edge[0]][edge[1]]['weight']

    text1.insert(tk.END, lenght)
    text1.insert(tk.END, '\n')

    return hamiltonian_cycle

G1 = nx.DiGraph()

node_id = None
node_coords = None

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

    #Обновление данных в графе
    G1.remove_edge(tree.item(row_id)['values'][0], tree.item(row_id)['values'][1])

    source = tree.item(row_id)['values'][0]
    target = tree.item(row_id)['values'][1]
    lenght = tree.item(row_id)['values'][2]
    weight = tree.item(row_id)['values'][3]

    G1.add_edge(source, target, weight=lenght, label=weight)


def update_tree():
    #tree.delete(*tree.get_children())
    for edge in G1.edges:
        #Проверка наличия ребра c данными вершинами в таблице
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

def add_node(event):
    node_id = len(G1.nodes) + 1
    G1.add_node(node_id, pos=(event.x, event.y))
    canvas1.create_oval(event.x-10, event.y-10, event.x+10, event.y+10, fill='red')
    canvas1.create_text(event.x, event.y, text=str(node_id))
    update_tree()


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
                    #Добавляем направленное ребро в граф
                    lenght = ((G1.nodes[node_id]['pos'][0] - G1.nodes[node]['pos'][0])**2 + (G1.nodes[node_id]['pos'][1] - G1.nodes[node]['pos'][1])**2)**0.5
                    weight = 1
                    G1.add_edge(node_id, node, weight=lenght, label=weight)

                    x1, y1 = G1.nodes[node_id]['pos']
                    x2, y2 = G1.nodes[node]['pos']
                    #Рисуем направленное ребро из x1, y1 в x2, y2
                    canvas1.create_line(x1, y1, x2, y2, arrow=tk.LAST)
                    node_id = None
                    update_tree()
                    break


canvas1 = tk.Canvas(root, width=400, height=400, bg='white', bd=2, relief='groove')
canvas1.grid(row=0, column=1, sticky='nsew')

canvas1.bind('<Button-1>', add_node)
canvas1.bind('<Button-3>', add_edge_on_right_click)


canvas2 = tk.Canvas(root, width=400, height=400, bg='white', bd=2, relief='groove')
canvas2.grid(row=1, column=1, sticky='nsew')

#таблица ребер графа G1 на фрейме frame5
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

#Добавим кнопку на первый фрейм
button1 = tk.Button(frame1, text='Построить гамильтонов цикл', command=lambda: nearest_neighbor_hamiltonian_cycle(G1))
button1.pack(fill='both')

#Добавим текстовое поле для вывода информации о гамильтоновом цикле на второй фрейм
text1 = tk.Text(frame2, height=10, width=30)
text1.pack(fill='both', expand=True)


root.mainloop()