from poglądowe.game import Game


class Checkers():
    def __init__(self) -> None:
        self.game = Game()
        self._turn = 1

    def move(self, move: dict) -> bool:
        # Update the board with the new move and switch turns
        if self.game.elements['board'].verify_moves(move, self._turn, self.game.elements['board'].difference_between_directions(move)):
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
