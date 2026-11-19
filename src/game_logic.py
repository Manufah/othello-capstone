class Player:
    def __init__(self, name, color, score = 2):
        self.name = str(name)
        self.color = color
        self.score = score

class OthelloBoard:
    SIZE = 8
    EMPTY = "."
    BLACK = "B"
    WHITE = "W"
    DIRECTIONS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    
    def __init__(self):
        self.grid = []
        self.current_turn = self.BLACK
        self.game_over = False

        self.reset_board()

    def reset_board(self):
        self.grid = []
        for board in range(self.SIZE):
            self.grid.append([self.EMPTY] * self.SIZE)

        self.grid[3][3] = self.WHITE
        self.grid[4][4] = self.WHITE
        self.grid[3][4] = self.BLACK
        self.grid[4][3] = self.BLACK

        self.current_turn = self.BLACK
        self.game_over = False

    def is_within_bounds(self, row, col):
        return 0 <= row < self.SIZE and 0 <= col < self.SIZE
