#create Graph class
class Graph():
    def __init__(self):
        self.graph = {}
    
    def add_member(self, u):
        if u not in self.graph.keys():
            self.graph[u] = []

    def add_relationship(self, u, v):
        if v not in self.graph[u]:
            self.graph[u].append(v)
    
#create member class
class Member():
    def __init__(self, name, age, location):
        self.name = name
        self.age = age
        self.location = location


    def __str__(self):
        return f"Name: {self.name}, Age: {self.age}, Location: {self.location} "

#method to add new members


# method to add new relationship




#method to find all friends



#  method to find the path between two members
