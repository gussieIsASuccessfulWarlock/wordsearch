def search_word(grid, word):
    rows, cols = len(grid), len(grid[0])
    directions = [(1, 1), (-1, -1), (1, -1), (-1, 1), (0, -1), (0, 1), (1, 0), (-1, 0)]
    
    def is_valid(row, col):
        return 0 <= row < rows and 0 <= col < cols
    
    def search_from(row, col):
        if grid[row][col] != word[0]:
            return False
        for dr, dc in directions:
            r, c, idx = row, col, 1
            while idx < len(word):
                r += dr
                c += dc
                if not is_valid(r, c) or grid[r][c] != word[idx]:
                    break
                idx += 1
            if idx == len(word):
                return True
        return False

    for r in range(rows):
        for c in range(cols):
            if search_from(r, c):
                return True
    return False


def mark_path(grid, path, marker):
    for (r, c) in path:
        grid[r][c] = marker

def search_word_with_path(grid, word):
    rows, cols = len(grid), len(grid[0])
    directions = [(1, 1), (-1, -1), (1, -1), (-1, 1), (0, -1), (0, 1), (1, 0), (-1, 0)]
    
    def is_valid(row, col):
        return 0 <= row < rows and 0 <= col < cols
    
    def search_from(row, col):
        if grid[row][col] != word[0]:
            return False, []
        for dr, dc in directions:
            r, c, idx = row, col, 1
            path = [(r, c)]
            while idx < len(word):
                r += dr
                c += dc
                if not is_valid(r, c) or grid[r][c] != word[idx]:
                    break
                path.append((r, c))
                idx += 1
            if idx == len(word):
                return True, path
        return False, []

    for r in range(rows):
        for c in range(cols):
            found, path = search_from(r, c)
            if found:
                return True, path
    return False, []

def findSOL(words, grid):
# Make a copy of the original grid to mark the paths
    marked_grid = [row[:] for row in grid]
    found_words_paths = {}
    for word in words:
        found, path = search_word_with_path(grid, word)
        if found:
            found_words_paths[word] = path
            mark_path(marked_grid, path, "*")
    return found_words_paths