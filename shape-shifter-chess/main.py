import csv
import os
import random
import gamelib

BOARD_WIDTH = 400
BOARD_HEIGHT = 400
SQUARE_SIZE = BOARD_WIDTH // 8
SQUARES = 8
EMPTY = ''
ACTIVE_PIECE = 'active'
POSSIBLE_PIECE = 'possible'
TEXT_INDENT = SQUARE_SIZE * 0.5
MOVEMENTS_PATH = 'data/movements.csv'
SAVED_GAME_PATH = 'data/saved.csv'
PROMPT_RESPONSES = {'yes': True, 'no': False}


def load_game():
    '''
    Returns the saved game board from saved_game.csv, and the respective level.
    '''
    game = [['' for j in range(SQUARES)] for i in range(SQUARES)]
    level = 0

    with open(SAVED_GAME_PATH) as saved_game:
        for row in csv.reader(saved_game):
            position, piece, state = row
            row, col = position.split(';')
            game[int(row)][int(col)] = (piece, state)
            level += 1
            
    return game, level - 2


def save_game(game):
    with open(SAVED_GAME_PATH, "w", newline='') as saved_game:
        writer = csv.writer(saved_game)
        for row in range(len(game)):
            for col in range(len(game[row])):
                if game[row][col] != EMPTY:
                    piece, state = game[row][col]
                    writer.writerow([f'{row};{col}', piece, state])


def load_piece_movements():
    '''
    Returns a dictionary with pieces as keys and a list of their possible movements as values.
    '''
    movements = {}

    with open(MOVEMENTS_PATH) as moves:
        for line in csv.reader(moves):
            piece, direction, extensible = line
            direction = direction.split(';')

            if extensible == 'true':
                for i in range(1, SQUARES + 1):
                    movements[piece] = movements.get(piece, []) + [tuple(i * int(x) for x in direction)]
            else:
                movements[piece] = movements.get(piece, []) + [tuple(int(x) for x in direction)]
    
    return movements


def new_game(movements, level):
    '''
    Creates a new game depending on the given level, with its active piece and possible ones.
    '''
    game = [['' for j in range(SQUARES)] for i in range(SQUARES)]
    
    original_x, original_y = random.randint(0, SQUARES - 1), random.randint(0, SQUARES - 1)
    original_piece = random.choice(list(movements))
    
    game[original_y][original_x] = (original_piece, ACTIVE_PIECE)
    
    piece = original_piece
    x, y = original_x, original_y
    
    for i in range(1, level + 2):
        while True:
            dir_x, dir_y = random.choice(movements[piece])
            sum_x, sum_y = x + dir_x, y + dir_y

            if sum_x in range(SQUARES) and sum_y in range(SQUARES) and game[sum_y][sum_x] == EMPTY:
                piece = random.choice(list(movements))
                x, y = sum_x, sum_y 
                game[sum_y][sum_x] = (piece, '')
                
                if (dir_x, dir_y) in movements[original_piece]:
                    game[sum_y][sum_x] = (piece, POSSIBLE_PIECE)
                    
                break

    save_game(game)
    return game


def update_active_piece(game, piece, square_x, square_y):
    # Find the position of the active piece and clear the state of all pieces
    active_x, active_y = '', ''

    for row in range(len(game)):
        for col in range(len(game[row])):
            if game[row][col] != EMPTY:
                if game[row][col][1] == ACTIVE_PIECE:
                    active_x, active_y = col, row
                game[row][col] = (game[row][col][0], '')

    game[square_y][square_x] = (piece, ACTIVE_PIECE)
    game[active_y][active_x] = EMPTY


def update_possible_pieces(game, piece, square_x, square_y, movements):
    # Change the state of the new possible pieces
    for direction in movements[piece]:
        dir_x, dir_y = direction

        for row in range(len(game)):
            for col in range(len(game[row])):
                sum_x, sum_y = dir_x + square_x, dir_y + square_y
                if sum_x == col and sum_y == row and game[row][col] != EMPTY:
                    game[row][col] = (game[row][col][0], POSSIBLE_PIECE)

def update_game(movements, game, x, y):
    '''
    Updates the game and the state of the pieces depending on the performed move.
    '''
    square_x, square_y = x // SQUARE_SIZE, y // SQUARE_SIZE
    
    if not square_x in range(SQUARES) or not square_y in range(SQUARES) or game[square_y][square_x] == EMPTY:
        return game

    piece, state = game[square_y][square_x]

    if state != POSSIBLE_PIECE:
        return game
    
    update_active_piece(game, piece, square_x, square_y)
    update_possible_pieces(game, piece, square_x, square_y, movements)

    return game


