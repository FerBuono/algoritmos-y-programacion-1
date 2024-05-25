from game.flood import Flood
from libs.stack import Stack
from libs.queue import Queue

class FloodGame:
    """Class to manage a Flood, along with its states and actions."""

    def __init__(self, height, width, n_colors):
        """Generates a new FloodGame, which has a Flood and other
        attributes to perform various game actions.

        Arguments:
            height, width (int): Size of the Flood grid.
            n_colors: Maximum number of colors to include in the grid.
        """
        self.flood = Flood(height, width)
        self.flood.shuffle_board(n_colors)
        self.best_move_count, _ = self._calculate_moves()
        self.move_count = 0
        self.solution_steps = Queue()
        self.undo_states = Stack()
        self.redo_states = Stack()

    def change_color(self, color):
        """Performs the action to select a color in the Flood, incrementing
        the number of moves made and managing the undo and redo structures.

        Arguments:
            color (int): New color to select
        """
        clone = self.flood.clone()
        self.undo_states.push(clone.board)

        self.move_count += 1
        self.flood.change_color(color)

        if not self.redo_states.is_empty():
            self.redo_states = Stack()

        if not self.solution_steps.is_empty() and self.solution_steps.peek() == color:
            self.solution_steps.dequeue()
        else:
            self.solution_steps = Queue()

    def undo(self):
        """Undoes the last move if there are previous steps,
        managing the undo and redo structures.
        """
        if self.undo_states.is_empty():
            return
        
        clone = self.flood.clone()
        self.redo_states.push(clone.board)

        self.flood.board = self.undo_states.pop()

        self.move_count -= 1
        self.solution_steps = Queue()

    def redo(self):
        """Redoes the undone move if it exists, managing the
        undo and redo structures.
        """
        if self.redo_states.is_empty():
            return

        clone = self.flood.clone()
        self.undo_states.push(clone.board)
        
        self.flood.board = self.redo_states.pop()

        self.move_count += 1
        self.solution_steps = Queue()

    def _calculate_moves(self):
        """Finds a solution of steps for the current Flood (in a Queue)
        and returns the number of moves taken to reach that solution.
        
        Heuristic: at each step, select the color that adds the most cells
        to the current Flood.

        To find this sequence of steps, first create a copy of the current Flood
        on which to perform tests. Then create a "test" copy to count the number
        of cells the new Flood would have if we selected the other available colors
        (excluding the current one). Finally, select the color that would add the
        most cells to the main block.

        Returns:
            int: Number of moves to reach the found solution.
            Queue: Steps used to reach that solution.
        """
        steps = Queue()
        moves = 0
        clone = self.flood.clone()
        while not clone.is_completed():
            possible_colors = {}
            other_colors = list(filter(lambda x: x != clone.board[0][0], clone.get_possible_colors()))

            for color in other_colors:
                test_clone = clone.clone()
                test_clone.change_color(color)
                possible_colors[color] = test_clone.main_block_cells()

            next_color = max(possible_colors, key=possible_colors.get)
            steps.enqueue(next_color)
            moves += 1
            clone.change_color(next_color)

        return moves, steps

    def has_next_step(self):
        """Returns a boolean indicating if there is a calculated solution."""
        return not self.solution_steps.is_empty()

    def next_step(self):
        """If there is a calculated solution, returns the next step.
        Otherwise, raises ValueError.

        Returns:
            Color of the next step in the solution.
        """
        return self.solution_steps.peek()

    def calculate_new_solution(self):
        """Calculates a sequence of steps that solve the current state
        of the flood, so that the `next_step()` method can be called.
        """
        _, self.solution_steps = self._calculate_moves()

    def dimensions(self):
        return self.flood.dimensions()

    def get_color(self, row, col):
        return self.flood.get_color(row, col)

    def get_possible_colors(self):
        return self.flood.get_possible_colors()

    def is_completed(self):
        return self.flood.is_completed()
