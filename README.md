# Othello (Reversi) — Python GUI Game

A modular desktop implementation of the classic board game **Othello (Reversi)** built in Python using `tkinter` for the graphical user interface, JSON for persistent match history, and `unittest` for automated game-logic verification.

## Features

- **Full Othello Rule Engine:** Validates legal moves across all 8 directions (horizontal, vertical, and diagonal), automatically flips outflanked opponent discs, handles automatic turn passing when a player has no valid moves, and detects end-game conditions.
- **Interactive `tkinter` GUI:** Features an 8x8 game board, real-time turn and score tracking, and a **New Game** reset control.
- **Toggleable Move Hints (`HINT: ON/OFF`):** Displays subtle visual indicators on valid squares (inspired by Chess.com) that can be toggled on or off mid-game.
- **Persistent Match History & Reset:** Automatically records completed match timestamps, scores, and winners into `data/scores.json`, viewable in a dedicated **Match History** window with an option to clear saved records.
- **Automated Unit Testing:** Includes a test suite covering initial board setup, valid move detection, disc flipping, custom exceptions, and JSON storage operations.

## Requirements

* **Python 3.8+** (uses only Python standard library modules: tkinter, json, os, datetime, and unittest — no external third-party packages required).

## How to Run

1. **Clone the repository:**
```bash
    git clone https://github.com/Manufah/othello-capstone.git
    cd othello-capstone
```

2. **Launch the game:**
```bash
python main.py
```

## Running Unit Tests

**To run the full test suite from the project root directory:**
```bash
python -m unittest discover -s tests -v
```

**To run a specific test case:**
```bash
python -m unittest tests.test_game_logic.TestOthelloLogic.test_place_piece_and_flip
```

## How to Play
1. **Black** moves first.

2. Click on an empty square that outflanks one or more opposing discs in a straight line (horizontally, vertically, or diagonally). All trapped opponent discs along those lines flip to your color.

3. Click HINT: OFF / HINT: ON at the bottom of the window to toggle visual hints for valid moves.

4. If a player has no legal moves available, the turn automatically passes to the opponent.

5. The game ends when neither player can make a valid move, and the player with the majority of discs on the board wins.