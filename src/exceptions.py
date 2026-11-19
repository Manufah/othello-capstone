class OthelloError(Exception):
    pass

class InvalidMoveError(OthelloError):
    pass

class GameOverError(OthelloError):
    pass