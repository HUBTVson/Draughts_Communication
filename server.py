import socket
import threading
import json
import signal
import numpy as np
from checkers import Checkers
from typing import Tuple, List


class CheckersServer:
    def __init__(self, host='localhost', port=5555) -> None:
        self.start_server(host, port)
        self.initialize_game()

    def start_server(self, host: str, port: int) -> None:
        self.clients: List[Tuple[socket.socket, int]] = []
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen(2)
        print(f"Server started on {host}:{port}")

        self.lock = threading.Lock()
        signal.signal(signal.SIGINT, self.shutdown)

    def initialize_game(self) -> None:
        self.game = Checkers()

    def broadcast_message(self, message: str) -> None:
        for client, _ in self.clients:
            client.send(message.encode())

    def restart_server(self) -> None:
        # Broadcast message to clients
        msg = json.dumps({
            "status": "EXIT",
            "message": "Server is restarting"
        })
        self.broadcast_message(msg)

        # Close all client connections
        for client, _ in self.clients:
            client.close()
        self.clients = []
        self.server.close()

        # Restart server
        self.initialize_game()
        self.start()

    def handle_client(self, client_socket: socket.socket, player_id: int) -> None:
        while True:
            try:
                message = client_socket.recv(1024).decode()
                if message["status"] == "EXIT":
                    self.clients.remove(client_socket)
                    client_socket.close()
                    self.broadcast_message(json.dumps({
                        "status": "EXIT",
                        "message": f"Player {player_id} has left the game"
                    }))
                    break

                if message["status"] == "move":
                    with self.lock:
                        if self.game.turn == player_id:
                            self.process_move(client_socket, message)
            except:
                if client_socket in self.clients:
                    self.clients.remove(client_socket)
                    client_socket.close()
                self.broadcast_message(json.dumps({
                    "status": "EXIT",
                    "message": f"Player {player_id} has left the game"
                }))
                break

    def process_move(self, client_socket: socket.socket, message: str) -> None:
        move = json.loads(message)
        if self.game.validate_move(move):
            self.game.move(move)
            self.broadcast_game_state()
        else:
            client_socket.send(json.dumps({"status": "Invalid move"}).encode())

    def broadcast_game_state(self) -> None:
        game_state = json.dumps(self.game.state)
        for client, _ in self.clients:
            msg = json.dumps({
                "status": "update",
                "game_state": game_state
            })
            client.send(msg.encode())

    def start(self) -> None:
        player_ids = [1, 2]
        workers = []

        while len(self.clients) < 2:
            # Accept connection from client
            client_socket, addr = self.server.accept()

            # Assign player id to client
            player_id = np.random.choice(player_ids)
            player_ids.remove(player_id)

            # Add client to list of clients
            self.clients.append((client_socket, player_id))
            print(f"{player_id} connected from {addr}")

            # Start a new thread to handle client
            thread = threading.Thread(target=self.handle_client, args=(
                client_socket, player_id))
            workers.append(thread)
            thread.start()

            # Send player id to client
            client_socket.send(str(player_id).encode())

        self.broadcast_game_state()

        # Restart server when game ends
        for worker in workers:
            worker.join()
        self.restart_server()

    def shutdown(self, signum, frame):
        print("\nShutting down server...")
        for client, _ in self.clients:
            client.close()
        self.server.close()
        exit()


if __name__ == "__main__":
    server = CheckersServer()
    server.start()
