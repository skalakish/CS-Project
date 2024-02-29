def find_neighbors(word, wordlist):
    results = []
    for i in range(len(word)):
        for replacement_char in 'abcdefghijklmnopqrstuvwxyz':
            if replacement_char != word[i]:
                new_word = word[:i] + replacement_char + word[i + 1:]
                if new_word + '\n' in wordlist and new_word != word:
                    results.append(new_word)
    return results

word = input("Enter the word: ")
with open('words_alpha.txt', 'r') as file:
    wordlist = file.readlines()

neighbors = find_neighbors(word, wordlist)
print("Neighbors of", word, ":", neighbors)
