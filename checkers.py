from poglądowe.game import Game


class Checkers():
    def __init__(self) -> None:
        self.game = Game()
        self._turn = 1
        

    def validate_move(self, move: dict) -> None:
        # Check if the move is valid
        self.game.process_move(self, move, self.game.pl)
        return True

    def move(self, move: dict) -> None:
        # Update the board with the new move and switch turns
        pass

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
        return self._board
