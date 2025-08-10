import badge
import utime

""" 
-1 Forbidden
0 Empty

11 Team 1 Pawn
12 Team 1 Knight
13 Team 1 Bishop
14 Team 1 Rook
15 Team 1 Queen
16 Team 1 King
21 ...
...
"""

def draw_square_to_buffer(x: int, y: int, piece: int) -> None:
    if not piece == -1:
        badge.display.rect(x, y, 15, 15, 0)
        return
    if piece == 0:
        return
    badge.display.nice_text(str(piece%10), x+1,y+1, rot = (piece/10-1)*90)

def move_board_to_buffer(board: List[List[int]], player_number: int) -> None:
    for row_index in range(14):
        for column_index in range(14):
            draw_square_to_buffer(row_index*14, column_index*14, board[row_index][column_index])


class App(badge.BaseApp):
    def on_open(self) -> None:
        example_board = [[0]*14 for _ in range(14)]
        example_board[3][6] = -1
        badge.display.fill(1)
        move_board_to_buffer(example_board, 1)
        badge.display.show()
    def loop(self) -> None:
        pass

