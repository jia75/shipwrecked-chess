import badge
import utime

class App(badge.BaseApp):
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