import tkinter as tk
from tkinter import font
from player import Move

# Class for the Tic Tac Toe Board and all related functionalities
class TicTacToeBoard(tk.Tk):
    def __init__(self, game):
        super().__init__()
        self.title("Tic-Tac-Toe Game")
        self._cells = {}
        self._game = game
        self._create_menu()

        # These functions will be initialized in the class initializer
        self._create_board_display()
        self._create_board_grid()

    # To create the board display
    def _create_board_display(self):
        # Create a Frame object to hold the game display
        display_frame = tk.Frame(master=self)

        # the .pack() is the geometry manager to place the frame object onto the main window's top border
        display_frame.pack(fill=tk.X)

        # Create a Label object inside the frame object
        self.display = tk.Label(
            master=display_frame,
            text="Ready?",
            font=font.Font(size=28, weight="bold"),
        )

        # Display label inside the frame using the .pack() geometry manager
        self.display.pack()

    # To create the board grid for the tic tac toe game
    def _create_board_grid(self):
        # Create a Frame object to hold the game's grid of cells
        grid_frame = tk.Frame(master=self)

        # Use the .pack() geometry manager to place the frame object on the main window
        grid_frame.pack()

        # Loop from 0 to 2 represent the row coordinates
        # Can be changed to have the option of using a different grid size, such as 4 by 4
        for row in range(self._game.board_size):
            # Configure width and minimum size of every cell on the grod
            self.rowconfigure(row, weight=1, minsize=50)
            self.columnconfigure(row, weight=1, minsize=75)

            # Loop for the three column coordinates
            for col in range(self._game.board_size):
                # Create a Button object for every cell on the grid
                button = tk.Button(
                    master=grid_frame,
                    text="",
                    font=font.Font(size=36, weight="bold"),
                    fg="black",
                    width=3,
                    height=2,
                    highlightbackground="lightblue",
                )

                # Add every new button to the ._cells dictionary
                self._cells[button] = (row, col)

                # Binds the click event of every button on the game board with the .play() method
                button.bind("<ButtonPress-1>", self.play)

                # Add every button to the main window using the .grid() geometry manager
                button.grid(
                    row=row,
                    column=col,
                    padx=5,
                    pady=5,
                    sticky="nsew"
                )

    # Tkinter event object as an argument
    def play(self, event):
        """Handle a player's move."""
        clicked_btn = event.widget
        row, col = self._cells[clicked_btn]
        move = Move(row, col, self._game.current_player.label)
        if self._game.is_valid_move(move):
            self._update_button(clicked_btn)
            self._game.process_move(move)
            if self._game.is_tied():
                self._update_display(msg="Tied game!", color="red")
            elif self._game.has_winner():
                self._highlight_cells()
                msg = f'Player "{self._game.current_player.label}" won!'
                color = self._game.current_player.color
                self._update_display(msg, color)
            else:
                self._game.toggle_player()
                msg = f"{self._game.current_player.label}'s turn"
                self._update_display(msg)

    def _create_menu(self):
        menu_bar = tk.Menu(master=self)
        self.config(menu=menu_bar)
        file_menu = tk.Menu(master=menu_bar)
        file_menu.add_command(
            label="Play Again",
            command=self.reset_board
        )
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=quit)
        menu_bar.add_cascade(label="File", menu=file_menu)

    def _update_button(self, clicked_btn):
        clicked_btn.config(text=self._game.current_player.label)
        clicked_btn.config(fg=self._game.current_player.color)

    def _update_display(self, msg, color="black"):
        self.display["text"] = msg
        self.display["fg"] = color

    def _highlight_cells(self):
        for button, coordinates in self._cells.items():
            if coordinates in self._game.winner_combo:
                button.config(highlightbackground="red")

    def reset_board(self):
        """Reset the game's board to play again."""
        self._game.reset_game()
        self._update_display(msg="Ready?")
        for button in self._cells.keys():
            button.config(highlightbackground="lightblue")
            button.config(text="")
            button.config(fg="black")