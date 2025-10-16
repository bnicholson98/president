# Implementation Guide

This guide provides step-by-step instructions for implementing the President card game in Python.

## Technology Stack

- **Language**: Python 3.8+
- **UI Library**: `rich` - for terminal-based UI with colors, tables, and formatting
- **Testing**: `pytest` - for unit and integration tests
- **Additional Libraries**: Standard library modules as needed

## Development Setup

### 1. Initialize Project Structure

Create the following directory structure:

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

### 2. Create Requirements File

Create `requirements.txt` with:
```
rich>=13.0.0
pytest>=7.0.0
```

## Implementation Steps

### Phase 1: Core Data Models

#### Step 1.1: Implement Card Class (`src/card.py`)

Create a `Card` class with:
- **Attributes**:
  - `rank`: Card rank (3-10, J, Q, K, A, 2)
  - `suit`: Card suit (Clubs, Diamonds, Hearts, Spades)
  
- **Methods**:
  - `__init__(rank, suit)`: Constructor
  - `__str__()`: String representation (e.g., "3♣", "A♠")
  - `__repr__()`: Object representation
  - `__eq__()`: Equality comparison
  - `__hash__()`: Make cards hashable
  - `get_value()`: Returns numerical value for comparison (3=0, 4=1, ..., A=11, 2=12, 3♠=13)
  - `is_three_of_spades()`: Check if card is the special 3 of spades
  - `is_three_of_clubs()`: Check if card is the starting card

**Special Considerations**:
- Handle the special case where 3♠ is highest when played as single
- Rank ordering: 3 < 4 < 5 < 6 < 7 < 8 < 9 < 10 < J < Q < K < A < 2 < 3♠ (single only)

**Tests to Write** (`tests/test_card.py`):
- Test card creation
- Test card comparison
- Test special card identification (3♣, 3♠)
- Test card value calculation
- Test string representations

---

#### Step 1.2: Implement Deck Class (`src/deck.py`)

Create a `Deck` class with:
- **Attributes**:
  - `cards`: List of Card objects

- **Methods**:
  - `__init__()`: Creates a standard 52-card deck
  - `shuffle()`: Randomizes card order
  - `deal(num_players)`: Deals all cards to specified number of players, returns list of hands
  - `__len__()`: Returns number of cards remaining

**Implementation Notes**:
- Use `random.shuffle()` for shuffling
- Deal cards as evenly as possible (some players may get one extra card)

**Tests to Write** (`tests/test_deck.py`):
- Test deck initialization (52 cards)
- Test deck contains all unique cards
- Test shuffle changes order
- Test dealing distributes all cards
- Test dealing with different player counts (3-8)

---

### Phase 2: Player and Game Logic

#### Step 2.1: Implement Player Class (`src/player.py`)

Create a `Player` class with:
- **Attributes**:
  - `name`: Player name
  - `hand`: List of cards in hand
  - `rank`: Current social rank (President, Vice-President, Neutral, Vice-Scum, Scum)
  - `score`: Total points accumulated
  - `is_human`: Boolean indicating if human or AI player
  - `has_passed`: Boolean for current trick
  
- **Methods**:
  - `__init__(name, is_human=False)`: Constructor
  - `add_cards(cards)`: Add cards to hand
  - `remove_cards(cards)`: Remove cards from hand
  - `sort_hand()`: Sort hand by card value
  - `has_card(card)`: Check if player has specific card
  - `get_valid_plays(current_play)`: Returns list of valid plays given current play
  - `has_three_of_clubs()`: Check if player has 3♣
  - `choose_play(current_play, trick_history)`: AI or human play selection
  - `choose_starting_play()`: Special method for starting with 3♣
  - `select_cards_to_give(count)`: Select strongest cards for exchange
  - `__str__()`: String representation

**Implementation Notes**:
- AI logic can start simple (play lowest valid cards, pass when no good options)
- Valid plays must match the number of cards in current play and be higher rank
- Sort hand for easier display and play selection

**Tests to Write** (`tests/test_player.py`):
- Test player initialization
- Test adding/removing cards
- Test hand sorting
- Test valid play detection
- Test three of clubs detection
- Test card selection logic

