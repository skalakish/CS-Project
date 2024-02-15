class Graph:
    def __init__(self):
        self.vertices = {}
        self.adj_matrix = []

    def add_vertex(self, vertex):
        if vertex not in self.vertices:
            self.vertices[vertex] = len(self.vertices)
            for row in self.adj_matrix:
                row.append(0)
            self.adj_matrix.append([0] * len(self.vertices))

    def add_edge(self, vertex1, vertex2):
        if vertex1 in self.vertices and vertex2 in self.vertices:
            index1 = self.vertices[vertex1]
            index2 = self.vertices[vertex2]
            self.adj_matrix[index1][index2] = 1
            self.adj_matrix[index2][index1] = 1

    def remove_vertex(self, vertex):
        if vertex in self.vertices:
            index = self.vertices[vertex]
            del self.vertices[vertex]
            self.adj_matrix.pop(index)
            for row in self.adj_matrix:
                row.pop(index)

    def __str__(self):
        result = "Adjacency Matrix:\n"
        for row in self.adj_matrix:
            result += " ".join(map(str, row)) + "\n"
        return result


def is_network_connected(graph):
    if not graph.vertices:
        return False


network = Graph()
network.add_vertex("A")
network.add_vertex("B")
network.add_edge("A", "B")
network.add_vertex("C")
network.add_edge("B", "C")
print(network)
print(is_network_connected(network))
