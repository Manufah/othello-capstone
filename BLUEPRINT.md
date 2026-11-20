# Blueprint Capstone: Othello

## 1. Peta Arsitektur Modul
* **src/exceptions.py**: Mendefinisikan kelas error khusus aturan game agar program tidak crash saat terjadi kesalahan input/langkah.

* **src/game_logic.py**: Otak permainan (Backend). Mengelola status papan, validasi langkah 8 arah, pembalikan bidak, skor, dan aturan auto-pass / game over.

* **src/storage.py**: Pengelola berkas (Persistence). Membaca dan menyimpan riwayat pertandingan atau leaderboard ke format JSON.

* **tests/test_game_logic.py**: Skenario pengujian otomatis untuk membuktikan semua aturan game berjalan akurat tanpa perlu membuka UI.

* **src/main_ui.py**: Antarmuka grafis (Frontend) berbasis Tkinter untuk interaksi 2 pemain menggunakan mouse/keyboard.


## 2. Rincian Spesifikasi Komponen per Modul

### Modul A: src/exceptions.py (Penanganan Kesalahan)
1. OthelloError(Exception): Kelas induk untuk seluruh pengecualian spesifik game Othello.
2. InvalidMoveError(OthelloError): Dilempar saat pemain memilih koordinat di luar papan (0...7), petak yang sudah terisi, atau petak yang tidak menjepit bidak lawan.
3. GameOverError(OthelloError): Dilempar saat pemain mencoba melakukan aksi melangkah ketika permainan sudah berakhir.

### Modul B: src/game_logic.py (Inti Permainan & OOP)

#### Kelas 1: Player
* **Atribut:**
    * name (str): Nama pemain.

    * color (str): Warna bidak pemain ("B" untuk Hitam atau "W" untuk Putih).

    * score (int): Jumlah bidak pemain di papan saat ini (nilai awal 2).

#### Kelas 2: OthelloBoard
* **Konstanta Kelas:**
    SIZE = 8, EMPTY = ".", BLACK = "B", WHITE = "W".

    DIRECTIONS: Kumpulan 8 tuple arah pergeseran koordinat (dr, dc).

* **Atribut Objek(__init__):**
    * grid: Matriks 2D (nested list) berukuran 8 X 8.
    * current_turn: Menyimpan giliran aktif (mulai dari "B").
    * game_over: Boolean penanda akhir permainan (False di awal).

* **Daftar Metode yang Harus Dibangun (Urut Berdasarkan Alur Kerja):**
    1. reset_board() (Sudah selesai): Mengosongkan grid 8 X 8, meletakkan 2 bidak Putih di (3,3) & (4,4) serta 2 bidak Hitam di (3,4) & (4,3), lalu menyetel ulang giliran ke Hitam dan game_over = False.

    2. is_within_bounds(row, col) (Sudah selesai): Mengembalikan True jika 0 <= row < 8 dan 0 <= col < 8.

    3. get_flippable_pieces(row, col, color):
        * Input: Koordinat tujuan & warna pemain.
        * Logika: Cek apakah petak tujuan kosong & dalam batas papan. Telusuri ke-8 arah mata angin; kumpulkan koordinat bidak lawan yang berderet lurus dan diujungnya tertutup oleh bidak color sendiri.
        * Output: list berisi tuple koordinat [(r, c), ...] bidak lawan yang sah dibalik.

    4. get_valid_moves(color):
        * Input: Warna pemain ("B" atau "W").
        * Logika: Periksa seluruh 64 petak di papan. Jika suatu petak kosong dan get_flippable_pieces() mengembalikan minimal 1 bidak, masukkan koordinat petak tersebut ke daftar.
        * Output: list berisi semua koordinat langkah yang sah untuk pemain tersebut.

    5. get_scores():
        * Logika: Menghitung total kemunculan "B" dan "W" di seluruh self.grid.
        * Output: dictionary berbentuk {"B": skor_hitam, "W": skor_putih}.

    6. place_piece(row, col):
        * Logika:
            a. Validasi (Guard Clause): Jika self.game_over bernilai True, lempar GameOverError. Jika (row, col) tidak ada di dalam get_valid_moves(self.current_turn), lempar InvalidMoveError.
            b. Eksekusi: Taruh bidak self.current_turn pada (row, col) dan ubah warna seluruh koordinat dari get_flippable_pieces() menjadi self.current_turn.
            c. Pergantian Giliran & Auto-Pass: Ganti giliran ke lawan. Cek apakah lawan punya langkah sah lewat get_valid_moves(). Jika lawan tidak punya langkah sah, kembalikan giliran ke pemain awal (pass). Jika kedua pemain sama-sama tidak punya langkah sah, ubah self.game_over = True.

    7. get_winner():
        * Logika: Membandingkan skor akhir dari get_scores(). Mengembalikan warna pemenang ("B" atau "W"), "DRAW" jika skor seri, atau None jika self.game_over masih False.

