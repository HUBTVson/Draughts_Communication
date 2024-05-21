class Checkers():
    def __init__(self) -> None:
        self._board = [
            [0, 1, 0, 1, 0, 1, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 0],
            [0, 1, 0, 1, 0, 1, 0, 1],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [2, 0, 2, 0, 2, 0, 2, 0],
            [0, 2, 0, 2, 0, 2, 0, 2],
            [2, 0, 2, 0, 2, 0, 2, 0]
        ]
        self._turn = 1
        

    def validate_move(self, move: dict) -> None:
        # Check if the move is valid
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
