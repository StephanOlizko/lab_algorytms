import tkinter as tk
import networkx as nx
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import random
import tkinter.ttk as ttk
import matplotlib.pyplot as plt


class Node:
    children = []
    parent = None
    value = None

    def __init__(self, parent, value):
        self.value = value
        self.parent = parent

    def add_child(self, child):
        self.children.append(child)

    def __str__(self):
        return str(self.value)


class Tree:
    nodes = {}
    top = None

    def __init__(self, top):
        self.top = Node(None, top)
        self.nodes[top] = self.top
    
    def add_node(self, parent, value):
        node = Node(parent, value)
        parent.add_child(node)
        self.nodes[value] = node
        return node
    
    def __str__(self):
        #обход в ширину
        pass
    
    def __getitem__(self, index):
        return self.nodes[index]


def finish():
    root.destroy() 
    print("Закрытие приложения")

def edit(event):
    row_id = tree_table.focus()
    column_id = tree_table.identify_column(event.x)
    cell_value = tree_table.item(row_id)['values'][int(column_id[1]) - 1]

    def save_edit(event):
        tree_table.set(row_id, column_id, edit_entry.get())
        edit_entry.destroy()

    edit_entry = tk.Entry(tree_table, text=cell_value)
    edit_entry.insert(0, cell_value)
    edit_entry.bind('<Return>', save_edit)
    edit_entry.place(x=event.x, y=event.y)

    draw_tree(tree, canvas1)

def draw_tree(tree, canvas):
    pass

def fill_table():
    global tree

    edges = text1.get('1.0', 'end').split(',')
    top = edges.pop(0).strip()
    tree = Tree(int(top))

    for edge in edges:
        source, target = edge.split()
        
        #поиск 



        tree_table.insert('', 'end', values=(source, target))
        text1.delete('1.0', 'end')
    
    draw_tree(tree, canvas1)

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



canvas1 = tk.Canvas(root, width=400, height=400, bg='white', bd=2, relief='groove')
canvas1.grid(row=0, column=1, sticky='nsew')

canvas2 = tk.Canvas(root, width=400, height=400, bg='white', bd=2, relief='groove')
canvas2.grid(row=1, column=1, sticky='nsew')


text1 = tk.Text(frame3, wrap='word', width=30, height=1)
text1.pack(fill='both', expand=True)

button_input = tk.Button(frame3, text='Ввод', command= fill_table)
button_input.pack(fill='x')

tree_table = ttk.Treeview(frame3, columns=('source', 'target',), height=15, show='headings')
tree_table.column('source', width=100, anchor='center')
tree_table.column('target', width=100, anchor='center')

tree_table.heading('source', text='Источник')
tree_table.heading('target', text='Цель')


tree_table.bind('<Double-1>', edit)
tree_table.pack(fill='both', expand=True)


root.mainloop()