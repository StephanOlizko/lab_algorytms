import networkx as nx
import time


def all_traverses(G, start_node):
    stk = [[start_node]] # Стек для хранения путей
    line = [[start_node]] # Очередь для хранения путей


    traverses = []
    # Максимум 1 секунда
    start_time = time.time()
    while line and time.time() < start_time + 1:
        #print(line, traverses)

        path = line.pop(0)
        node = path[-1]
        if len(set(path)) == len(G.nodes):
            traverses.append(path)
        else:
            for neighbor in G.neighbors(node):
                line.append(path + [neighbor])

    # Из обходов удалим повторяющиеся вершины из путей
    ans = []
    for traverse in traverses:
        tmp = []
        for i in traverse:
            if i not in tmp:
                tmp.append(i)
        if tmp not in ans:
            ans.append(tmp)

    return ans



if __name__ == '__main__':
    # Создать граф
    G = nx.Graph()
    G.add_nodes_from(range(5))
    G.add_edges_from([(0, 1), (0, 2), (1, 3), (1, 4)])

    # Получить все обходы
    traverses = all_traverses(G, 0)
    print(traverses)
