import colorama
from colorama import Fore, Style
from poglądowe.player import Player
from poglądowe.board import Board
import os
import platform
import json

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
        clear = lambda: os.system(self.clear_text)
        clear()

    def add_players(self):
        self.elements['player1'] = Player('Player 1', Fore.GREEN, 1)
        self.elements['player2'] = Player('Player 2', Fore.YELLOW, 2)

    def add_board(self):
        self.elements['board'] = Board(8)

    def fill_board(self):
        self.elements['board'].generate_squares(self.elements['player1'], self.elements['player2'])

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

    def show_winner(self):
        winner = self.get_player1() if self.get_player2().get_amount_pieces() <= 0 else self.get_player2()
        self.clear_console()
        print("\n\n\n\t\t\t" + winner.get_name_player() + " IS THE WINNER!!!!!")

    def process_move(self, move, player_id):
        coordinates = move['coordinates']
        coordinates = self.convert_int(coordinates)

        playing = self.get_player1() if player_id == 'player1' else self.get_player2()
        opponent = self.get_player1() if playing == self.get_player2() else self.get_player2()

        forced_movements = self.forced_movements(playing)
        if forced_movements != [] and [coordinates] not in forced_movements:
            return False, "Mandatory movements"

        playing = self.make_move(coordinates, playing, opponent)
        return True, "Move successful"

    def get_game_state(self):
        return {
            'board': self.elements['board'].get_state(),
            'player1_pieces': self.get_player1().get_amount_pieces(),
            'player2_pieces': self.get_player2().get_amount_pieces(),
        }
