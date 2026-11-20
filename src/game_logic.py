from src.exceptions import InvalidMoveError, GameOverError

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


    def get_flippable_pieces(self, row, col, color):
        if not self.is_within_bounds(row, col) or self.grid[row][col] != self.EMPTY:
            return []

        if color == self.BLACK:
            opponent = self.WHITE
        elif color == self.WHITE:
            opponent = self.BLACK

        flippable = []

        for dr, dc in self.DIRECTIONS:
            r = row + dr
            c = col + dc
            pieces_in_direction = []

            while self.is_within_bounds(r, c) and self.grid[r][c] == opponent:
                pieces_in_direction.append((r, c))
                r += dr
                c += dc

            if self.is_within_bounds(r, c) and self.grid[r][c] == color and len(pieces_in_direction) > 0:
                flippable.extend(pieces_in_direction)

        return flippable


    def get_valid_moves(self, color):
        valid_moves = []

        for row in range(self.SIZE):
            for col in range(self.SIZE):
                if self.get_flippable_pieces(row, col, color):
                    valid_moves.append((row, col))

        return valid_moves


    def get_scores(self):
        black_score = 0
        white_score = 0

        for row in self.grid:
            for col in row:
                if col == self.BLACK:
                    black_score += 1
                elif col == self.WHITE:
                    white_score += 1

        return {
            self.BLACK: black_score,
            self.WHITE: white_score
        }


    def place_piece(self, row, col):
        if self.game_over == True:
            raise GameOverError("Permainan sudah berakhir!")

        flippable = self.get_flippable_pieces(row, col, self.current_turn)
        if not flippable:
            raise InvalidMoveError("Langkah tidak valid!")

        self.grid[row][col] = self.current_turn

        for r, c in flippable:
            self.grid[r][c] = self.current_turn

        if self.current_turn == self.BLACK:
            opponent = self.WHITE
        elif self.current_turn == self.WHITE:
            opponent = self.BLACK

        if len(self.get_valid_moves(opponent)) > 0:
            self.current_turn = opponent
        elif len(self.get_valid_moves(self.current_turn)) > 0:
            pass
        else:
            self.game_over = True


    def get_winner(self):
        if not self.game_over:
            return None

        scores = self.get_scores()
        black_score = scores[self.BLACK]
        white_score = scores[self.WHITE]

        if black_score > white_score:
            return black_score
        elif white_score > black_score:
            return white_score
        else:
            return "DRAW"