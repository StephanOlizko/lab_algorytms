import streamlit as st
import matplotlib.pyplot as plt
import networkx as nx
from all_traverses import all_traverses
import pandas as pd

# Игнорируем предупреждения
#st.set_option('deprecation.showPyplotGlobalUse', False)


# Ввести случайный граф дерево или ввести граф вручную
if st.checkbox('Создать случайное дерево'):
    num_nodes = st.number_input('Введите количество вершин', min_value=1, value=1)

    # Создать случайное дерево
    G = nx.random_tree(num_nodes, seed=42)
else:
    # Запросить у пользователя количество вершин и ребер
    num_nodes = st.number_input('Введите количество вершин', min_value=1, value=1)
    num_edges = st.number_input('Введите количество ребер', min_value=0, max_value=(num_nodes * (num_nodes - 1) // 2), value=0)

    # Создать пустой граф
    G = nx.Graph()

    # Добавить вершины
    G.add_nodes_from(range(num_nodes))

    # Запросить у пользователя ребра
    for i in range(num_edges):
        edge = st.text_input(f'Введите ребро {i+1} в формате "node1-node2"', value=f'{i}-{(i+1)%num_nodes}')
        node1, node2 = map(int, edge.split('-'))
        G.add_edge(node1, node2)

    # Проверим что граф является деревом инчае выдадим предупреждение
    if not nx.is_tree(G):
        st.warning('Граф не является деревом')
        st.stop()


# Добавить атрибуты к вершинам в зависимости от слоя
for node in G.nodes:
    #Посчитать расстояние от вершины до корня 
    try:
        G.nodes[node]['layer'] = nx.shortest_path_length(G, 0, node)
    except nx.NetworkXNoPath:
        raise ValueError('Граф не является деревом')
# Изменим атрибуты вершин так чтобы 0 была в самом верху
for node in G.nodes:
    G.nodes[node]['layer'] = num_nodes - G.nodes[node]['layer']


# Визуализировать граф в виде дерева с вершиной 0
graph = plt.figure()
pos = nx.multipartite_layout(G, subset_key="layer", align="horizontal")
nx.draw(G, pos, with_labels=True, node_size=2000, node_color='skyblue')
plt.title('Граф')
st.pyplot(graph)


# Запросить у пользователя начальную вершину (по умолчанию 0)
start_node = st.number_input('Введите начальную вершину', min_value=0, max_value=num_nodes-1, value=0)

# Получить все обходы кнопка, сохраним состояние перед этим чтобы случайный граф не пересоздавался
if st.button('Получить все обходы'):
    traverses = all_traverses(G, start_node)
    st.write('Количество обходов:', len(traverses))

    # Выведем обходы в виде таблицы, где в каждой строке будет один обход, стобец один - номер обхода, столбец два - обход
    st.write('Обходы:')
    
    traverses = [" -> ".join(map(str, traverse)) for traverse in traverses]
    df = pd.DataFrame(traverses, columns=['Обход'])

    st.write(df)


