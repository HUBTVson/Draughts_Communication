import socket
import threading
import json


class CheckersClient:
    def __init__(self, host='localhost', port=5555):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.connect((host, port))
        threading.Thread(target=self.listen_for_updates).start()
        self.game_state = None
        self.player_id = None

    def listen_for_updates(self):
        # Receive player id
        self.player_id = self.server.recv(1024).decode()
        print(f"You are player{self.player_id}")

        while True:
            # Receive message from server
            message = self.server.recv(1024).decode()
            if message:
                # Decode message
                data = json.loads(message)

                # Check for message type
                if data["status"] == "EXIT":
                    # Close client connection and exit
                    print(data["message"])
                    self.server.close()
                    exit()

                elif data["status"] == "Invalid move":
                    # Print error message and prompt user for input
                    print("Invalid move. Try again.")
                    self.get_user_input()

                elif data["status"] == "update":
                    # Update game state and render board
                    self.game_state = json.loads(data["game_state"])
                    self.render_board()
                    if self.game_state["turn"] == self.player_id:
                        self.get_user_input()

                else:
                    # Unknown message
                    print("Unknown message")
                    print(data)

    def send_move(self, start, end, captures=[]):
        # Send move to server

        move = {
            # CHANGE HERE START
            "start": start,
            "end": end,
            "captures": captures
            # CHANGE HERE END
        }

        # Serialize move and send to server
        msg = json.dumps({
            "status": "move",
            "move": move
        }).encode()
        self.server.send(msg)

    def render_board(self):
        # Render game board

        # ADD PRETTY PRINTING
        board = self.game_state["board"]
        for row in board:
            print(' '.join(map(str, row)))
        print()

    def get_user_input(self):
        # Get user input for move
        try:
            print(f"Player{self.player_id}'s turn")

            # CHANGE HERE START
            start = input("Enter start position (row,col): ").split(',')
            end = input("Enter end position (row,col): ").split(',')
            # CHANGE HERE END
        except:
            self.shutdown(None, None)

        # Send move to server
        start = (int(start[0]), int(start[1]))
        end = (int(end[0]), int(end[1]))
        self.send_move(start, end)

    def shutdown(self, signum, frame):
        # Send exit message to server
        self.server.send(json.dumps({
            "status": "EXIT"
        }).encode())
        # Shutdown client
        print("\nShutting down client...")
        self.server.close()
        exit()


if __name__ == "__main__":
    server = CheckersClient()
