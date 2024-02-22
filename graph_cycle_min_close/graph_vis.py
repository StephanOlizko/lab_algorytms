import tkinter as tk
import networkx as nx

node_id = None
node_coords = None


def add_node(event):
    node_id = len(G.nodes) + 1
    G.add_node(node_id, pos=(event.x, event.y))
    canvas.create_oval(event.x-10, event.y-10, event.x+10, event.y+10, fill='red')
    canvas.create_text(event.x, event.y, text=str(node_id))


def add_edge_on_right_click(event):
    global node_id

    if node_id is None:
        for node in G.nodes:
            x, y = G.nodes[node]['pos']
            if (x - event.x)**2 + (y - event.y)**2 < 100:
                node_id = node
                break

    else:
        for node in G.nodes:
            x, y = G.nodes[node]['pos']
            if (x - event.x)**2 + (y - event.y)**2 < 100:
                if node_id == node:
                    x1, y1 = G.nodes[node_id]['pos']
                    canvas.create_oval(x1, y1, x1+15, y1+15, width=2)
                else:
                    G.add_edge(node_id, node)
                    x1, y1 = G.nodes[node_id]['pos']
                    x2, y2 = G.nodes[node]['pos']
                    canvas.create_line(x1, y1, x2, y2, width=2)
                    node_id = None
                    break


        
root = tk.Tk()
canvas = tk.Canvas(root, width=400, height=400)
canvas.pack()

G = nx.Graph()

canvas.bind('<Button-1>', add_node)
canvas.bind('<Button-3>', add_edge_on_right_click)

root.mainloop()