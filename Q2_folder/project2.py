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
            raise ValueError("Error: Vertex does not exist in the graph.")

    def add_edge(self, v1, v2):
        if v1 in self.matrix and v2 in self.matrix:
            self.matrix[v1][v2] = 1
            self.matrix[v2][v1] = 1
        else:
            raise ValueError("Error: One or both vertices do not exist in the graph.")

    def remove_edge(self, vertex1, vertex2):
        if vertex1 in self.matrix and vertex2 in self.matrix:
            if vertex2 in self.matrix[vertex1]:
                del self.matrix[vertex1][vertex2]
            if vertex1 in self.matrix[vertex2]:
                del self.matrix[vertex2][vertex1]
        else:
            raise ValueError("Error: At least one vertex does not exist in the graph or there is no such edge.")

    def display_matrix(self):
        keys = sorted(self.matrix.keys())
        print('    ' + '  '.join(keys))

        for key in keys:
            row_str = key + '  '
            for k in keys:
                if k in self.matrix[key]:
                    row_str += '1  '
                else:
                    row_str += '0  '
            print(row_str)

    def is_network_connected(self):
        visited = set()

        def dfs(vertex):
            visited.add(vertex)
            for neighbour in self.matrix[vertex]:
                if neighbour not in visited:
                    dfs(neighbour)

        if not self.matrix:
            return False

        v_st = next(iter(self.matrix))
        dfs(v_st)

        return len(visited) == len(self.matrix)

    def create_ring_network(self, nodes):
        self.matrix = {key: {} for key in nodes}
        for i in range(len(nodes)):
            self.add_edge(nodes[i], nodes[(i + 1) % len(nodes)])

    def create_star_network(self, hub, *nodes):
        self.matrix = {}
        self.add_vertex(hub)
        for node in nodes:
            self.add_vertex(node)
            self.add_edge(hub, node)


network = Graph()

network.add_vertex("Computer1")
network.add_vertex("Computer2")
network.add_edge("Computer1", "Computer2")

print("Network Connectivity:", "Connected" if network.is_network_connected() else "Disconnected")

network.add_vertex("Computer3")
network.add_vertex("Computer4")
network.add_edge("Computer3", "Computer4")

print("Network Connectivity:", "Connected" if network.is_network_connected() else "Disconnected")

print("Adjacency Matrix:")
network.display_matrix()

print("\nCreating a Ring Network:")
ring_network = Graph()
ring_network.create_ring_network(["ComputerA", "ComputerB", "ComputerC", "ComputerD", "ComputerE", "ComputerF"])
print("Ring Network Connectivity:", "Connected" if ring_network.is_network_connected() else "Disconnected")
print("Adjacency Matrix for Ring Network:")
ring_network.display_matrix()

print("\nCreating a Star Network:")
star_network = Graph()
star_network.create_star_network("CentralHub", "Node1", "Node2", "Node3", "Node4", "Node5")
print("Star Network Connectivity:", "Connected" if star_network.is_network_connected() else "Disconnected")
print("Adjacency Matrix for Star Network:")
star_network.display_matrix()
