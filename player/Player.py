from typing import NamedTuple


# Define the Player Class
# .label attribute for X and O signs
# .color attribute for Tkinter color for identifying the target player on teh game board
class Player(NamedTuple):
    label: str
    color: str