### Modul C: src/storage.py (Penyimpanan Skor ke File JSON)

1. load_history(filepath):
    * Membaca daftar riwayat pertandingan dari file JSON (File Input).
    * Menggunakan blok try-except untuk menangani FileNotFoundError (jika file belum ada, kembalikan list kosong []) dan json.JSONDecodeError (jika file korup/kosong, tangani dengan aman tanpa crash).

2. save_match_result(filepath, player_black, player_white, score_black, score_white, winner)
    * Memanggil load_history() untuk mengambil data lama, menambahkan dictionary hasil pertandingan terbaru (nama pemain, skor masing-masing, pemenang, serta waktu/tanggal), lalu menuliskannya kembali ke file JSON (File Output).

### Modul D: tests/test_game_logic.py (Pengujian Unit Test)

1. test_initial_board_setup: Memastikan 4 bidak tengah terpasang di posisi yang tepat dan skor awal masing-masing adalah 2.

2. test_initial_valid_moves: Memastikan pemain Hitam memiliki tepat 4 langkah sah di awal permainan: [(2, 3), (3, 2), (4, 5), (5, 4)].

3. test_place_piece_and_flip: Menguji penempatan bidak pada koordinat sah, memastikan bidak lawan di tengahnya berubah warna, skor ter-update, dan giliran berpindah ke Putih.

4. test_invalid_move_raises_exception: Menggunakan assertRaises(InvalidMoveError) saat mencoba menaruh bidak di kotak yang sudah terisi atau kotak yang tidak menjepit bidak lawan.

5. test_auto_pass_and_game_over: Menguji skenario papan kustom ketika satu pemain tidak punya langkah sah (giliran otomatis dilewati) dan ketika kedua pemain buntu (game_over menjadi True).

### Modul E: src/main_ui.py (Antarmuka Grafis Tkinter)

1. Layar Setup Pemain (Dialog / Frame Awal):
    * Input Entry untuk nama Pemain 1 (Hitam) dan Pemain 2 (Putih), serta tombol Mulai Permainan.

2. Panel Informasi Atas (Header):
    * Menampilkan nama pemain, indikator giliran aktif (misalnya teks/bingkai menyala untuk pemain yang sedang jalan), dan skor real-time kedua pemain.

3. Area Papan Utama (tk.Canvas):
    * Menggambar kotak grid 8 X 8 berwarna hijau klasik Othello.
    * Menggambar keping bidak berbentuk lingkaran hitam/putih sesuai isi board.grid.
    * Menggambar titik penanda kecil (hint) pada koordinat yang dihasilkan oleh board.get_valid_moves() agar pemain mudah melihat langkah yang diperbolehkan.
    * Mendeteksi klik mouse (<Button-1>), mengonversi koordinat piksel (x, y) menjadi indeks baris dan kolom (y // ukuran_kotak, x // ukuran_kotak), lalu memanggil board.place_piece(row, col) di dalam blok try-except OthelloError.

4. Panel Kontrol Bawah & Riwayat:
    * Tombol Restart (memanggil board.reset_board()), tombol Riwayat Skor (menampilkan data dari storage.py dalam jendela pop-up), serta otomatis menyimpan hasil dan menampilkan pemenang ketika board.game_over bernilai True.

## 3. Daftar Periksa (Checklist) Progres Pengerjaan
* **Tahap 0:** Setup repositori GitHub, struktur folder, dan .gitignore.
* **Tahap 1**: Membuat Custom Exception di src/exceptions.py.
* **Tahap 2A**: Membuat kelas Player serta kerangka awal OthelloBoard (__init__, reset_board, is_within_bounds).
* **Tahap 2B:** Menyelesaikan metode logika inti OthelloBoard (get_flippable_pieces, get_valid_moves, get_scores, place_piece, get_winner).
* **Tahap 3**: Membangun modul penyimpanan file JSON di src/storage.py.
* **Tahap 4:** Menulis & menjalankan unit test di tests/test_game_logic.py hingga semua lulus (OK).
* **Tahap 5:** Membangun tampilan grafis Tkinter di src/main_ui.py dan menghubungkannya dengan logika serta storage.
* **Tahap 6:** Uji coba bermain berdua (playtesting), debugging, melengkapi komentar & README.md, lalu merekam video demonstrasi.