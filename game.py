from player import Move
from itertools import cycle
from game_setup import DEFAULT_PLAYERS, BOARD_SIZE


class TicTacToeGame:
    def __init__(self, players=DEFAULT_PLAYERS, board_size=BOARD_SIZE):
        # Cyclical iterator over the input tuple of players
        self._players = cycle(players)

        # The board size defined by BOARD_SIZE variable
        self.board_size = board_size

        # The current active player
        self.current_player = next(self._players)

        # How to determine the winner based on cells
        self.winner_combo = []

        # List of players' moves in the game
        self._current_moves = []

        # Boolean value to determine winner state
        self._has_winner = False

        # List of cell combinations to define the win conditions
        self._winning_combos = []

        # Method to set up the board
        self._setup_board()

    # List comprehension to provide an initial list of values for ._current_moves
    # Creates the list of lists that contains empty Move objects.
    def _setup_board(self):
        self._current_moves = [
            [Move(row, col) for col in range(self.board_size)]
            for row in range(self.board_size)
        ]
        # Method call to assign its return value to ._winning_combos
        self._winning_combos = self._get_winning_combos()

    # Get the winning combos based on rows, columns, and diagonals
    def _get_winning_combos(self):
        rows = [
            [(move.row, move.col) for move in row]
            for row in self._current_moves
        ]
        columns = [list(col) for col in zip(*rows)]
        first_diagonal = [row[i] for i, row in enumerate(rows)]
        second_diagonal = [col[j] for j, col in enumerate(reversed(columns))]
        return rows + columns + [first_diagonal, second_diagonal]

    # Check if it is a valid move or not
    def is_valid_move(self, move):
        """Return True if move is valid, and False otherwise"""
        # row and col coordinates for the imput move
        row, col = move.row, move.col

        # Check if the move has an empty string label.
        # Condition will be True if no player has made the input move before
        move_was_not_played = self._current_moves[row][col].label == ""

        # Check if the game does not have a winner yet
        no_winner = not self._has_winner

        # Return the value of winner and if move was not played
        return no_winner and move_was_not_played

    # process the Move object as an argument
    def process_move(self, move):
        """Process the current move and check if it's a win."""
        # Get the row and col coordinates from the move input
        row, col = move.row, move.col

        # Assign the input coordinates for the move
        self._current_moves[row][col] = move

        # Loop for winning combinations
        # Generator expression taht retreives all the labels from the moves in the current winning combination
        # Converted to set object
        for combo in self._winning_combos:
            results = set(
                self._current_moves[n][m].label
                for n, m in combo
            )

            # Boolean expression determining the win is not
            is_win = (len(results) == 1) and ("" not in results)

            # Checks if the is_win condition is True and then breaks
            if is_win:
                self._has_winner = True
                self.winner_combo = combo
                break

    def has_winner(self):
        """Return True if the game has a winner, and False otherwise."""
        return self._has_winner

    def is_tied(self):
        """Return True if the game is tied, and False otherwise."""
        no_winner = not self._has_winner
        played_moves = (
            move.label for row in self._current_moves for move in row
        )
        return no_winner and all(played_moves)

    def toggle_player(self):
        """Returned a toggled player."""
        self.current_player = next(self._players)

    def reset_game(self):
        """Reset the game state to play again."""
        for row, row_content in enumerate(self._current_moves):
            for col, _ in enumerate(row_content):
                row_content[col] = Move(row, col)
        self._has_winner = False
        self.winner_combo = []
