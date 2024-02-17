class Graph:
    def __init__(self):
        self.matrix = {}

    def add_vertex(self, vertex):
        if vertex not in self.matrix:
            self.matrix[vertex] = {}

    def remove_vertex(self, vertex):
        if vertex in self.matrix:
            for connected_vertex in self.matrix[vertex]:
                del self.matrix[connected_vertex][vertex]
            del self.matrix[vertex]
        else:
            raise ValueError("Vertex does not exist in the graph.")

    def add_edge(self, v1, v2):
        if v1 in self.matrix and v2 in self.matrix:
            self.matrix[v1][v2] = 1
            self.matrix[v2][v1] = 1
        else:
            raise ValueError("One or both vertices do not exist in the graph.")

    def remove_edge(self, vertex1, vertex2):
        if vertex1 in self.matrix and vertex2 in self.matrix:
            if vertex2 in self.matrix[vertex1]:
                del self.matrix[vertex1][vertex2]
            if vertex1 in self.matrix[vertex2]:
                del self.matrix[vertex2][vertex1]
        else:
            raise ValueError("One or both vertices do not exist in the graph or there is no edge between them.")

    def display_matrix(self):
        keys = sorted(self.matrix.keys())
        print('   ' + '  '.join(keys))

        for key in keys:
            row = [self.matrix[key].get(k, 0) for k in keys]
            print(key, row)

    def is_network_connected(self):
        visited = set()

        def dfs(vertex):
            visited.add(vertex)
            for neighbour in self.matrix[vertex]:
                if neighbour not in visited:
                    dfs(neighbour)

        if not self.matrix:
            return False

        start_vertex = next(iter(self.matrix))
        dfs(start_vertex)

        return len(visited) == len(self.matrix)

    def ring_network(self, nodes):
        self.matrix = {key: {} for key in nodes}
        for i in range(0, len(nodes) - 1):
            self.add_edge(nodes[i], nodes[i + 1])

        self.add_edge(nodes[-1], nodes[0])

    def create_star_network(self, hub, *nodes):
        self.matrix = {}
        self.add_vertex(hub)
        for node in nodes:
            self.add_vertex(node)
            self.add_edge(hub, node)



network = Graph()


network.add_vertex("A")
network.add_vertex("B")
network.add_edge("A", "B")


print("Is the network connected?", network.is_network_connected())


network.add_vertex("C")
network.add_vertex("D")
network.add_edge("C", "D")


print("Is the network connected?", network.is_network_connected())


network.display_matrix()


ring_network = Graph()
ring_network.ring_network(["A", "B", "C", "D", "E", "F"])
print("\nRing Network:")
ring_network.display_matrix()
print("Is the ring network connected?", ring_network.is_network_connected())


star_network = Graph()
star_network.create_star_network("Hub", "Node1", "Node2", "Node3", "Node4", "Node5")
print("\nStar Network:")
star_network.display_matrix()
print("Is the star network connected?", star_network.is_network_connected())
