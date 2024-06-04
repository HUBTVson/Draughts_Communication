import socket
import threading
import json
from colorama import Fore, Style
from piece import Piece
from square import Square


class CheckersClient:
    def __init__(self, host='localhost', port=5555):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.connect((host, port))
        threading.Thread(target=self.listen_for_updates).start()
        self.game_state = None
        self.player_id = None

    def listen_for_updates(self):
        self.player_id = self.server.recv(1024).decode()
        print(f"You are player {self.player_id}")

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
            "from_x": start[0],
            "from_y": start[1],
            "to_x": end[0],
            "to_y": end[1]
        }
        msg = json.dumps({
            "status": "move",
            "move": move
        }).encode()
        self.server.send(msg)

    def render_board(self):
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
        try:
            print(f"Player {self.player_id}'s turn")
            user_input = input("Enter move (start_x,start_y end_x,end_y) or 'exit' to quit: ").strip()
            if user_input.lower() == 'exit':
                self.shutdown()
            else:
                start, end = user_input.split()
                start = tuple(map(int, start.split(',')))
                end = tuple(map(int, end.split(',')))
                self.send_move(start, end)
        except Exception as e:
            print(f"Invalid Input, try again")
            self.get_user_input()

    def shutdown(self):
        self.server.send(json.dumps({"status": "EXIT"}).encode())
        print("Shutting down client...")
        self.server.close()
        exit()


if __name__ == "__main__":
    client = CheckersClient()
