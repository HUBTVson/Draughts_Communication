import socket
import threading
import json
import signal

class CheckersClient:
    def __init__(self, host='localhost', port=5555):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))
        signal.signal(signal.SIGINT, self.shutdown)
        threading.Thread(target=self.listen_for_updates).start()

    def listen_for_updates(self):
        while True:
            message = self.client.recv(1024).decode()
            if message:
                data = json.loads(message)
                if 'status' in data and data['status'] == 'Your turn':
                    print("It's your turn!")
                    self.get_user_input()
                else:
                    self.game_state = data
            self.render_board()

    def send_move(self, start, end, captures=[]):
        move = {
            "start": start,
            "end": end,
            "captures": captures
        }
        self.client.send(json.dumps(move).encode())

    def render_board(self):
        board = self.game_state["board"]
        for row in board:
            print(' '.join(map(str, row)))
        print()

    def get_user_input(self):
        start = input("Enter start position (row,col): ").split(',')
        end = input("Enter end position (row,col): ").split(',')
        start = [int(start[0]), int(start[1])]
        end = [int(end[0]), int(end[1])]
        self.send_move(start, end)

    def shutdown(self, signum, frame):
        print("\nShutting down client...")
        self.client.close()
        exit()

if __name__ == "__main__":
    client = CheckersClient()
