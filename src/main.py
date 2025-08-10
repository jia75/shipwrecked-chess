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

    def on_open(self) -> None:
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
