from typing import NamedTuple


# Define the Move class
# .row and .col attributes hold the coordinates of the move's target cell
# .label attribute hold the sign that identifies the player, X or O. Defaults to empty string, no play has done yet
class Move(NamedTuple):
    row: int
    col: int
    label: str = ""
