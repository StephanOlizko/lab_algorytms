import tkinter as tk
import tkinter.ttk as ttk
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


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


G1 = nx.Graph()

node_id = None
node_coords = None

def update_tree():
    tree.delete(*tree.get_children())
    for edge in G1.edges:
        source, target = edge
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
                    G1.add_edge(node_id, node)
                    x1, y1 = G1.nodes[node_id]['pos']
                    x2, y2 = G1.nodes[node]['pos']
                    canvas1.create_line(x1, y1, x2, y2, width=2)
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
tree.pack(fill='both', expand=True)



root.mainloop()