def display_game(game, level):
    '''
    Draws the chess board with the pieces in their corresponding states.
    '''
    gamelib.draw_begin()

    gamelib.draw_rectangle(0, 0, BOARD_WIDTH, BOARD_HEIGHT + 75, fill="black")

    for square_x in range(SQUARES):
        for square_y in range(SQUARES):
            if (square_x + square_y) % 2 == 0:
                gamelib.draw_rectangle(square_x * SQUARE_SIZE + 2, square_y * SQUARE_SIZE + 2, SQUARE_SIZE * (square_x + 1) - 2, SQUARE_SIZE * (square_y + 1) - 2, fill='#2D2D3F')
            else:
                gamelib.draw_rectangle(square_x * SQUARE_SIZE + 2, square_y * SQUARE_SIZE + 2, SQUARE_SIZE * (square_x + 1) - 2, SQUARE_SIZE * (square_y + 1) - 2, fill='#171717')

            if game[square_y][square_x] != EMPTY:
                piece, state = game[square_y][square_x]

                if state == ACTIVE_PIECE:
                    gamelib.draw_image(f"images/{piece}_rojo.gif", (square_x * SQUARE_SIZE) + 3, (square_y * SQUARE_SIZE) + 3)
                elif state == POSSIBLE_PIECE:
                    gamelib.draw_rectangle(square_x * SQUARE_SIZE + 3, square_y * SQUARE_SIZE + 3, SQUARE_SIZE * (square_x + 1) - 2, SQUARE_SIZE * (square_y + 1) - 2, fill='', outline='red', width='2')
                    gamelib.draw_image(f"images/{piece}_blanco.gif", (square_x * SQUARE_SIZE) + 3, (square_y * SQUARE_SIZE) + 3)
                elif state == '':
                    gamelib.draw_image(f"images/{piece}_blanco.gif", (square_x * SQUARE_SIZE) + 3, (square_y * SQUARE_SIZE) + 3)

    gamelib.draw_text('SHAPE SHIFTER CHESS', TEXT_INDENT, BOARD_HEIGHT + 15, size=10, bold=True, anchor='nw')
    gamelib.draw_text(f'Level: {level}', TEXT_INDENT, BOARD_HEIGHT + 40, size=10, bold=True, anchor='nw')
    gamelib.draw_text('Exit: Esc', TEXT_INDENT + BOARD_WIDTH // 2, BOARD_HEIGHT + 15, size=10, bold=True, anchor='nw')
    gamelib.draw_text('Retry: Z', TEXT_INDENT + BOARD_WIDTH // 2, BOARD_HEIGHT + 40, size=10, bold=True, anchor='nw')

    gamelib.draw_end()

def main():
    movements = load_piece_movements()
    game = []
    level = 0 
    load = None
    
    # Check if there is a saved game to load
    if os.path.exists(SAVED_GAME_PATH):
        while True:
            load = gamelib.input('Do you want to continue the saved game? (Yes/No)')
            if load is None:
                return
            if load.lower() in PROMPT_RESPONSES:
                load = PROMPT_RESPONSES[load.lower()]
                break

    if load:
        game, level = load_game()
    else:
        level = 1
        game = new_game(movements, level)
    
    gamelib.title("Shape Shifter Chess")
    gamelib.resize(BOARD_WIDTH, BOARD_HEIGHT + 75)

    while gamelib.is_alive():
        display_game(game, level)

        ev = gamelib.wait()
        if not ev:
            break

        if ev.type == gamelib.EventType.ButtonPress and ev.mouse_button == 1:
            # Check if the level is passed based on the pieces on the board
            x, y = ev.x, ev.y
            game = update_game(movements, game, x, y)
                
            pieces_on_board = [game[row][col] for row in range(len(game)) for col in range(len(game[row])) if game[row][col] != EMPTY]
            
            if len(pieces_on_board) == 1:
                level += 1
                game = new_game(movements, level)
            
        elif ev.type == gamelib.EventType.KeyPress:

            if ev.key == 'Escape':
                # End game
                break

            if ev.key.lower() == 'z':
                # Retry game
                game, level = load_game()

gamelib.init(main)
