# President Card Game

A Python terminal-based implementation of the classic President card game for 3-8 players.

## Overview

President is a trick-taking card game where players compete to get rid of all their cards first. Players earn social rankings (President, Vice-President, Vice-Scum, Scum) based on their finishing order, which affects card exchanges in subsequent rounds. The game features strategic gameplay with passing, set matching, and special card hierarchies.

## Features

- 🎮 Terminal-based gameplay with rich text formatting
- 👥 Support for 3-8 players
- 🎴 Full card ranking system with special rules for 2s and 3 of spades
- 🏆 Round-based scoring system
- 🔄 Card exchange mechanics between rounds based on player rankings
- 📊 Score tracking across multiple rounds

## Requirements

- Python 3.8+
- `rich` library for terminal formatting
- `pytest` for testing

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd president
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the game:
```bash
python main.py
```

Run tests:
```bash
pytest
```

Run tests with coverage:
```bash
pytest --cov=src tests/
```

## Game Rules

### Setup

Starting to the dealer's left, deal one card at a time until all cards have been dealt.

### Starting the Game

The player holding the **3 of clubs** must start the first round by leading with it (either as a single card or as part of a set of 3s).

### Card Rankings

- **3** is the lowest rank
- Ranks follow in normal order: **3, 4, 5, 6, 7, 8, 9, 10, J, Q, K, A**
- **2** is higher than Ace
- **3 of spades** is the highest card, but only when played as a single

### Gameplay

1. **Leading**: The starting player leads by playing any single card or any set of cards of equal rank (e.g., three 5s)

2. **Playing or Passing**: Each subsequent player must either:
   - **Pass** (choose not to play), OR
   - **Play** a card or set that beats the previous play

3. **Beating Cards**:
   - A single card beats a single card if it's higher in rank
   - A set of cards can only be beaten by a higher-ranked set with the **same number of cards**
   - Example: Two 6s can be beaten by two 7s or two Kings, but NOT by a single King or three 7s

4. **Passing Strategy**: You may pass even if you have cards that could beat the current play. Once you pass, you cannot play again until the current trick is complete.

5. **Winning Tricks**: Play continues around the table until someone plays and all other active players pass. The player who played the highest set wins the trick. All played cards are set aside face down. The winner leads the next trick with any card or set.

6. **Finishing Order**: 
   - The first player to run out of cards becomes the **President**
   - Play continues until only one player has cards remaining
   - The last player with cards becomes the **Scum**
   - With 4+ players: second finisher is the **Vice-President**, second-to-last is the **Vice-Scum**

### Between Rounds

Before the next round begins, players exchange cards based on their rankings:

- **Scum** gives their 2 strongest cards to the **President**
- **President** chooses any 2 cards to give back to the **Scum**
- If there is a **Vice-President** and **Vice-Scum**, the same exchange happens but for 1 card

After the exchange, cards are dealt for the next round, and the player with the 3 of clubs starts again.

### Scoring

- Players earn **1 point** for winning a round (becoming President)
- The player who wins the final (Nth) round earns **max(2, N-2) points**
- The player with the **most points** at the end of all rounds wins the game

## Project Structure

```
president/
├── src/
│   ├── __init__.py
│   ├── card.py           # Card and Deck classes
│   ├── player.py         # Player class
│   ├── game.py           # Game logic
│   ├── trick.py          # Trick management
│   └── ui.py             # Rich UI components
├── tests/
│   ├── __init__.py
│   ├── test_card.py
│   ├── test_player.py
│   ├── test_game.py
│   └── test_trick.py
├── main.py               # Entry point
├── requirements.txt
├── README.md
├── IMPLEMENTATION_GUIDE.md
└── .gitignore
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Acknowledgments

President is a classic card game enjoyed worldwide under various names including Scum, Capitalism, and Butthead.
