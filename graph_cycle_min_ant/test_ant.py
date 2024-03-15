import networkx as nx
import random

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

    def __str__(self) -> str:
        return f'Ant({self.path}, {self.path_length})'

class AntColony:
    def __init__(self, graph, num_ants, decay_rate, alpha=1, beta=1):
        self.graph = graph
        self.num_ants = num_ants
        self.decay_rate = decay_rate
        self.alpha = alpha
        self.beta = beta
        self.pheromones = {(i, j): 1 for i in graph.nodes for j in graph.nodes if i != j}
        self.ants = [Ant(graph) for _ in range(num_ants)]

    def update_pheromones(self):
        for i, j in self.pheromones.keys():
            self.pheromones[(i, j)] *= (1 - self.decay_rate)
        for ant in self.ants:
            for i in range(len(ant.path) - 1):
                self.pheromones[(ant.path[i], ant.path[i+1])] += 1 / ant.path_length

    def choose_next_node(self, ant):
        probabilities = []
        for node in self.graph.nodes:
            if ant.can_visit(node):
                pheromone = self.pheromones[(ant.current_node, node)] ** self.alpha
                distance = self.graph[ant.current_node][node]['weight'] ** (-self.beta)
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
        for _ in range(iterations):
            for ant in self.ants:
                while len(ant.path) < len(self.graph.nodes):
                    next_node = self.choose_next_node(ant)
                    if next_node is None:
                        break
                    ant.visit(next_node)

                print(ant)
                if ant.path[-1] != ant.path[0]:
                    if self.graph.has_edge(ant.path[-1], ant.path[0]):
                        ant.visit(ant.path[0])
                    else:
                        ant.path_length = float('inf')

            self.update_pheromones()


        return min(self.ants, key=lambda ant: ant.path_length)


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

colony = AntColony(Gdefault, 10, 0.5)
best_ant = colony.search(10)

print(best_ant.path)
print(best_ant.path_length)
#print(*colony.ants)