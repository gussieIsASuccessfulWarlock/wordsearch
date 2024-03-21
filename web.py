from flask import Flask, render_template
from run import genGRID

app = Flask(__name__)

colors = ['red', 'green', 'blue', 'orange', 'purple', 'sky', 'pink', 'yellow', 'indigo', 'teal', 'lime', 'amber', 'cyan']

def findOverlappingCorradinates(cordiantes):
    # cordiantes = {'must': [(0, 0), (1, 1), (2, 2), (3, 3)], 'Zipa': [(1, 0), (2, 1), (3, 2), (4, 3)], 'jink': [(2, 0), (3, 1), (4, 2), (5, 3)], 'crus': [(0, 1), (1, 2), (2, 3), (3, 4)], 'dunelike': [(0, 5), (1, 5), (2, 5), (3, 5), (4, 5), (5, 5), (6, 5), (7, 5)]}
    overlapping = []
    # Create a list of all the overlapping coordinates
    positions = [position for positions in cordiantes.values() for position in positions]
    for i in positions:
        if positions.count(i) > 1 and i not in overlapping:
            overlapping.append(i)
    # Get the overlapping words into object like {cordiantes: [(0, 0)], words: ['must', 'crus']}
    overlapping_dict = []
    for i in overlapping:
        # get the overlapping words
        words = []
        # find the words that contain i in their positions
        for word, positions in cordiantes.items():
            if i in positions:
                words.append(word)
        overlapping_dict.append({'cordiantes': i, 'words': words})
    return overlapping_dict

@app.route('/')
def display_matrix():
    # Generate the matrix
    matrix, words = genGRID()
    print(matrix)
    print(words)
    # Assign colors to words
    color_map = {word: colors[index % len(colors)] for index, word in enumerate(words)}
    # get the color of the overlapping words
    overlapping = findOverlappingCorradinates(words)
    # add a border to each word that is overlapping
    # Create a copy of the matrix where each letter is associated with its color
    colored_matrix = [[{'letter': letter, 'color': 'black'} for letter in row] for row in matrix]
    for word, positions in words.items():
        for x, y in positions:
            colored_matrix[x][y]['color'] = color_map[word]
    for i in overlapping:
        x, y = i['cordiantes']
        color_one = color_map[i['words'][0]]
        color_two = color_map[i['words'][1]]
        current_color = colored_matrix[x][y]['color']
        if current_color == color_one:
            colored_matrix[x][y]['border'] = 'border border-2 border-' + color_two + '-500'
        else:
            colored_matrix[x][y]['border'] = 'border border-2 border-' + color_one + '-500'
    # Colors list
    list_of_colors = []
    for word, color in color_map.items():
        list_of_colors.append({'word': word, 'color': color})
    return render_template("matrix.html", matrix=colored_matrix, words=list_of_colors)

if __name__ == '__main__':
    app.run(debug=True)