import badge
import utime

class App(badge.BaseApp):
    def __init__(self) -> None:
        self.grid = [[-1, -1, -1, 34, 32, 33, 36, 35, 33, 32, 34, -1, -1, -1], 
                     [-1, -1, -1, 31, 31, 31, 31, 31, 31, 31, 31, -1, -1, -1], 
                     [-1, -1, -1, 0, 0, 0, 0, 0, 0, 0, 0, -1, -1, -1], 
                     [24, 21, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 31, 34], 
                     [22, 21, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 31, 32], 
                     [23, 21, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 31, 33], 
                     [26, 21, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 31, 35], 
                     [25, 21, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 31, 36], 
                     [23, 21, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 31, 33], 
                     [22, 21, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 31, 32], 
                     [24, 21, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 31, 34], 
                     [-1, -1, -1, 0, 0, 0, 0, 0, 0, 0, 0, -1, -1, -1],
                     [-1, -1, -1, 11, 11, 11, 11, 11, 11, 11, 11, -1, -1, -1],
                     [-1, -1, -1, 14, 12, 13, 15, 16, 13, 12, 14, -1, -1, -1]]
        self.num = 1
        self.pos = [3, 13]
        self.selected = [-1, -1]

    def handle_move(self, move) -> None:
        if self.grid[move[1][1]][move[1][0]] == -1 or self.grid[move[1][1]][move[1][0]] // 10 == self.num:
            return
        if self.grid[move[0][1]][move[0][0]] % 10 == 1:
            if self.move[1][0] == self.move[0][0] - 1:
                if self.move[1][1] == self.move[0][1] and self.grid[self.move[1][1]][self.move[1][0]] == 0:
                    self.grid[self.move[1][1]][self.move[1][0]] = self.num * 10 + 1
                    self.grid[self.move[0][1]][self.move[0][0]] = 0
                elif (self.move[1][1] == self.move[0][1] - 1 or self.move[1][1] == self.move[0][1] + 1) and self.grid[self.move[1][1]][self.move[1][0]] > 0:
                    self.grid[self.move[1][1]][self.move[1][0]] = self.num * 10 + 1
                    self.grid[self.move[0][1]][self.move[0][0]] = 0
        elif self.grid[move[0][1]][move[0][0]] % 10 == 2:
            pass
        elif self.grid[move[0][1]][move[0][0]] % 10 == 3:
            pass
        elif self.grid[move[0][1]][move[0][0]] % 10 == 4:
            pass
        elif self.grid[move[0][1]][move[0][0]] % 10 == 5:
            pass
        elif self.grid[move[0][1]][move[0][0]] % 10 == 6:
            pass

    def on_open(self) -> None:
        self.isHost = False
        self.players = []
        self.state = "Home" # Home, Game, Lobby

    def loop(self) -> None:
        if self.turn != 1:
            return
        if badge.input.get_button(badge.input.Buttons.SW8):
            self.pos[1] = self.pos[1] - 1 if self.pos[1] > 0 else 13
        if badge.input.get_button(badge.input.Buttons.SW4):
            self.pos[1] = self.pos[1] + 1 if self.pos[1] < 13 else 0
        if badge.input.get_button(badge.input.Buttons.SW18):
            self.pos[0] = self.pos[0] - 1 if self.pos[0] > 0 else 13
        if badge.input.get_button(badge.input.Buttons.SW13):
            self.pos[0] = self.pos[0] + 1 if self.pos[0] < 13 else 0
        if badge.input.get_button(badge.input.Buttons.SW5):
            if self.selected == self.pos:
                self.selected = [-1, -1]
            elif self.selected == [-1, -1] and self.grid[self.pos[1]][self.pos[0]] > 0:
                self.selected = self.pos
            else:
                self.handle_move([self.selected, self.pos])

    def create_lobby(self) -> None:
        self.isHost = True
        self.players = [badge.contacts.my_contact()]
        self.state = "Lobby"

    def join_lobby(self, hostId) -> None:
        if self.isHost:
            raise RuntimeError("Cannot join lobby as host")
        badge.radio.send_packet(hostId, "join_request".encode('utf-8'))
        self.state = "Lobby"
        
    def on_packet(self, packet, is_foreground):
        if (self.isHost and packet.data == "join_request".encode('utf-8')):
            new_player = packet.source
            if new_player not in self.players:
                self.players.append(new_player)
                badge.radio.send_packet(new_player, "join_accepted".encode('utf-8'))
                badge.display.show_text(f"Player {new_player} joined")
                for player in self.players.remove(new_player):
                    badge.radio.send_packet(player, f"player_joined:{new_player}".encode('utf-8'))
            else:
                badge.display.show_text(f"Player {new_player} already in lobby")
        elif (not self.isHost and packet.data == "join_accepted".encode('utf-8')):
            badge.display.show_text("Joined lobby")
            self.players.append(packet.source)
            self.state = "Lobby"
        elif packet.data.startswith(b"player_joined:"):
            new_player = packet.data.decode('utf-8').split(":")[1]
            if new_player not in self.players:
                self.players.append(new_player)
                badge.display.show_text(f"New player joined: {new_player}")
