def find_neighbors(word, wordlist):
    results = []
    for i in range(len(word)):
        for replacement_char in 'abcdefghijklmnopqrstuvwxyz':
            if replacement_char != word[i]:
                new_word = word[:i] + replacement_char + word[i + 1:]
                if new_word in wordlist and new_word != word:
                    results.append(new_word)
    return results






word = input("Enter the word")
list = open('words_alpha.txt', 'r')
wordlist =list.readlines()
find_neighbors(word, wordlist)

