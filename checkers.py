from game import Game


class Checkers():
    def __init__(self) -> None:
        self.game = Game()
        self._turn = 0
        self.players = [self.game.elements['player1'],
                        self.game.elements['player2']]

    def move(self, move: dict) -> bool:
        # Update the board with the new move and switch turns
        move_tmp = move.copy()
        move_tmp['from_x'] = int(move['from_x'] - 1)
        move_tmp['from_y'] = int(move['from_y'] - 1)
        move_tmp['to_x'] = int(move['to_x'] - 1)
        move_tmp['to_y'] = int(move['to_y'] - 1)
        if self.game.elements['board'].verify_moves(move_tmp, self.players[self._turn], self.game.elements['board'].difference_between_and_direction(move_tmp)):
            self.game.process_move(move, self._turn)
            self.turn += 1
            print(self._turn)
            return True
        else:
            print("Invalid move")
            return False

    @property
    def state(self) -> dict:
        return {
            "board": self.board,
            "turn": str(self.turn)
        }

    @property
    def turn(self) -> int:
        return self._turn

    @turn.setter
    def turn(self, value: int) -> None:
        self._turn = value % 2

    @property
    def board(self) -> list:
        return self.game.state