---

#### Step 2.2: Implement Game Class (`src/game.py`)

Create a `Game` class with:
- **Attributes**:
  - `players`: List of Player objects
  - `current_round`: Current round number
  - `current_trick`: List of plays in current trick
  - `current_player_idx`: Index of current player
  - `active_players`: Set of players who haven't passed this trick
  - `finished_order`: List tracking order players finished
  - `round_winner`: Player who won current round
  
- **Methods**:
  - `__init__(num_players, num_humans=1)`: Initialize game
  - `setup_round()`: Deal cards and prepare for new round
  - `start_round()`: Begin round, handle 3♣ starting requirement
  - `play_trick()`: Execute one complete trick
  - `process_play(player, cards)`: Validate and process a player's play
  - `is_valid_play(cards, current_play)`: Validate if play is legal
  - `complete_trick()`: End trick, determine winner, reset for next
  - `check_round_end()`: Check if round is over (all but one player finished)
  - `exchange_cards()`: Handle between-round card exchanges
  - `calculate_scores()`: Award points based on rankings
  - `is_game_over()`: Determine if game should end
  - `get_winner()`: Return player with highest score
  - `run()`: Main game loop

**Game Flow**:
1. Initialize players
2. For each round:
   - Deal cards
   - Exchange cards (after round 1)
   - Play tricks until round ends
   - Assign rankings
   - Calculate scores
3. Determine winner

**Special Logic**:
- Track which players have passed in current trick
- Reset pass status when trick completes
- Handle 3♠ as highest single card only
- Enforce 3♣ as starting play of first round

**Tests to Write** (`tests/test_game.py`):
- Test game initialization
- Test round setup
- Test valid play validation
- Test trick completion
- Test round completion and ranking
- Test card exchange logic
- Test score calculation
- Test game end conditions

---

### Phase 3: User Interface

#### Step 3.1: Implement UI Class (`src/ui.py`)

Create a `UI` class using `rich` library with:
- **Methods**:
  - `display_welcome()`: Show game title and instructions
  - `get_game_settings()`: Prompt for number of players
  - `display_game_state(game)`: Show current game state (scores, round number)
  - `display_player_hand(player)`: Show player's cards in a formatted way
  - `display_current_trick(trick)`: Show cards played in current trick
  - `display_valid_plays(valid_plays)`: Show available play options
  - `get_player_choice(valid_plays)`: Get input from human player
  - `display_play(player, cards)`: Announce a player's move
  - `display_pass(player)`: Announce a player passed
  - `display_trick_winner(player)`: Announce trick winner
  - `display_round_results(rankings)`: Show round end results
  - `display_card_exchange(exchanges)`: Show between-round exchanges
  - `display_final_scores(players)`: Show final game results
  - `display_winner(player)`: Announce game winner
  - `confirm_continue()`: Ask if player wants to play another game

**Rich Library Features to Use**:
- `Console` for formatted output
- `Table` for displaying scores and rankings
- `Panel` for important information
- `Prompt` for user input
- Color coding (e.g., red for hearts/diamonds, black for clubs/spades)
- `Style` for emphasis and readability

