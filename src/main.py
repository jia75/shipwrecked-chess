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
        self.isHost = False
        self.players = []
        self.state = "Home" # Home, Game, Lobby

    def loop(self) -> None:
        pass

    def create_lobby(self) -> None:
        self.isHost = True
        self.players = [badge.contacts.my_contact()]
        self.state = "Lobby"

    def join_lobby(self, hostId) -> None:
        # 1321
        if self.isHost:
            raise RuntimeError("Cannot join lobby as host")
        badge.radio.send_packet(hostId, "join_request".encode('utf-8'))
        self.state = "Lobby"
        
    def handle_move(self, player, move):
        pass
    
    def send_move(self, move):
        if self.state != "Game":
            raise RuntimeError("Cannot send move, not in game state")
        for player in self.players:
            badge.radio.send_packet(player, f"move:{move}".encode('utf-8'))

    def on_packet(self, packet, is_foreground):
        if (self.isHost and packet.data == "join_request".encode('utf-8')):
            new_player = packet.source
            if new_player not in self.players:
                self.players.append(new_player)
                badge.radio.send_packet(new_player, f"join_accepted:{','.join(self.players)}".encode('utf-8'))
                badge.display.show_text(f"Player {new_player} joined")
                for player in self.players.remove(new_player):
                    badge.radio.send_packet(player, f"player_joined:{new_player}".encode('utf-8'))
            else:
                pass
        elif (not self.isHost and packet.data == "join_accepted".encode('utf-8')):
            badge.display.show_text("Joined lobby")
            self.players.append(packet.source)
            self.state = "Lobby"
        elif packet.data.startswith(b"player_joined:"):
            new_player = packet.data.decode('utf-8').split(":")[1]
            if new_player not in self.players:
                self.players.append(new_player)
        elif packet.data.startswith(b"join_accepted:"):
            players_list = packet.data.decode('utf-8').split(":")[1]
            self.players = players_list.split(",")
        elif packet.data.startswith(b"move:"):
            move = packet.data.decode('utf-8').split(":")[1]
            self.handle_move(packet.source, move)