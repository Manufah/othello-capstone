from src.exceptions import InvalidMoveError, GameOverError

class Player:
    # Menyimpan atribut identitas pemain (nama, warna bidak, dan skor)
    def __init__(self, name, color, score = 2):
        self.name = str(name)
        self.color = color
        self.score = score

class OthelloBoard:
    # Konstanta ukuran papan 8x8, simbol isi petak, dan 8 arah penjuru mata angin
    SIZE = 8
    EMPTY = "."
    BLACK = "B"
    WHITE = "W"
    DIRECTIONS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]


    # Inisialisasi atribut awal papan dan langsung mengatur ulang ke posisi pembuka
    def __init__(self):
        self.grid = []
        self.current_turn = self.BLACK
        self.game_over = False

        self.reset_board()


    # Mengosongkan grid 8x8 dan menempatkan 4 bidak awal secara diagonal di tengah papan
    def reset_board(self):
        self.grid = []
        for board in range(self.SIZE):
            self.grid.append([self.EMPTY] * self.SIZE)

        # Posisi awal standar Othello: 2 Putih di (3,3) & (4,4), 2 Hitam di (3,4) & (4,3)
        self.grid[3][3] = self.WHITE
        self.grid[4][4] = self.WHITE
        self.grid[3][4] = self.BLACK
        self.grid[4][3] = self.BLACK

        self.current_turn = self.BLACK
        self.game_over = False


    # Mengecek apakah koordinat (row, col) masih berada di dalam batas grid 0..7
    def is_within_bounds(self, row, col):
        return 0 <= row < self.SIZE and 0 <= col < self.SIZE


    # Mencari daftar koordinat bidak lawan yang terjepit jika bidak ditaruh di (row, col)
    def get_flippable_pieces(self, row, col, color):
        # Tidak valid jika koordinat di luar papan atau petak sudah terisi bidak
        if not self.is_within_bounds(row, col) or self.grid[row][col] != self.EMPTY:
            return []

        # Menentukan warna bidak lawan berdasarkan warna pemain saat ini
        if color == self.BLACK:
            opponent = self.WHITE
        elif color == self.WHITE:
            opponent = self.BLACK

        flippable = []

        # Menelusuri seluruh 8 arah dari titik (row, col)
        for dr, dc in self.DIRECTIONS:
            r = row + dr
            c = col + dc
            pieces_in_direction = []

            # Kumpulkan koordinat bidak lawan yang berderet tanpa terputus di arah ini
            while self.is_within_bounds(r, c) and self.grid[r][c] == opponent:
                pieces_in_direction.append((r, c))
                r += dr
                c += dc

            # Sah menjepit jika di ujung deretan bidak lawan bertemu bidak milik sendiri
            if self.is_within_bounds(r, c) and self.grid[r][c] == color and len(pieces_in_direction) > 0:
                flippable.extend(pieces_in_direction)

        return flippable


    # Mengembalikan seluruh daftar koordinat (row, col) yang sah dilangkahi oleh warna tertentu
    def get_valid_moves(self, color):
        valid_moves = []

        for row in range(self.SIZE):
            for col in range(self.SIZE):
                if self.get_flippable_pieces(row, col, color):
                    valid_moves.append((row, col))

        return valid_moves


    # Menghitung jumlah total bidak Hitam dan Putih yang ada di papan saat ini
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


    # Menjalankan satu langkah pemain: validasi, taruh bidak, balik bidak lawan, dan atur giliran
    def place_piece(self, row, col):
        if self.game_over == True:
            raise GameOverError("Permainan sudah berakhir!")

        # Cek apakah posisi yang dipilih mampu menjepit minimal satu bidak lawan
        flippable = self.get_flippable_pieces(row, col, self.current_turn)
        if not flippable:
            raise InvalidMoveError("Langkah tidak valid!")

        # Tempatkan bidak baru dan ubah warna seluruh bidak lawan yang terjepit
        self.grid[row][col] = self.current_turn

        for r, c in flippable:
            self.grid[r][c] = self.current_turn

        # Menentukan warna lawan untuk pengecekan giliran berikutnya
        if self.current_turn == self.BLACK:
            opponent = self.WHITE
        elif self.current_turn == self.WHITE:
            opponent = self.BLACK

        # Pindah giliran ke lawan jika punya langkah sah, auto-pass jika tidak ada, atau akhiri game
        if len(self.get_valid_moves(opponent)) > 0:
            self.current_turn = opponent
        elif len(self.get_valid_moves(self.current_turn)) > 0:
            pass
        else:
            self.game_over = True


    # Menentukan hasil pemenang berdasarkan skor akhir setelah game_over bernilai True
    def get_winner(self):
        if not self.game_over:
            return None

        scores = self.get_scores()
        black_score = scores[self.BLACK]
        white_score = scores[self.WHITE]

        if black_score > white_score:
            return self.BLACK
        elif white_score > black_score:
            return self.WHITE
        else:
            return "DRAW"