**Implementation Notes**:
- Make the interface clear and easy to read
- Use colors to distinguish suits
- Number valid plays for easy selection
- Clear screen between turns (optional, for cleaner experience)
- Show helpful context (what beats what, who's winning, etc.)

**Tests to Write** (`tests/test_ui.py`):
- Test output formatting (check string output)
- Test input parsing
- Mock user inputs for testing interactive elements

---

### Phase 4: Main Application

#### Step 4.1: Implement Main Entry Point (`main.py`)

Create the main application with:
```python
def main():
    """Main entry point for the President card game."""
    # Initialize UI
    # Get game settings
    # Create and run game
    # Display results
    # Ask to play again
    pass

if __name__ == "__main__":
    main()
```

**Implementation Flow**:
1. Display welcome screen
2. Get number of players and human players
3. Create Game instance
4. Run game with UI integration
5. Display final results
6. Option to play again

---

### Phase 5: Testing and Refinement

#### Step 5.1: Write Comprehensive Tests

For each test file:
- Use `pytest` fixtures for common setup
- Test edge cases (e.g., single player with 3♣, all players pass except one)
- Test special card behaviors
- Test score calculations for various round numbers
- Test card exchange with different player counts

#### Step 5.2: AI Improvements (Optional Enhancement)

Implement smarter AI strategies:
- **Defensive play**: Pass on weak hands when not leading
- **Aggressive play**: Play strong cards when likely to win
- **Card counting**: Track what's been played
- **Social ranking awareness**: Presidents play more aggressively
- **Set management**: Keep strong sets together

#### Step 5.3: Additional Features (Optional)

Consider implementing:
- **Game variants**: Different rule sets (Revolution, Jokers, etc.)
- **Statistics tracking**: Win rates, average scores
- **Saved games**: Pause and resume functionality
- **Replay system**: Review previous hands
- **Difficulty levels**: Easy/Medium/Hard AI
- **Network play**: Multiplayer over network

---

## Implementation Order Recommendation

1. **Start with Card and Deck** - These are foundational and easiest to test
2. **Implement Player** - Build on Card/Deck, test hand management
3. **Build Game Logic** - Most complex, but now you have building blocks
4. **Create UI** - Can test game logic independently before adding UI
5. **Integrate with Main** - Bring everything together
6. **Comprehensive Testing** - Ensure all edge cases work
7. **Polish and Refine** - Improve AI, add features, enhance UX

---

## Testing Strategy

### Unit Tests
- Test each class in isolation
- Mock dependencies where needed
- Aim for >80% code coverage

### Integration Tests
- Test complete game flows
- Test multi-round games
- Test all player count variations (3-8)

### Manual Testing
- Play complete games
- Test edge cases that are hard to automate
- Verify UI/UX quality

---

## Debug and Development Tips

1. **Logging**: Add logging for game state changes to help debug
2. **Verbose Mode**: Add a `--verbose` flag to show more game details
3. **Deterministic Testing**: Use fixed random seeds in tests
4. **Step-by-step Mode**: Allow stepping through AI moves for debugging
5. **Hand Inspection**: Add ability to see all hands when debugging

---

## Code Quality Guidelines

- Follow PEP 8 style guidelines
- Use type hints for function parameters and returns
- Write docstrings for all classes and public methods
- Keep functions focused and single-purpose
- Use meaningful variable names
- Comment complex logic
- Avoid magic numbers (use constants)

---

## Example Development Session

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run tests as you develop
pytest tests/test_card.py -v
pytest tests/ -v --cov=src

# Run the game
python main.py

# Run specific test
pytest tests/test_game.py::test_trick_completion -v
```

---

## Common Pitfalls to Avoid

1. **Forgetting 3♠ special rule**: Only highest when played as single
2. **Card exchange confusion**: President gives back ANY cards, not weakest
3. **Pass tracking**: Players who pass are out until trick ends
4. **Score calculation**: Final round uses special formula max(2, N-2)
5. **Set validation**: Must match exact count of cards in current play
6. **Round starting**: Only first round starts with 3♣

---

## Completion Checklist

- [ ] All core classes implemented (Card, Deck, Player, Game, UI)
- [ ] All unit tests passing
- [ ] Integration tests passing
- [ ] Game playable from start to finish
- [ ] All special rules implemented correctly (3♣ start, 3♠ highest single, exchanges)
- [ ] Score calculation working correctly
- [ ] UI is clear and user-friendly
- [ ] AI makes reasonable decisions
- [ ] Edge cases handled (ties, empty hands, etc.)
- [ ] Code documented and commented
- [ ] README updated with any changes

---

## Future Enhancements

After core implementation, consider:
- Save/load game state
- Game replay feature
- Statistics and achievements
- Tournament mode
- Custom rule sets
- Improved AI with difficulty levels
- Network multiplayer
- Web interface version
- Mobile app version

---

## Support and Resources

- **Rich Documentation**: https://rich.readthedocs.io/
- **Pytest Documentation**: https://docs.pytest.org/
- **Python Official Docs**: https://docs.python.org/3/

Good luck with your implementation! 🎴
