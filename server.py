import socket
import threading
import json
import numpy as np
from checkers import Checkers
from typing import Tuple, List


class CheckersServer:
    def __init__(self, host='localhost', port=5555) -> None:
        self.host = host
        self.port = port
        self.start_server(host, port)
        self.initialize_game()

    def start_server(self, host: str, port: int) -> None:
        # Start server on specified host and port
        self.clients: List[Tuple[socket.socket, int]] = []
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen(2)
        print(f"Server started on {host}:{port}")

        self.lock = threading.Lock()

    def initialize_game(self) -> None:
        # Initialize game state
        self.game = Checkers()

    def broadcast_message(self, message: str) -> None:
        # Broadcast message to all clients
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

        # Clear list of clients and close server
        self.clients = []
        self.server.close()

        # Restart server
        self.initialize_game()
        self.start_server(self.host, self.port)
        self.start()

    def handle_client(self, client_socket: socket.socket, player_id: int, debug: bool = False) -> None:
        while True:
            try:
                # Receive message from client
                message = client_socket.recv(1024).decode()
                # Deserialize message
                message = json.loads(message)

                # Check for message type
                if message["status"] == "EXIT":
                    raise Exception("Client exited")

                # Process move
                if message["status"] == "move":
                    message = message["move"]
                    with self.lock:
                        if self.game.turn == player_id:
                            self.process_move(client_socket, message)
            except Exception as e:
                if debug:
                    print(e)

                # Remove client from list of clients
                try:
                    self.clients.remove((client_socket, player_id))
                    client_socket.close()
                except Exception as ignored:
                    pass

                # Broadcast message and exit thread
                self.broadcast_message(json.dumps({
                    "status": "EXIT",
                    "message": f"Player {player_id} has left the game"
                }))
                break

    def process_move(self, client_socket: socket.socket, move: str) -> None:
        # Process move from client

        # Validate move
        if self.game.validate_move(move):
            # If move is valid, update game state
            self.game.move(move)
            # Broadcast game state to all clients
            self.broadcast_game_state()
        else:
            # If move is invalid, send message to client
            client_socket.send(json.dumps({"status": "Invalid move"}).encode())

    def broadcast_game_state(self) -> None:
        # Broadcast game state to all clients

        # Serialize game state
        game_state = json.dumps(self.game.state)
        # Send game state to all clients
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
            print(f"Player {player_id} connected from {addr}")

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
