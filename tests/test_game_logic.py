import unittest
import os
from src.game_logic import OthelloBoard
from src.exceptions import InvalidMoveError, GameOverError
from src.storage import load_history, save_match_result

class TestOthelloLogic(unittest.TestCase):
    # mempersiapkan kondisi awal sebelum setiap test dilakukan
    def setUp(self):
        self.board = OthelloBoard()
        self.test_file = "data/test_scores.json"

    # membersihkan kondisi setelah setiap fungsi selesai dilakukan
    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    # menguji bahwa 4 bidak awal sudah terpasang di posisi yang tepat
    # memastikan skor awal masing - masing adalah 2
    def test_initial_board_setup(self):
        self.assertEqual(self.board.get_scores(), {"B": 2, "W": 2})
        self.assertEqual(self.board.current_turn, "B")

    # memastikan pemain hitam memiliki tepat 4 langkah sah di awal game 
    def test_initial_valid_moves(self):
        self.assertEqual(len(self.board.get_valid_moves("B")), 4)
        self.assertIn((2, 3), self.board.get_valid_moves("B"))

    # menguji penempatan koordinat bidak yang sah
    # memastikan bidak lawan yang terjepit di tengah tengah berubah warna
    # memastikan skor ter-update
    # memastikan giliran berpindah ke lawannya
    def test_place_piece_and_flip(self):
        self.board.place_piece(2, 3)
        self.assertEqual(self.board.grid[2][3], "B")
        self.assertEqual(self.board.grid[3][3], "B")

        self.assertEqual(self.board.get_scores(), {"B": 4, "W": 1})
        self.assertEqual(self.board.current_turn, "W")

    # mencoba kondisi error ketika player mencoba menaruh bidak di kotak yang sudah terisi atau kotak yang tidak menjepit lawan
    def test_invalid_move_raises_exception(self):
        with self.assertRaises(InvalidMoveError):
            self.board.place_piece(0, 0)

    # menguji skenario ketika satu pemain tidak punya langkah sah (giliran berganti ke lawannya) dan ketika kedua pemain buntu (game_over menjadi True)
    def test_storage_save_and_load(self):
        save_match_result("Rahmat", "Lawan", 40, 24, "B", filepath=self.test_file)
        history = load_history(self.test_file)
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]["player_black"], "Rahmat")
        self.assertEqual(history[0]["winner"], "B")

if __name__ == "__main__":
    unittest.main()