import socket
import threading
import json
import signal


class CheckersClient:
    def __init__(self, host='localhost', port=5555):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.connect((host, port))
        signal.signal(signal.SIGINT, self.shutdown)
        threading.Thread(target=self.listen_for_updates).start()
        self.game_state = None
        self.player_id = None

    def listen_for_updates(self):
        # Receive player id
        self.player_id = self.server.recv(1024).decode()
        print(f"You are player{self.player_id}")

        while True:
            message = self.server.recv(1024).decode()
            if message:
                data = json.loads(message)

                if data["status"] == "EXIT":
                    print(data["message"])
                    self.server.close()
                    exit()

                elif data["status"] == "Invalid move":
                    print("Invalid move. Try again.")
                    self.get_user_input()

                elif data["status"] == "update":
                    self.game_state = json.loads(data["game_state"])
                    self.render_board()
                    if self.game_state["turn"] == self.player_id:
                        self.get_user_input()

                else:
                    print("Unknown message")
                    print(data)

    def send_move(self, start, end, captures=[]):
        move = {
            "start": start,
            "end": end,
            "captures": captures
        }
        msg = json.dumps({
            "status": "move",
            "move": move
        }).encode()
        self.server.send(msg)

    def render_board(self):
        board = self.game_state["board"]
        for row in board:
            print(' '.join(map(str, row)))
        print()

    def get_user_input(self):
        try:
            print(f"Player{self.player_id}'s turn")
            start = input("Enter start position (row,col): ").split(',')
            end = input("Enter end position (row,col): ").split(',')
        except KeyboardInterrupt:
            self.server.send(json.dumps({
                "status": "EXIT"
            }).encode())
            self.shutdown(None, None)

        start = (int(start[0]), int(start[1]))
        end = (int(end[0]), int(end[1]))
        self.send_move(start, end)

    def shutdown(self, signum, frame):
        print("\nShutting down client...")
        self.server.close()
        exit()


if __name__ == "__main__":
    server = CheckersClient()
