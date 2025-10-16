# President Card Game

A Python terminal-based implementation of the classic President card game (also known as Scum, Capitalism, or Rich Man Poor Man).

## About

President is a trick-taking card game for 3-8 players where the objective is to be the first player to get rid of all your cards. Players compete across multiple rounds, with special card exchanges between rounds based on social rankings earned in the previous round.

## Game Overview

- **Type**: Trick-taking card game
- **Players**: 3-8
- **Deck**: Standard 52-card deck
- **Duration**: Multiple rounds until a winner is determined

## Game Rules

### Setup

All 52 cards are dealt randomly to players. Players may receive different numbers of cards depending on the total number of players.

### Starting the Game

The player holding the **3 of clubs** must start the first round by leading with it (either as a single card or as part of a set of 3s).

### Card Rankings

- **3** is the lowest rank
- **4-10, J, Q, K, A** follow in ascending order
- **Ace** is high
- **2** is even higher than Ace
- **3 of spades** is the highest card in the game (but only when played as a single card)

### Gameplay

1. The starting player leads by playing any single card or any set of cards of equal rank (e.g., three 5s)
2. Each subsequent player must either:
   - **Pass** (choose not to play), OR
   - **Play** a card or set that beats the previous play

3. **Beating plays**:
   - A single card beats a single card if it's higher in rank
   - A set of cards can only be beaten by a higher-ranked set with the **same number of cards**
   - Example: Two 6s can be beaten by two 7s or two Kings, but NOT by a single King or three 7s

4. **Passing**:
   - You may pass even if you have cards that could beat the current play
   - Once you pass, you cannot play again until the current trick is complete

5. **Winning a trick**:
   - Play continues around the table until someone plays and all other active players pass
   - The player who played the highest set wins the trick
   - All played cards are set aside face down
   - The winner leads the next trick with any card or set

6. **Round completion**:
   - The first player to run out of cards becomes the **President**
   - Play continues until only one player has cards remaining
   - The last player with cards becomes the **Scum**
   - With 4+ players, the second-to-last finisher is the **Vice-Scum** and second finisher is the **Vice-President**

### Between Rounds

Before the next round begins, players exchange cards based on their rankings:

- **Scum** gives their 2 strongest cards to the **President**
- **President** chooses any 2 cards to give back to the **Scum**
- **Vice-Scum** gives their 1 strongest card to the **Vice-President** (4+ players only)
- **Vice-President** chooses any 1 card to give back to the **Vice-Scum** (4+ players only)

After the exchange, cards are dealt for the next round, and the player with the 3 of clubs starts again.

### Scoring

- Players earn **1 point** for winning a round (becoming President)
- The player who wins the **Nth round** (final round) earns **max(2, N-2)** points
- The player with the most points at the end of all rounds wins the game

## Requirements

- Python 3.8+
- `rich` library for terminal UI
- `pytest` for testing

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd president

# Create a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

```bash
# Run the game
python main.py

# Run tests
pytest
```

## Project Structure

```
president/
├── README.md
├── IMPLEMENTATION_GUIDE.md
├── requirements.txt
├── main.py
├── src/
│   ├── __init__.py
│   ├── card.py
│   ├── deck.py
│   ├── player.py
│   ├── game.py
│   └── ui.py
└── tests/
    ├── __init__.py
    ├── test_card.py
    ├── test_deck.py
    ├── test_player.py
    └── test_game.py
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

[Choose your license]

## Acknowledgments

President is a classic card game with many variations played around the world.
