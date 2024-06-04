import queue
import socket
import threading
import json
from colorama import Fore, Style
import msvcrt

from piece import Piece
from square import Square


class CheckersClient:
    def __init__(self, host='localhost', port=5555):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.connect((host, port))
        self._input_queue = queue.Queue()
        self._input_interrupt = False
        self.game_state = None
        self.player_id = None
        self.input_thread = threading.Thread(
            target=self._safe_input, daemon=True)
        self.input_thread.start()
        self.listen_for_updates()

    def _safe_input(self) -> str:
        """Read input, handle "quit" command, KeyboardInterrupt and EOFError"""

        # wait for input unless the input_interrupt is set
        input_stoppers = ['\r', '\n']
        while not self._input_interrupt:
            try:
                input_str = ""
                last_key = None

                while not self._input_interrupt:
                    last_key = msvcrt.getwche()
                    if last_key in input_stoppers:
                        break
                    if last_key == '\b':
                        if input_str:
                            input_str = input_str[:-1]
                            print(' \b', end='', flush=True)

                    input_str += last_key

            except (KeyboardInterrupt, EOFError):
                print("info Keyboard interrupt")
                self.shutdown(None, None)
            if input_str == "quit".casefold():
                self.shutdown(None, None)

            self._input_queue.put(input_str)

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
                    self._input_interrupt = True
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
            "from_x": start[0],
            "from_y": start[1],
            "to_x": end[0],
            "to_y": end[1]
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
        new_board = []
        for row in range(8):
            new_row = []
            for column in range(8):
                if (row + column) % 2 == 0:
                    new_row.append(Square(Fore.WHITE))
                else:
                    new_row.append(Square(Fore.BLACK))

                if board[row][column] == 1:
                    new_row[column].piece = Piece(Fore.GREEN)
                elif board[row][column] == -1:
                    new_row[column].piece = Piece(Fore.RED)
                elif board[row][column] == 2:
                    new_row[column].piece = Piece(Fore.GREEN)
                    new_row[column].piece.convert_to_queen()
                elif board[row][column] == -2:
                    new_row[column].piece = Piece(Fore.RED)
                    new_row[column].piece.convert_to_queen()
            new_board.append(new_row)

        draw_b = 'x→ '
        reset = Style.RESET_ALL
        con = 0
        for a in range(1, 9):
            draw_b += str(a) + ' '
        draw_b += ' y↓'
        draw_b += '\n'
        for row in new_board:
            draw_b += '   '
            for col in row:
                if col.is_piece_inside():
                    piece_string = col.get_piece().get_character() + ' '
                    draw_b += col.piece_color() + piece_string + reset
                else:
                    draw_b += col.color + '■ ' + reset
            con += 1
            draw_b += '|' + str(con) + '\n'
        print(draw_b)

    def get_user_input(self):
        # Get user input for move
        try:
            print(f"Player{self.player_id}'s turn\n")

            print("Enter start position (row,col) or 'quit' to exit:")
            start = self._input_queue.get(block=True)
            # if start == "quit":
            #     self.shutdown(None, None)

            print("Enter end position (row,col):")
            end = self._input_queue.get(block=True)
            # if end == "quit":
            #     self.shutdown(None, None)

            # # CHANGE HERE START
            # start = input("Enter start position (row,col): ").split(',')
            # end = input("Enter end position (row,col): ").split(',')
            # # CHANGE HERE END
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
        self._input_interrupt = True
        raise SystemExit


if __name__ == "__main__":
    server = CheckersClient()
