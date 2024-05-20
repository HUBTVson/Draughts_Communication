import socket
import threading
import json
import signal

class CheckersServer:
    def __init__(self, host='localhost', port=5555):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen(2)
        print(f"Server started on {host}:{port}")
        self.clients = []
        self.game_state = self.initialize_game()
        signal.signal(signal.SIGINT, self.shutdown)
        self.lock = threading.Lock()

    def initialize_game(self):
        board = [
            [0, 1, 0, 1, 0, 1, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 0],
            [0, 1, 0, 1, 0, 1, 0, 1],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [2, 0, 2, 0, 2, 0, 2, 0],
            [0, 2, 0, 2, 0, 2, 0, 2],
            [2, 0, 2, 0, 2, 0, 2, 0]
        ]
        return {'board': board, 'turn': 'player1'}

    def handle_client(self, client_socket, player_id):
        while True:
            try:
                message = client_socket.recv(1024).decode()
                if message:
                    with self.lock:
                        if self.game_state['turn'] == player_id:
                            self.process_move(client_socket, message)
            except:
                self.clients.remove(client_socket)
                client_socket.close()
                break

    def process_move(self, client_socket, message):
        move = json.loads(message)
        if self.validate_move(move):
            self.update_game_state(move)
            self.broadcast_game_state()
            self.notify_next_player()
        else:
            client_socket.send(json.dumps({"status": "Invalid move"}).encode())

    def validate_move(self, move):
        # Implement move validation logic
        return True

    def update_game_state(self, move):
        start = move["start"]
        end = move["end"]
        captures = move.get("captures", [])
        piece = self.game_state["board"][start[0]][start[1]]
        self.game_state["board"][start[0]][start[1]] = 0
        self.game_state["board"][end[0]][end[1]] = piece
        self.game_state["turn"] = "player2" if self.game_state["turn"] == "player1" else "player1"

    def broadcast_game_state(self):
        game_state = json.dumps(self.game_state)
        for client in self.clients:
            client.send(game_state.encode())

    def notify_next_player(self):
        current_turn = self.game_state["turn"]
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