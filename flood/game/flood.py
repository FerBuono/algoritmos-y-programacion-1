import random

COLORS = {
    0: '#FF0000',
    1: '#33DD33',
    2: '#334DFF',
    3: '#8000B3',
    4: '#FF8000',
    5: '#DA2071',
    6: '#EEEE00',
    7: '#C0C0C0',
    8: '#808080',
    9: '#0C0C0C'
}
MAIN_BLOCK = 'block'

class Flood:
    """Class to manage a board of N colors."""

    def __init__(self, height, width):
        """Generates a new Flood with a single color of the given dimensions.

        Arguments:
            height, width (int): Size of the grid.
        """
        self.rows = height
        self.columns = width
        self.initial_color = random.randint(0, 9)
        self.colors = []
        self.board = [[self.initial_color for j in range(width)] for i in range(height)]

    def shuffle_board(self, n_colors):
        """Randomly assigns up to `n_colors` throughout the board's cells.

        Arguments:
            n_colors (int): Maximum number of colors to include in the grid.
        """
        self.colors = [self.initial_color] + random.sample(list(filter(lambda x: x != self.initial_color, COLORS)), n_colors - 1)
        self.board = [[random.choice(self.colors) for col in range(len(self.board[0]))] for row in range(len(self.board))]

    def get_color(self, row, col):
        """Returns the color at the specified coordinates.

        Arguments:
            row, col (int): Positions of the row and column in the grid.

        Returns:
            Assigned color.
        """
        return self.board[row][col]

    def get_possible_colors(self):
        """Returns a sorted sequence of all possible game colors.
        The sequence will include all colors used to generate the board,
        regardless of how many of these colors currently remain on the board.

        Returns:
            iterable: sorted sequence of colors.
        """
        return sorted(self.colors)

    def dimensions(self):
        """Grid dimensions (rows and columns)

        Returns:
            (int, int): height and width of the grid in that order.
        """
        return (self.rows, self.columns)

    def _change_color(self, new_color, old_color, r=0, c=0):
        """Recursively checks if the neighbors of the cell at board[r][c]
        (starting from r = 0 and c = 0) are of the main block color and
        changes them to the new color.
        """
        if r < 0 or r >= self.rows or c < 0 or c >= self.columns:
            return
        if self.board[r][c] != old_color:
            return
        
        self.board[r][c] = new_color

        self._change_color(new_color, old_color, r, c + 1)
        self._change_color(new_color, old_color, r, c - 1)
        self._change_color(new_color, old_color, r + 1, c)
        self._change_color(new_color, old_color, r - 1, c)

    def change_color(self, new_color):
        """Assigns the new color to the Flood of the grid. That is,
        all coordinates forming a continuous path of the same color
        starting from the origin coordinate (0, 0) will be assigned `new_color`.

        Arguments:
            new_color: New color value to assign to the Flood.
        """
        old_color = self.board[0][0]

        if self.is_completed() or old_color == new_color:
            return
            
        self._change_color(new_color, old_color)

    def clone(self):
        """Returns:
            Flood: Copy of the current Flood
        """
        new = Flood(self.rows, self.columns)
        new.initial_color = self.initial_color
        new.colors = self.colors
        new.board = [[num for num in row] for row in self.board]
        return new

    def _main_block_cells(self, color, clone, r=0, c=0):
        """Recursively checks if the cell board[r][c] belongs
        to the main block and changes its value to 'block' to identify it.
        """
        count = 0

        if r < 0 or r >= clone.rows or c < 0 or c >= clone.columns:
            return 0
        if clone.board[r][c] != color:
            return 0

        clone.board[r][c] = MAIN_BLOCK
        count += 1

        count += clone._main_block_cells(color, clone, r, c + 1)
        count += clone._main_block_cells(color, clone, r, c - 1)
        count += clone._main_block_cells(color, clone, r + 1, c)
        count += clone._main_block_cells(color, clone, r - 1, c)

        return count

    def main_block_cells(self):
        """The number of cells occupied by the main block.

        Returns:
            int: size of the main block
        """
        clone = self.clone()
        color = clone.board[0][0]
        return self._main_block_cells(color, clone)

    def is_completed(self):
        """Indicates if all grid coordinates have the same color.

        Returns:
            bool: True if the entire grid has the same color
        """
        current_color = self.board[0][0]
        for row in self.board:
            for num in row:
                if num != current_color:
                    return False
        return True
