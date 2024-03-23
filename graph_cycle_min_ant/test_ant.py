import networkx as nx
import random
import multiprocessing
import time
import threading

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
    def __init__(self, graph, num_ants, decay_rate, influence, mode='serial'):
        print(mode)
        self.graph = graph
        self.num_ants = num_ants
        self.decay_rate = decay_rate
        self.influence = influence
        self.pheromones = {(i, j): 1 for i in graph.nodes for j in graph.nodes if i != j}
        self.ants = [Ant(graph) for _ in range(num_ants)]
        self.mode = mode

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

    def search_serial(self, iterations):
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

            self.update_pheromones()

        return min(self.ants, key=lambda ant: ant.path_length)

    def search_parallel(self, iterations):
        results = []
        lock = threading.Lock()

        def process_ant(ant):
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

            with lock:
                results.append(ant)

        for _ in range(iterations):
            threads = []
            for ant in self.ants:
                thread = threading.Thread(target=process_ant, args=(ant,))
                thread.start()
                threads.append(thread)

            for thread in threads:
                thread.join()

            best_ant = min(results, key=lambda ant: ant.path_length)
            self.update_pheromones()

        return best_ant

    def search(self, iterations):
        if self.mode == 'serial':
            return self.search_serial(iterations)
        elif self.mode == 'parallel':
            return self.search_parallel(iterations)
        else:
            raise ValueError("Invalid mode. Use 'serial' or 'parallel'.") 

#Usecase
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

def generate_full_graph(n):
    G = nx.DiGraph()
    for i in range(n):
        for j in range(n):
            if i != j:
                G.add_edge(i, j, weight=random.randint(1, 10))
    return G

if __name__ == '__main__':
    #colony = AntColony(Gdefault, 10, 0.1, 1, mode='serial')
    Gdefault = generate_full_graph(50)

    start = time.time()
    colony = AntColony(Gdefault, 10, 0.1, 1, mode='parallel')
    best_ant = colony.search(10)
    end = time.time()
    print(end - start)

    print(best_ant.path)
    print(best_ant.path_length)
    print("________________________")

    start = time.time()
    colony = AntColony(Gdefault, 10, 0.1, 1, mode='serial')
    best_ant = colony.search(10)
    end = time.time()
    print(end - start)

    print(best_ant.path)
    print(best_ant.path_length)