import socket
import threading
import json
import numpy as np
from checkers import Checkers
from typing import Tuple, List


class CheckersServer:
    def __init__(self, host='localhost', port=5555):
        self.host = host
        self.port = port
        self.start_server(host, port)
        self.initialize_game()

    def start_server(self, host: str, port: int) -> None:
        self.clients: List[Tuple[socket.socket, int]] = []
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen(2)
        print(f"Server started on {host}:{port}")

        self.lock = threading.Lock()

    def initialize_game(self) -> None:
        self.game = Checkers()

    def broadcast_message(self, message: str) -> None:
        for client, _ in self.clients:
            client.send(message.encode())

    def restart_server(self) -> None:
        msg = json.dumps({
            "status": "EXIT",
            "message": "Server is restarting"
        })
        self.broadcast_message(msg)
        for client, _ in self.clients:
            client.close()
        self.clients = []
        self.server.close()
        self.initialize_game()
        self.start_server(self.host, self.port)
        self.start()

    def handle_client(self, client_socket: socket.socket, player_id: int, debug: bool = True) -> None:
        while True:
            try:
                message = client_socket.recv(1024).decode()
                message = json.loads(message)
                if message["status"] == "EXIT":
                    raise Exception("Client exited")
                if message["status"] == "move":
                    message = message["move"]
                    with self.lock:
                        if self.game.turn == player_id:
                            self.process_move(client_socket, message)
            except Exception as e:
                if debug:
                    print(e)
                try:
                    self.clients.remove((client_socket, player_id))
                    client_socket.close()
                except Exception as ignored:
                    pass
                self.broadcast_message(json.dumps({
                    "status": "EXIT",
                    "message": f"Player {player_id} has left the game"
                }))
                break

    def process_move(self, client_socket: socket.socket, move) -> None:
        if self.game.move(move):
            winner = self.game.winner
            if winner is not None:
                msg = json.dumps({
                    "status": "EXIT",
                    "message": f"Player {winner} has won the game"
                })
                self.broadcast_message(msg)
                self.restart_server()
            else:
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
        player_ids = [0, 1]
        workers = []

        while len(self.clients) < 2:
            client_socket, addr = self.server.accept()
            player_id = np.random.choice(player_ids)
            player_ids.remove(player_id)
            self.clients.append((client_socket, player_id))
            print(f"Player {player_id} connected from {addr}")
            thread = threading.Thread(target=self.handle_client, args=(client_socket, player_id))
            workers.append(thread)
            thread.start()
            client_socket.send(str(player_id).encode())

        self.broadcast_game_state()

        for worker in workers:
            worker.join()
        self.restart_server()

    def shutdown(self, signum, frame):
        print("Shutting down server...")
        for client, _ in self.clients:
            client.close()
        self.server.close()
        exit()


if __name__ == "__main__":
    server = CheckersServer()
    server.start()
