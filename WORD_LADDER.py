def find_neighbors(word, word_list):
    neighbors = []
    for i in range(len(word)):
        for c in 'abcdefghijklmnopqrstuvwxyz':
            new_word = word[:i] + c + word[i+1:]
            if new_word in word_list:
                neighbors.append(new_word)
    return neighbors

def word_ladder(start, end, word_list):
    if start == end:
        return 0

    queue = [(start, [start])]
    visited = set([start])

    while queue:
        word, path = queue.pop(0)
        neighbors = find_neighbors(word, word_list)

        for neighbor in neighbors:
            if neighbor == end:
                return path + [neighbor]
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))

    return 0

# Example usage
word_list = {"cat", "cot", "dot", "dog", "bat", "rat", ...}  # Replace with your word list
start_word = "cat"
end_word = "dog"
shortest_path = word_ladder(start_word, end_word, word_list)

if shortest_path:
    print(f"Shortest word ladder: {' -> '.join(shortest_path)}")
else:
    print("No ladder found.")