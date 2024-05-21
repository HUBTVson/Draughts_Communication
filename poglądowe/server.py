import socket
import threading
import json
import signal
from poglądowe.game import Game

class CheckersServer:
    def __init__(self, host='localhost', port=5555):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen(2)
        print(f"Server started on {host}:{port}")
        self.clients = []
        self.game = Game()
        signal.signal(signal.SIGINT, self.shutdown)
        self.lock = threading.Lock()

    def handle_client(self, client_socket, player_id):
        while True:
            try:
                message = client_socket.recv(1024).decode()
                if message:
                    with self.lock:
                        if self.game.elements['board'].current_turn == player_id:
                            self.process_move(client_socket, message, player_id)
            except:
                self.clients.remove((client_socket, player_id))
                client_socket.close()
                break

    def process_move(self, client_socket, message, player_id):
        move = json.loads(message)
        success, status_message = self.game.process_move(move, player_id)
        if success:
            self.broadcast_game_state()
            self.notify_next_player()
        else:
            client_socket.send(json.dumps({"status": status_message}).encode())

    def broadcast_game_state(self):
        game_state = json.dumps(self.game.get_game_state())
        for client, _ in self.clients:
            client.send(game_state.encode())

    def notify_next_player(self):
        current_turn = self.game.elements['board'].current_turn
        for client, player_id in self.clients:
            if player_id == current_turn:
                client.send(json.dumps({"status": "Your turn"}).encode())

    def start(self):
        while len(self.clients) < 2:
            client_socket, addr = self.server.accept()
            player_id = 'player1' if len(self.clients) == 0 else 'player2'
            self.clients.append((client_socket, player_id))
            print(f"{player_id} connected from {addr}")
            threading.Thread(target=self.handle_client, args=(client_socket, player_id)).start()
        
        self.notify_next_player()

    def shutdown(self, signum, frame):
        print("\nShutting down server...")
        for client, _ in self.clients:
            client.close()
        self.server.close()
        exit()

if __name__ == "__main__":
    server = CheckersServer()
    server.start()
