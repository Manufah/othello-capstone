import tkinter as tk
from tkinter import messagebox
from src.game_logic import OthelloBoard
from src.exceptions import InvalidMoveError, GameOverError
from src.storage import load_history, save_match_result, clear_history

class OthelloGUI:
    # Inisialisasi jendela utama, tata letak widget UI, dan objek papan permainan
    def __init__(self, root):
        super().__init__()
        self.root = root
        self.root.title("Othello Game")

        # Frame bagian atas untuk menampilkan informasi giliran dan skor
        self.frame_atas = tk.Frame(self.root)
        self.frame_atas.pack(pady = 10)

        self.label_info = tk.Label(self.frame_atas, text = "Giliran Hitam | Hitam: 2 | Putih: 2", font = ("Arial", 12, "bold"))
        self.label_info.pack()

        # Kanvas utama berukuran 480x480 piksel (grid 8x8 @ 60 piksel per kotak)
        self.canvas = tk.Canvas(self.root, width = 480, height = 480, bg = "#2E7D32")
        self.canvas.pack()
        # Menghubungkan klik kiri mouse pada papan ke metode on_board_click
        self.canvas.bind("<Button-1>", self.on_board_click)

        # Frame bagian bawah untuk tombol kontrol permainan dan riwayat skor
        self.frame_bawah = tk.Frame(self.root)
        self.frame_bawah.pack(pady = 10)
        
        self.btn_new = tk.Button(self.frame_bawah, text = "New Game", command = self.reset_game)
        self.btn_new.pack(side = tk.LEFT, padx = 5)
        
        self.btn_history = tk.Button(self.frame_bawah, text = "Riwayat Skor", command = self.show_history)
        self.btn_history.pack(side = tk.LEFT, padx = 5)

        # Status fitur petunjuk langkah sah (default mati saat pertama dibuka)
        self.show_hints = False
        self.btn_hint = tk.Button(self.frame_bawah, text = "HINT: OFF", command = self.toogle_hints)
        self.btn_hint.pack(side = tk.LEFT, padx = 5)

        # Menyiapkan objek logika Othello dan ukuran setiap petak
        self.board = OthelloBoard()
        self.cell_size = 60

        # Menggambar papan awal saat aplikasi pertama kali dijalankan
        self.draw_board()


    # Menggambar ulang seluruh petak 8x8, bidak hitam/putih, serta titik hint langkah sah
    def draw_board(self):
        self.canvas.delete("all")
        valid_moves = self.board.get_valid_moves(self.board.current_turn)
        for row in range(8):
            for col in range(8):
                # Menghitung batas koordinat piksel kiri-atas dan kanan-bawah setiap kotak
                x1 = col * self.cell_size
                y1 = row * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size

                # Menggambar garis kotak petak papan
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="#1B5E20", width=2)

                piece = self.board.grid[row][col]
                margin = 8

                # Menggambar bidak hitam, bidak putih, atau titik hint samar jika fitur HINT aktif
                if piece == "B":
                    self.canvas.create_oval(x1 + margin, y1 + margin, x2 - margin, y2 - margin, fill = "black")
                elif piece == "W":
                    self.canvas.create_oval(x1 + margin, y1 + margin, x2 - margin, y2 - margin, fill = "white")
                elif self.show_hints and piece not in ("B", "W") and (row, col) in valid_moves:
                    hint_margin = 22
                    self.canvas.create_oval(
                        x1 + hint_margin, y1 + hint_margin,
                        x2 - hint_margin, y2 - hint_margin,
                        fill="#1E5622", outline=""
                    )


    # Memperbarui teks giliran pemain dan perolehan skor terbaru di panel atas
    def update_info_label(self):
        scores = self.board.get_scores()
        turn_text = "Hitam" if self.board.current_turn == "B" else "Putih"
        self.label_info.config(text = f"Giliran {turn_text} | Hitam: {scores['B']} | Putih: {scores['W']}")

    # Menangani klik mouse pemain, memvalidasi langkah, dan mengecek kondisi akhir game
    def on_board_click(self, event):
        # Mengonversi koordinat klik piksel menjadi indeks kolom dan baris (0-7)
        col = event.x // self.cell_size
        row = event.y // self.cell_size

        # Mengabaikan klik jika berada di luar batas grid 8x8
        if not (0 <= row < 8 and 0 <= col < 8):
            return

        try:
            # Menaruh bidak pada papan logika lalu memperbarui tampilan dan skor
            self.board.place_piece(row, col)
            self.draw_board()
            self.update_info_label()

            # Jika permainan sudah berakhir, simpan hasil ke JSON dan tampilkan popup pemenang
            if self.board.game_over:
                scores = self.board.get_scores()
                winner = self.board.get_winner()

                save_match_result("Player Hitam", "Player Putih", scores["B"], scores["W"], winner)

                if winner == "B":
                    winner_text = "Player Hitam"
                elif winner == "C":
                    winner_text = "Player Putih"
                else:
                    winner_text = "Seri (Draw)"

                messagebox.showinfo("Game Over", f"Game Over! Pemenang: {winner_text} (Hitam: {scores['B']} - Putih: {scores['W']})")

        except (InvalidMoveError, GameOverError):
            # Mengabaikan klik pada petak yang tidak sah atau saat permainan sudah selesai
            pass


    # Mengubah status tampilan petunjuk langkah sah (ON/OFF) dan menggambar ulang papan
    def toogle_hints(self):
        self.show_hints = not self.show_hints
        status_text = "HINT: ON" if self.show_hints else "HINT: OFF"
        self.btn_hint.config(text = status_text)

        self.draw_board()


    # Mengatur ulang papan ke kondisi awal untuk memulai pertandingan baru
    def reset_game(self):
        self.board = OthelloBoard()
        self.draw_board()
        self.update_info_label()


    # Membuka jendela baru untuk menampilkan maksimal 10 riwayat pertandingan terakhir
    def show_history(self):
        history = load_history()
        if not history:
            messagebox.showinfo("Riwayat Skor", "Belum ada riwayat pertandingan")
            return
        
        win = tk.Toplevel(self.root)
        win.title("Riwayat Pertandingan")

        # Menyusun daftar teks riwayat dari pertandingan terbaru ke yang lebih lama
        lines = []
        for idx, item in enumerate(reversed(history[-10:]), start=1):
            winner_text = "Seri" if item["winner"] == "Draw" else ("Hitam" if item["winner"] == "B" else "Putih")
            line = (
                f"{idx}. [{item['timestamp']}] "
                f"Hitam ({item['score_black']}) vs Putih ({item['score_white']}) "
                f"-> Pemenang: {winner_text}"
                )
            lines.append(line)

        full_text = "\n".join(lines)
        label = tk.Label(win, text=full_text, justify=tk.LEFT, font=("Arial", 10), padx=15, pady=15)
        label.pack()

        # Fungsi internal untuk meminta konfirmasi sebelum menghapus semua riwayat
        def handle_clear():
            if messagebox.askyesno("Konfirmasi", "Yakin ingin menghapus semua riwayat pertandingan?"):
                clear_history()
                win.destroy()
                messagebox.showinfo("Berhasil", "Riwayat pertandingan telah dihapus.")

        btn_clear = tk.Button(win, text="Hapus Riwayat", command=handle_clear)
        btn_clear.pack(pady=(0, 15))