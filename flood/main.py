import gamelib
from game.flood import COLORS
from game.flood_game import FloodGame

# Constants to initialize the game state
# If N_COLORS is greater than 10, more entries must be added to
# the COLORS array below.
GAME_WIDTH = 15
GAME_HEIGHT = 12
N_COLORS = 5

# Visual constants
CELL_SIZE = 35
LINE_WIDTH = 2
SHOW_NUMBERS = False  # useful to enable if colors are not clear

MARGIN = 20

MOVE_HEIGHT = GAME_HEIGHT * CELL_SIZE + MARGIN * 2
BUTTONS_HEIGHT = MOVE_HEIGHT + MARGIN
BUTTONS_WIDTH = (GAME_WIDTH * CELL_SIZE - MARGIN) // 2
WINDOW_WIDTH = GAME_WIDTH * CELL_SIZE + MARGIN * 2
WINDOW_HEIGHT = BUTTONS_HEIGHT + (CELL_SIZE + MARGIN) * 2

def create_game():
    game = FloodGame(GAME_HEIGHT, GAME_WIDTH, N_COLORS)
    return game

def handle_click(game, x, y):
    row = (y - MARGIN) // CELL_SIZE
    col = (x - MARGIN) // CELL_SIZE

    height, width = game.dimensions()

    if 0 <= row < height and 0 <= col < width:
        color = game.get_color(
            (y - MARGIN) // CELL_SIZE,
            (x - MARGIN) // CELL_SIZE
        )
        game.change_color(color)

    # First row of buttons
    if 0 <= y - BUTTONS_HEIGHT < CELL_SIZE:
        if 0 <= x - MARGIN < BUTTONS_WIDTH:
            game.undo()
        if 0 <= x - MARGIN * 2 - BUTTONS_WIDTH < BUTTONS_WIDTH:
            game.redo()

    # Second row of buttons
    if 0 <= y - BUTTONS_HEIGHT - CELL_SIZE - MARGIN < CELL_SIZE:
        if 0 <= x - MARGIN < BUTTONS_WIDTH:
            return create_game()
        if 0 <= x - MARGIN * 2 - BUTTONS_WIDTH < BUTTONS_WIDTH:
            game.calculate_new_solution()

    return game

def display_grid(game):
    height, width = game.dimensions()

    # Display the colored squares
    for r in range(height):
        for c in range(width):
            color = game.get_color(r, c)
            gamelib.draw_rectangle(
                c * CELL_SIZE + MARGIN,
                r * CELL_SIZE + MARGIN,
                (c + 1) * CELL_SIZE + MARGIN,
                (r + 1) * CELL_SIZE + MARGIN,
                fill=COLORS[color],
                width=0
            )
            if game.has_next_step() and color == game.next_step():
                gamelib.draw_oval(
                    c * CELL_SIZE + MARGIN + CELL_SIZE // 4,
                    r * CELL_SIZE + MARGIN + CELL_SIZE // 4,
                    (c + 1) * CELL_SIZE + MARGIN - CELL_SIZE // 4,
                    (r + 1) * CELL_SIZE + MARGIN - CELL_SIZE // 4,
                    fill='black',
                    width=1
                )

    # Display the "divider" lines
    for r in range(height):
        for c in range(width):
            color = game.get_color(r, c)
            if SHOW_NUMBERS:
                gamelib.draw_text(
                    str(color),
                    c * CELL_SIZE + CELL_SIZE // 2 + MARGIN,
                    r * CELL_SIZE + CELL_SIZE // 2 + MARGIN,
                    bold=True,
                    fill='white',
                    anchor='center',
                    size=CELL_SIZE // 2
                )
            if r + 1 < height and game.get_color(r + 1, c) != color:
                gamelib.draw_line(
                    c * CELL_SIZE - LINE_WIDTH / 2 + MARGIN,
                    (r + 1) * CELL_SIZE + MARGIN,
                    (c + 1) * CELL_SIZE + LINE_WIDTH / 2 + MARGIN,
                    (r + 1) * CELL_SIZE + MARGIN,
                    fill='black',
                    width=LINE_WIDTH
                )
            if c + 1 < width and game.get_color(r, c + 1) != color:
                gamelib.draw_line(
                    (c + 1) * CELL_SIZE + MARGIN,
                    r * CELL_SIZE - LINE_WIDTH / 2 + MARGIN,
                    (c + 1) * CELL_SIZE + MARGIN,
                    (r + 1) * CELL_SIZE + LINE_WIDTH / 2 + MARGIN,
                    fill='black',
                    width=LINE_WIDTH
                )

    gamelib.draw_rectangle(
        MARGIN,
        MARGIN,
        width * CELL_SIZE + MARGIN,
        height * CELL_SIZE + MARGIN,
        fill=None,
        width=LINE_WIDTH
    )

def display_controls(game):
    gamelib.draw_rectangle(
        0,
        0,
        WINDOW_WIDTH,
        WINDOW_HEIGHT,
        fill='lightgrey'
    )

    move_color = 'black'
    best_move_count = game.best_move_count
    move_text = f'Moves: {game.move_count} / {best_move_count}'
    if game.move_count > best_move_count:
        move_color = 'red'
        move_text += '  :('
    elif game.is_completed():
        move_color = 'blue'
        move_text += '  :)'

    gamelib.draw_text(
        move_text,
        WINDOW_WIDTH // 3,
        MOVE_HEIGHT,
        anchor='w',
        bold=True,
        fill=move_color
    )

    actions = [
        'Undo (Z)',
        'Redo (X)',
        'New (N)',
        'Solve (S)',
    ]
    for i in range(4):
        gamelib.draw_rectangle(
            MARGIN + (BUTTONS_WIDTH + MARGIN) * (i % 2),
            BUTTONS_HEIGHT + (CELL_SIZE + MARGIN if i >= 2 else 0),
            (BUTTONS_WIDTH + MARGIN) * (i % 2 + 1),
            BUTTONS_HEIGHT + CELL_SIZE + (CELL_SIZE + MARGIN if i >= 2 else 0),
            width=LINE_WIDTH
        )
        gamelib.draw_text(
            actions[i],
            MARGIN + (BUTTONS_WIDTH + MARGIN) * (i % 2) + BUTTONS_WIDTH // 2,
            BUTTONS_HEIGHT + CELL_SIZE // 2 + (CELL_SIZE + MARGIN if i >= 2 else 0),
            fill='black',
            anchor='c',
            bold=True
        )

def main():
    try:
        game = create_game()
    except NotImplementedError:
        gamelib.say('Not all methods in Part 1 are completed')
        return

    gamelib.resize(
        WINDOW_WIDTH,
        WINDOW_HEIGHT
    )

    while gamelib.loop(fps=30):
        gamelib.draw_begin()
        try:
            display_controls(game)
            display_grid(game)
        except NotImplementedError:
            gamelib.say('Not all methods in Part 1 are completed')
            return
        gamelib.draw_end()

        for ev in gamelib.get_events():
            if ev.type == gamelib.EventType.KeyPress:
                if ev.key == 'Escape':
                    return

                if ev.key.lower() == 'z':
                    game.undo()

                if ev.key.lower() == 'x':
                    game.redo()

                if ev.key.lower() == 's':
                    game.calculate_new_solution()

                if ev.key.lower() == 'n':
                    game = create_game()

            if ev.type == gamelib.EventType.ButtonPress:
                x, y = ev.x, ev.y
                game = handle_click(game, x, y)

gamelib.init(main)
