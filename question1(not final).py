from collections import deque
class Graph:
    def __init__(self):
        self.graph = {}
        self.counter = 0

    def add_member(self, member_name, additional_info=None):
        if member_name not in self.graph:
            self.graph[member_name] = {'additional_info': additional_info, 'friends': set()}
        else:
            print(f"Member with name '{member_name}' already exists in the social network.")

    def add_relationship(self, member1_name, member2_name):
        if member1_name in self.graph and member2_name in self.graph:
            self.graph[member1_name]['friends'].add(member2_name)
            self.graph[member2_name]['friends'].add(member1_name)
        else:
            print("One or both members do not exist in the social network.")

    def get_members(self):
        return list(self.graph.keys())

    def get_member_info(self, member_name):
        if member_name in self.graph:
            return self.graph[member_name]
        else:
            print(f"Member with name '{member_name}' does not exist in the social network.")

    def initialise_counter(self):
        self.counter = 0

    def find_shortest_path(self, member1_name, member2_name):
        for member in self.graph[member1_name]['friends']:
            if member == member2_name:
                self.counter += 1
                return
            else:
                self.counter += 1
                for membr in self.graph[member1_name]['friends']:
                    self.find_shortest_path(membr, member2_name)
                

    def find_shortest_path(self, start_member, end_member):
        # Check if both members exist
        if start_member not in self.graph or end_member not in self.graph:
            print("One or both members do not exist.")
            return None
        
        visit_queue = deque([[start_member]])
        visited_queue = set([start_member])
        
        while visit_queue:
            
            path = visit_queue.popleft()
            current = path[-1]

            if current == end_member:
                return path
            
            for member in  self.graph[current]['friends']:
                if member not in visited_queue:
                    visited_queue.append(member)
                    new_path = list(path)
                    new_path.append(member)
                    visit_queue.append(new_path)


        return None

