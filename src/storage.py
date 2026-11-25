import json, os, datetime

# load history (membaca daftar riwayat pertandingan)
# menangani error terpisah
def load_history(filepath = "data/scores.json"):
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []


# mengambil riwayat lama lewat load_history(filepath)
# menambahkan dictionary hasil pertandingan (berisi: nama pemain, skor masing - masing, pemenang, waktu/tanggal)
# memastikan folder tersedia dan menyimpan riwayat baru ke file JSON
def save_match_result(player_black, player_white, score_black, score_white, winner, filepath = "data/scores.json"):
    history = load_history(filepath)

    new_record = {
        "player_black": player_black,
        "player_white": player_white,
        "score_black": int(score_black),
        "score_white": int(score_white),
        "winner": winner,
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    history.append(new_record)

    folder = os.path.dirname(filepath)
    if folder:
        os.makedirs(folder, exist_ok=True)

    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(history, file, indent=4)


# Menghapus seluruh isi riwayat pertandingan dengan menimpa file menjadi list kosong
def clear_history(filepath="data/scores.json"):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as file:
        json.dump([], file, indent=4)