import random

EMPTY = ""
MOVEMENTS = ['a', 'w', 'd', 's']
RANDOM_MOVES = 50

def format_dimensions(dimensions):
    """
    Function that receives the game dimensions in the format numxnum and returns both numbers separately.
    If the input format is not as expected, it asks for the dimensions again.
    """
    while True:
        if 'x' in dimensions:
            dimension_1, dimension_2 = dimensions.split('x')
            if dimension_1.isdigit() and dimension_2.isdigit():
                return int(dimension_1), int(dimension_2)
        dimensions = input('Enter valid dimensions (e.g., 4x3): ')

def create_matrix(board_dimensions):
    """
    Function that receives the board dimensions and returns a shuffled matrix of N rows x M columns
    filled with numbers from 1 to (N * M - 1). To shuffle, it uses random.choice and calls the move()
    function, sending a random move and the matrix as parameters.
    """
    N, M = format_dimensions(board_dimensions)

    num = 1
    matrix = [[num + col + row * M for col in range(M)] for row in range(N)]
    backup_matrix = [row[:] for row in matrix]

    matrix[-1][-1] = EMPTY
    backup_matrix[-1][-1] = EMPTY

    for _ in range(RANDOM_MOVES):
        move(random.choice(MOVEMENTS), matrix)

    return matrix, backup_matrix

def display_game(matrix, moves, move_limit):
    """
    Function that receives a matrix and prints it in the specified format,
    along with game instructions and move counts.
    """
    print("\n====", "Fifteen", "====")
    print('\n'.join(['  |'.join(['{:3}'.format(num) for num in row]) for row in matrix]))
    print("\nControls: w, a, s, d")
    print("Exit the game: o")
    print('Moves made: ', moves)
    print('Moves remaining: ', move_limit - moves)

def move(direction, matrix):
    """
    Function that receives a direction (already validated as valid) and the matrix to alter,
    and returns the same matrix with positions changed according to the move.
    Valid directions: 'a', 'w', 's', 'd'
    """
    empty_row, empty_col = locate_empty(matrix)
    new_row, new_col = empty_row, empty_col

    if direction == 'w':
        new_row = empty_row + 1
    elif direction == 's':
        new_row = empty_row - 1
    elif direction == 'a':
        new_col = empty_col + 1
    elif direction == 'd':
        new_col = empty_col - 1

    if 0 <= new_row < len(matrix) and 0 <= new_col < len(matrix[new_row]):
        matrix[empty_row][empty_col] = matrix[new_row][new_col]
        matrix[new_row][new_col] = EMPTY

def locate_empty(matrix):
    """
    Function that locates the empty cell in a matrix.
    """
    for row in range(len(matrix)):
        for col in range(len(matrix[row])):
            if matrix[row][col] == EMPTY:
                return row, col
