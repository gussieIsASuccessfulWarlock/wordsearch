import os
import random
from rich import print
from another import findSOL

# Picks random words from the dictionary that have a certain number of letters
def getWords(numofletters=4, maxwords=10):
    #file_location = "/usr/share/dict/words"
    file_location = os.path.join(os.path.dirname(__file__), "list.txt")
    words = []
    # Read the file in a random order
    with open(file_location, "r") as file:
        lines = file.readlines()
        random.shuffle(lines)
        for line in lines:
            if len(line) == numofletters + 1:
                words.append(line.strip())
            if len(words) >= maxwords:
                break
    return words

# checks if placment of word is possible
def is_placeable(word, row, col, grid, direction):
    for i in range(len(word)):
        new_row = row + i * direction[0]
        new_col = col + i * direction[1]
        if new_row >= len(grid) or new_col >= len(grid[0]) or new_row < 0 or new_col < 0:
            return False  # Out of bounds
        if grid[new_row][new_col] != ' ' and grid[new_row][new_col] != word[i]:
            return False  # Conflict with an existing letter
    return True

#Place a word on the grid at the specified location and direction.
def place_word(word, row, col, grid, direction):
    for i in range(len(word)):
        new_row = row + i * direction[0]
        new_col = col + i * direction[1]
        grid[new_row][new_col] = word[i]

#Remove word from grid
def remove_word(word, row, col, grid, direction):
    for i in range(len(word)):
        new_row = row + i * direction[0]
        new_col = col + i * direction[1]
        grid[new_row][new_col] = ' '

#Attempt to place words onto the grid according to the rules specified.
def find_solution(four_letter_words, long_word, grid, used_words):
    if not four_letter_words:  # Base case: all four-letter words have been placed
        return grid
    
    # Randomly shuffle the words to get a different starting point each time
    random.shuffle(four_letter_words)
    four_letter_words.append(long_word)

    for word in four_letter_words:
        if word not in used_words:
            for row in range(len(grid)):
                for col in range(len(grid[0])):
                    for direction in [(1, 1), (-1, -1), (1, -1), (-1, 1), (0, -1), (0, 1), (1, 0), (-1, 0)]:
                        if is_placeable(word, row, col, grid, direction):
                            place_word(word, row, col, grid, direction)
                            used_words.add(word)
                            print("Placing word: " + word, end="\r")
                            remaining_words = [w for w in four_letter_words if w not in used_words]
                            
                            # Recursive call to try to place the remaining words
                            result = find_solution(remaining_words, long_word, grid, used_words)
                            if result is not None:
                                return result  # Success
                            
                            # Backtrack
                            remove_word(word, row, col, grid, direction)
                            used_words.remove(word)

    return None
# 2 -4
# 4 -5
# 1 -6
# 1 -7
# 1 -9

def genGRID():
    empty_grid = [[' ' for _ in range(6)] for _ in range(8)]
    four_letter_words = []
    for i in getWords(4, 5):
        four_letter_words.append(i.upper())
    for i in getWords(5, 4):
        four_letter_words.append(i.upper())
    long_word = getWords(6, 1)[0]
    solution_grid = find_solution(four_letter_words, long_word, empty_grid, set())

    # Fill remaining empty cells with random letters
    for row in range(len(solution_grid)):
        for col in range(len(solution_grid[0])):
            if solution_grid[row][col] == ' ':
                solution_grid[row][col] = chr(random.randint(65, 90))

    findSOLOutput = findSOL(four_letter_words, solution_grid)
    return solution_grid, findSOLOutput