from logic import format_dimensions, create_matrix, display_game, move, RANDOM_MOVES, MOVEMENTS

def main():
    """
    FIFTEEN: A simple game where the objective is to arrange all the numbers from left to right and top to bottom
    given a board of dimensions NxM, which always has one empty cell. The player can move the tiles in different
    directions using the empty space.

    The game is won when all elements are ordered from left to right, with the empty cell located in the bottom-right corner.

    Valid directions: 'a', 'w', 's', 'd'
    To end the game: 'o'
    """
    moves = 0
    move_limit = RANDOM_MOVES * 5

    board_dimensions = input('\nEnter the board dimensions (e.g., 4x3): ')

    game_matrix, backup_matrix = create_matrix(board_dimensions)

    # Show initial game state
    display_game(game_matrix, moves, move_limit)

    # Keep asking for inputs while the game is not finished
    while (game_matrix != backup_matrix) and (moves < move_limit):
        inputs = input('Input: ')

        for user_input in inputs:
            while user_input not in MOVEMENTS + ['o']:
                user_input = input(f'"{user_input}" is not valid, try again: ')

            if user_input == 'o':
                display_game(game_matrix, moves, move_limit)
                print('\nGame over...\n')
                return

            move(user_input, game_matrix)
            moves += 1

            if moves >= move_limit:
                display_game(game_matrix, moves, move_limit)
                print('\nYou lost :(\n')
                return

        display_game(game_matrix, moves, move_limit)

    print('\nYou won!!\n')

if __name__ == "__main__":
    main()
