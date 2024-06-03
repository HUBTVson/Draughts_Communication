import colorama
from colorama import Fore, Style
from player import Player
from board import Board
import os
import platform

colorama.init()


class Game:
    def __init__(self):
        self.clear_text = ""
        self.elements = {'board': None, 'player1': None, 'player2': None}
        self.choose_os()
        self.add_players()
        self.add_board()
        self.fill_board()

    def choose_os(self):
        os = {'Windows': 'cls', 'Linux': 'clear'}
        self.clear_text = os[platform.system()]
        Board.clear_text = self.clear_text

    def clear_console(self):
        def clear(): return os.system(self.clear_text)
        clear()

    def add_players(self):
        self.elements['player1'] = Player('Player 1', Fore.GREEN, 1)
        self.elements['player2'] = Player('Player 2', Fore.YELLOW, 2)

    def add_board(self):
        self.elements['board'] = Board(8)

    def fill_board(self):
        self.elements['board'].generate_squares(
            self.elements['player1'], self.elements['player2'])

    def draw_board(self):
        self.elements['board'].draw_matrix()

    def convert_int(self, coordinates):
        for coor in coordinates:
            coordinates[coor] = int(coordinates[coor]) - 1
        return coordinates

    def pieces_left(self):
        return self.get_player1().get_amount_pieces() > 0 and self.get_player2().get_amount_pieces() > 0

    def forced_movements(self, playing):
        return self.elements['board'].verify_forced_movements(playing)

    def make_move(self, coordinates, playing, opponent):
        return self.elements['board'].move_piece(coordinates, playing, opponent)

    def get_player1(self):
        return self.elements['player1']

    def get_player2(self):
        return self.elements['player2']
    
    def get_winner(self):
        if self.get_player1().get_amount_pieces() <= 0:
            return 0
        if self.get_player2().get_amount_pieces() <= 0:
            return 1
        return None

    def show_winner(self):
        winner = self.get_player1() if self.get_player2(
        ).get_amount_pieces() <= 0 else self.get_player2()
        self.clear_console()
        print("\n\n\n\t\t\t" + winner.get_name_player() + " IS THE WINNER!!!!!")

    def process_move(self, move, player_id):
        coordinates = move
        coordinates = self.convert_int(coordinates)

        playing = self.get_player1() if player_id == 0 else self.get_player2()
        opponent = self.get_player1() if playing == self.get_player2() else self.get_player2()

        forced_movements = self.forced_movements(playing)
        if forced_movements != [] and [coordinates] not in forced_movements:
            return False

        playing = self.make_move(coordinates, playing, opponent)
        return True

    def get_game_state(self):
        return {
            'board': self.elements['board'].get_state(),
            'player1_pieces': self.get_player1().get_amount_pieces(),
            'player2_pieces': self.get_player2().get_amount_pieces(),
        }

    @property
    def state(self):
        board = self.elements['board'].matrix
        new_board = []
        for row in board:
            new_row = []
            for square in row:
                if square.piece:
                    color = 'black' if square.piece.p_color == '\x1b[33m' else 'white'
                    is_queen = square.piece.is_queen
                    if color == 'black':
                        if is_queen:
                            new_row.append(2)
                        else:
                            new_row.append(1)
                    else:
                        if is_queen:
                            new_row.append(-2)
                        else:
                            new_row.append(-1)
                else:
                    new_row.append(0)
            new_board.append(new_row)
        # przerobić board na matrix zer, jedynek i dwójek
        return new_board
