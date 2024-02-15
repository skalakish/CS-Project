def get_adjacency_matrix(self)
    vertices =list(self.graph.keys())
    matrix = [[0 for _ in vertices]] for _ in vertices]
        
    for i, vertex1 in enumerate(vertices):
        for j, vertex2 in enumerate(vertices):
            if vertex2 in self.graph[vertex1]:
                matrix[i][j] = 1

    return matrix
    