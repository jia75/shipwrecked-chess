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

class App(badge.BaseApp):
    def __init__(self) -> None:
        self.grid = [[-1, -1, -1, 34, 32, 33, 36, 35, 33, 32, 34, -1, -1, -1], 
                     [-1, -1, -1, 31, 31, 31, 31, 31, 31, 31, 31, -1, -1, -1], 
                     [-1, -1, -1, 0, 0, 0, 0, 0, 0, 0, 0, -1, -1, -1], 
                     [24, 21, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 41, 44], 
                     [22, 21, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 41, 42], 
                     [23, 21, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 41, 43], 
                     [26, 21, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 41, 45], 
                     [25, 21, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 41, 46], 
                     [23, 21, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 41, 43], 
                     [22, 21, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 41, 42], 
                     [24, 21, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 41, 44], 
                     [-1, -1, -1, 0, 0, 0, 0, 0, 0, 0, 0, -1, -1, -1],
                     [-1, -1, -1, 11, 11, 11, 11, 11, 11, 11, 11, -1, -1, -1],
                     [-1, -1, -1, 14, 12, 13, 15, 16, 13, 12, 14, -1, -1, -1]]
        self.num = 1
        self.pos = [3, 13]
        self.oldPos = [3, 13]
        self.selected = [-1, -1]
        self.last_player_size = 0
        self.state = "Home" # Home, Game, Lobby, NoBadge

    def rotated_fill_aid(self, x, y, x_off, y_off, w, h, color, rot):
        if rot == 0:
            badge.display.fill_rect(x+x_off, y+y_off, w, h, color)
        elif rot == 90:
            badge.display.fill_rect(x-y_off-h, y+x_off, h, w, color)
        elif rot == 180:
            badge.display.fill_rect(x-x_off-w, y-y_off-h, w, h, color)
        elif rot == 270:
            badge.display.fill_rect(x+y_off, y-x_off-w, h, w, color)
            

    def display_symbol(self, letter: str, x: int, y: int, rot: int):
        if letter == "P":
            self.rotated_fill_aid(x, y, 2, 4, 8, 4, 0, rot)
            self.rotated_fill_aid(x, y, 4, 8, 4, 2, 0, rot)
            self.rotated_fill_aid(x, y, 0, 10, 12, 2, 0, rot)
        elif letter == "N":
            self.rotated_fill_aid(x, y, 2, 0, 8, 4, 0, rot)
            self.rotated_fill_aid(x, y, 0, 2, 4, 4, 0, rot)
            self.rotated_fill_aid(x, y, 6, 2, 6, 6, 0, rot)
            self.rotated_fill_aid(x, y, 2, 8, 10, 4, 0, rot)
            self.rotated_fill_aid(x, y, 0, 10, 12, 2, 0, rot)
        elif letter == "B":
            self.rotated_fill_aid(x, y, 4, 0, 4, 12, 0, rot)
            self.rotated_fill_aid(x, y, 2, 2, 8, 4, 0, rot)
            self.rotated_fill_aid(x, y, 2, 8, 8, 4, 0, rot)
            self.rotated_fill_aid(x, y, 0, 10, 12, 2, 0, rot)
            self.rotated_fill_aid(x, y, 4, 2, 2, 2, 1, rot)
            self.rotated_fill_aid(x, y, 6, 4, 2, 2, 1, rot)
        elif letter == "R":
            self.rotated_fill_aid(x, y, 0, 0, 12, 4, 0, rot)
            self.rotated_fill_aid(x, y, 2, 2, 8, 8, 0, rot)
            self.rotated_fill_aid(x, y, 0, 10, 12, 2, 0, rot)
            self.rotated_fill_aid(x, y, 2, 0, 2, 2, 1, rot)
            self.rotated_fill_aid(x, y, 6, 0, 2, 2, 1, rot)
        elif letter == "Q":
            self.rotated_fill_aid(x, y, 4, 0, 4, 12, 0, rot)
            self.rotated_fill_aid(x, y, 2, 8, 8, 2, 0, rot)
            self.rotated_fill_aid(x, y, 0, 2, 2, 6, 0, rot)
            self.rotated_fill_aid(x, y, 10, 2, 2, 6, 0, rot)
            self.rotated_fill_aid(x, y, 0, 10, 12, 2, 0, rot)
        elif letter == "K":
            self.rotated_fill_aid(x, y, 4, 4, 4, 4, 0, rot)
            self.rotated_fill_aid(x, y, 2, 8, 8, 2, 0, rot)
            self.rotated_fill_aid(x, y, 0, 4, 2, 4, 0, rot)
            self.rotated_fill_aid(x, y, 10, 4, 2, 4, 0, rot)
            self.rotated_fill_aid(x, y, 2, 2, 2, 2, 0, rot)
            self.rotated_fill_aid(x, y, 8, 2, 2, 2, 0, rot)
            self.rotated_fill_aid(x, y, 0, 10, 12, 2, 0, rot)

    def draw_square_to_buffer(self, x: int, y: int, piece: int) -> None:
        if piece == -1:
            return
        badge.display.rect(x, y, 15, 15, 0)
        if piece == 0:
            return
        piece_mappings = {
            1: "P",
            2: "N",
            3: "B",
            4: "R",
            5: "Q",
            6: "K",
        }
        ptype = piece % 10
        letter = piece_mappings.get(ptype, "?")
        if piece//10 == 1:
            self.display_symbol(letter, x+2, y, 0)
        elif piece//10 == 2:
            self.display_symbol(letter, x+16, y+2, 90)
        elif piece//10 == 3:
            self.display_symbol(letter, x+14, y+14, 180)
        elif piece//10 == 4:
            self.display_symbol(letter, x, y+14, 270)

    def move_board_to_buffer(self, board: List[List[int]], player_number: int) -> None:
        for column_index in range(14):
            for row_index in range(14):
                self.draw_square_to_buffer(row_index*14, column_index*14, board[column_index][row_index])

    def draw_hover(self, x, y, old_x, old_y) -> None:
        badge.display.rect(old_x*14+1, old_y*14+1, 13, 13, 1)
        badge.display.rect(x*14+1, y*14+1, 13, 13, 0)
        self.move_board_to_buffer(self.grid, 1)
        badge.display.show()

    def draw_selection(self, x, y) -> None:
        badge.display.fill_rect(x*14+1, y*14+1, 13, 13, 0)
        self.move_board_to_buffer(self.grid, 1)
        badge.display.show()

    def erase_selection(self, x, y) -> None:
        badge.display.fill_rect(x*14+1, y*14+1, 13, 13, 1)
        self.move_board_to_buffer(self.grid, 1)
        badge.display.show()

    def create_lobby(self) -> None:
        print("Creating lobby")
        self.is_host = True
        self.players = [badge.contacts.my_contact().badge_id] # Badge ID for now, as when queuing, we only get the ID
        self.state = "Lobby"
        self.connected_to_lobby = True

        self.display_lobby()
        badge.display.show()

    def join_lobby(self) -> None:
        # 4023
        if self.is_host:
            raise RuntimeError("Cannot join lobby as host")
        badge.radio.send_packet(0xffff, "join_request".encode('utf-8'))
        self.state = "Lobby"

        self.display_lobby()
        badge.display.show()

    def start_game(self) -> None:
        if self.is_host:
            if len(self.players) < 2:
                raise RuntimeError("Not enough players to start game")
            temp_players = self.players.copy()
            temp_players.remove(badge.contacts.my_contact().badge_id)
            for player in temp_players:
                utime.sleep(1.5)
                badge.radio.send_packet(player, f"game_start:{self.players.index(player)+1}".encode('utf-8'))
        self.state = "Game"
        badge.display.fill(1)
        self.move_board_to_buffer(self.grid, self.num)
        self.draw_hover(self.pos[0], self.pos[1], self.oldPos[0], self.oldPos[1])
        
    def handle_move(self, move) -> None:
        sx, sy = move[0]
        tx, ty = move[1]

        self.grid[ty][tx] = self.grid[sy][sx]
        self.grid[sy][sx] = 0

        badge.display.fill(1)
        self.move_board_to_buffer(self.grid, self.num)
        badge.display.show()
    
    def send_move(self, move):
        if self.state != "Game":
            raise RuntimeError("Cannot send move, not in game state")
        for player in self.players:
            utime.sleep(1.5)
            badge.radio.send_packet(player, f"move:{move}".encode('utf-8'))

    def on_packet(self, packet, is_foreground):
        data_str = packet.data.decode('utf-8')
        if data_str == "join_request": # received by host
            if self.state == "Lobby" and self.is_host and len(self.players)+self.unsure_players < 4:
                badge.radio.send_packet(packet.source, f"join_accepted".encode('utf-8'))
                self.unsure_players += 1
        elif data_str == "join_accepted" and not self.is_host and not self.connected_to_lobby: # received by guest
            if self.state == "Lobby":
                utime.sleep(1.5)
                badge.radio.send_packet(packet.source, f"join_confirmed".encode('utf-8'))
                self.connected_to_lobby = True

                self.display_lobby()
                badge.display.show()
            else:
                utime.sleep(1.5)
                badge.radio.send_packet(packet.source, f"join_canceled".encode('utf-8'))
        elif data_str == "join_confirmed" and self.is_host: # received by host
            if self.state == "Lobby":
                # print([0][3])
                self.unsure_players -= 1
                self.players.append(packet.source)
                self.display_lobby()
                badge.display.show()
                for player in players:
                    if player == badge.contacts.my_contact().badge_id:
                        continue
                    utime.sleep(1.5)
                    badge.radio.send_packet(player, f"player_joined:{str(packet.source)}".encode('utf-8')) # tell everyone there's a new player
                if (len(self.players) >= 4):
                    self.state = "Game"
                    self.num = 1
                    badge.display.fill(1)
                    self.move_board_to_buffer(self.grid, self.num)
                    self.draw_hover(self.pos[0], self.pos[1], self.oldPos[0], self.oldPos[1])
                    badge.display.show()
                    for player in self.players:
                        utime.sleep(1.5)
                        badge.radio.send_packet(player, f"game_start:{self.players.index(player)+1}".encode('utf-8'))
        elif data_str.startswith("game_start:") and not self.is_host: # received by guests
            if self.state == "Lobby" and not self.is_host:
                self.start_game()
        elif data_str == "join_canceled" and self.is_host:
            self.players.remove(packet.source)
            self.unsure_players -= 1
        elif data_str.startswith("player_joined:"): # received by guests already in lobby
            new_player = int(data_str.split(":")[1])
            if new_player not in self.players:
                self.players.append(new_player)
            self.display_lobby()
            badge.display.show()
        elif data_str.startswith("move:"):
            try:
                move_data = data_str.split(":", 1)[1]
                move = eval(move_data)
                self.handle_move(move)
            except ValueError as e:
                raise RuntimeError(f"Invalid move data received: {e}")
    
    def display_home(self) -> None:
        if self.state != "Home":
            raise RuntimeError("Can't display home; not in home state")
        badge.display.fill(1)
        badge.display.nice_text("QuadChess", 0, 0, font=32)
        badge.display.text("<- Create lobby", 0, 88)
        badge.display.text("<- Join lobby", 0, 178)

    def display_lobby(self) -> None:
        if self.state != "Lobby":
            raise RuntimeError("Can't display lobby; not in lobby state")
        badge.display.fill(1)
        badge.display.text("QuadChess", 0, 0)
        player_count = len(self.players)
        badge.display.text("Lobby (" + str(player_count) + "/4)", 0, 88)
        if (self.is_host):
            badge.display.text("<- Start game override", 0, 178)
        for i in range(player_count):
            badge.display.text(str(self.players[i]), 0, 108+i*20)


    def display_no_badge(self) -> None:
        badge.display.fill(1)
        badge.display.text("Dawg you don't have a badge id", 0, 0)
        badge.display.text("Don't wipe out your config", 0, 88)
        def display_shrug(self) -> None:
            shrug = r"""
            ¯\_()_/¯
            """
            badge.display.fill(1)
            badge.display.nice_text(shrug, 0, 0, font=32)
            badge.display.show()

    def on_open(self) -> None:
        self.is_host = False
        try:
            badgeId = badge.contacts.my_contact().badge_id
        except Exception as e:
            self.state = "NoBadge"
            return
        self.players = []
        self.state = "Home" # Home, Game, Lobby, NoBadge
        self.last_player_size = 0
        self.connected_to_lobby = False
        self.unsure_players = 0

        self.display_home()
        badge.display.show()

        # badge.display.fill(1)
        # self.move_board_to_buffer(self.grid, self.num)
        # self.draw_hover(self.pos[0], self.pos[1], self.oldPos[0], self.oldPos[1])

    def loop(self) -> None:
        if self.state == "NoBadge":
            self.display_no_badge()
        elif self.state == "Home":
            if badge.input.get_button(badge.input.Buttons.SW10):
                self.join_lobby()
            elif badge.input.get_button(badge.input.Buttons.SW18):
                self.create_lobby()
        elif self.state == "Game":
            if badge.input.get_button(badge.input.Buttons.SW8):
                self.pos[1] = self.pos[1] - 1 if self.pos[1] > 0 else 13
                self.move_board_to_buffer(self.grid, self.num)
                self.draw_hover(self.pos[0], self.pos[1], self.oldPos[0], self.oldPos[1])
                self.oldPos = self.pos.copy()
            if badge.input.get_button(badge.input.Buttons.SW4):
                self.pos[1] = self.pos[1] + 1 if self.pos[1] < 13 else 0
                self.move_board_to_buffer(self.grid, self.num)
                self.draw_hover(self.pos[0], self.pos[1], self.oldPos[0], self.oldPos[1])
                self.oldPos = self.pos.copy()
            if badge.input.get_button(badge.input.Buttons.SW18):
                self.pos[0] = self.pos[0] - 1 if self.pos[0] > 0 else 13
                self.move_board_to_buffer(self.grid, self.num)
                self.draw_hover(self.pos[0], self.pos[1], self.oldPos[0], self.oldPos[1])
                self.oldPos = self.pos.copy()
            if badge.input.get_button(badge.input.Buttons.SW13):
                self.pos[0] = self.pos[0] + 1 if self.pos[0] < 13 else 0
                self.move_board_to_buffer(self.grid, self.num)
                self.draw_hover(self.pos[0], self.pos[1], self.oldPos[0], self.oldPos[1])
                self.oldPos = self.pos.copy()
            if badge.input.get_button(badge.input.Buttons.SW5):
                if self.selected == self.pos:
                    self.erase_selection(self.selected[0], self.selected[1])
                    self.selected = [-1, -1]
                elif self.selected == [-1, -1] and self.grid[self.pos[1]][self.pos[0]] > 0:
                    self.selected = self.pos.copy()
                    self.draw_selection(self.selected[0], self.selected[1])
                else:
                    self.handle_move([self.selected, self.pos])
                    self.erase_selection(self.selected[0], self.selected[1])
                    self.handle_move([self.selected, self.pos])
                    self.send_move([self.selected, self.pos])
                    self.selected = [-1, -1]
        
        elif self.state == "Lobby":
            if badge.input.get_button(badge.input.Buttons.SW10):
                if (self.is_host):
                    self.start_game()
