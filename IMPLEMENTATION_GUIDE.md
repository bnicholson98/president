# Implementation Guide

This guide provides step-by-step instructions for implementing the President card game in Python.

## Phase 1: Project Setup

### Step 1.1: Initialize Project Structure

Create the following directory structure:

```
president/
├── src/
│   └── __init__.py
├── tests/
│   └── __init__.py
├── main.py
├── requirements.txt
├── README.md
├── IMPLEMENTATION_GUIDE.md
└── .gitignore
```

### Step 1.2: Create requirements.txt

```txt
rich>=13.0.0
pytest>=7.0.0
pytest-cov>=4.0.0
```

### Step 1.3: Create .gitignore

```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/
*.egg-info/
dist/
build/

# Testing
.pytest_cache/
.coverage
htmlcov/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db
```

## Phase 2: Core Data Structures

### Step 2.1: Implement Card Class (src/card.py)

**Requirements:**
- Define `Suit` enum: CLUBS, DIAMONDS, HEARTS, SPADES
- Define `Rank` enum: THREE through ACE, plus TWO
- Implement `Card` class:
  - Properties: `suit`, `rank`
  - Method: `__str__()` for display
  - Method: `__repr__()` for debugging
  - Method: `__eq__()` and `__hash__()` for comparisons
  - Method: `get_value()` returns numeric value for comparison (3=0, 4=1, ..., A=11, 2=12)
  - Method: `is_three_of_spades()` checks if card is 3♠

**Special Considerations:**
- 3 of spades is special - highest when played as single
- 2 is higher than Ace

### Step 2.2: Implement Deck Class (src/card.py)

**Requirements:**
- Initialize with standard 52-card deck
- Method: `shuffle()` randomizes deck
- Method: `deal(num_players)` returns list of hands (each hand is a list of Cards)
  - Deals one card at a time to each player in rotation
  - Handles uneven distribution (some players may have one more card)

**Tests to Write (tests/test_card.py):**
- Test card creation and properties
- Test card value comparisons
- Test 3 of spades identification
- Test deck initialization (52 cards)
- Test deck shuffling (order changes)
- Test dealing to different numbers of players (3-8)
- Test deal distribution is fair

## Phase 3: Player Management

### Step 3.1: Implement Player Class (src/player.py)

**Requirements:**
- Properties:
  - `name`: string
  - `hand`: list of Cards
  - `score`: integer (total points)
  - `rank`: string or enum (President, Vice-President, Neutral, Vice-Scum, Scum, or None)
  - `has_passed`: boolean (for current trick)
- Methods:
  - `add_cards(cards)`: adds cards to hand
  - `remove_cards(cards)`: removes cards from hand
  - `sort_hand()`: sorts hand by card value
  - `has_three_of_clubs()`: returns True if player has 3♣
  - `get_valid_plays(current_play)`: returns list of valid card combinations
    - If no current_play, return all possible plays from hand
    - If current_play exists, return only plays that beat it
  - `choose_cards_to_give(num)`: for card exchange (returns strongest cards for Scum)
  - `is_hand_empty()`: returns True if no cards left

**Tests to Write (tests/test_player.py):**
- Test player creation
- Test adding/removing cards
- Test hand sorting
- Test 3 of clubs detection
- Test valid play generation (singles, pairs, triples, etc.)
- Test valid plays against current play
- Test card selection for exchange

## Phase 4: Trick Logic

### Step 4.1: Implement Play Class (src/trick.py)

**Requirements:**
- Represents a set of cards played together
- Properties:
  - `cards`: list of Cards
  - `player`: Player who played
  - `num_cards`: number of cards in play
  - `rank`: rank of cards (all cards must be same rank)
- Methods:
  - `beats(other_play)`: returns True if this play beats other_play
    - Must have same number of cards
    - Must have higher rank value
    - Special case: single 3 of spades beats everything
  - `is_valid()`: checks all cards are same rank

### Step 4.2: Implement Trick Class (src/trick.py)

**Requirements:**
- Manages a single trick (round of plays until someone wins)
- Properties:
  - `plays`: list of Play objects
  - `current_play`: the Play to beat (or None)
  - `active_players`: players who haven't passed yet
- Methods:
  - `add_play(play)`: adds a play to the trick
  - `can_play(player, cards)`: validates if player can play these cards
  - `player_passes(player)`: marks player as passed for this trick
  - `is_complete()`: returns True if only one active player remains (or all passed)
  - `get_winner()`: returns Player who won the trick

**Tests to Write (tests/test_trick.py):**
- Test play creation and validation
- Test play comparisons (single vs single, pairs vs pairs, etc.)
- Test 3 of spades special rule
- Test trick initialization
- Test adding plays to trick
- Test player passing
- Test trick completion detection
- Test winner determination

## Phase 5: Game Logic

### Step 5.1: Implement Game Class (src/game.py)

**Requirements:**
- Properties:
  - `players`: list of Players
  - `current_round`: integer
  - `total_rounds`: integer
  - `deck`: Deck
  - `current_trick`: Trick or None
  - `finished_players`: list of Players who finished this round (in order)
- Methods:
  - `setup_round()`: deals cards, performs card exchanges if not first round
  - `find_starting_player()`: returns player with 3♣
  - `play_trick()`: manages one complete trick
  - `handle_card_exchange()`: 
    - Scum gives 2 best cards to President
    - President gives 2 any cards to Scum
    - Vice-Scum gives 1 best card to Vice-President
    - Vice-President gives 1 any card to Vice-Scum
  - `play_round()`: manages one complete round until one player remains
  - `assign_ranks()`: assigns President, VP, VS, Scum based on finish order
  - `calculate_scores(is_final_round)`: awards points based on ranks
  - `play_game()`: main game loop for all rounds
  - `get_winner()`: returns player with highest score

**Rank Assignment Logic:**
- First to finish: President (1 point)
- Last with cards: Scum
- With 4+ players:
  - Second to finish: Vice-President
  - Second-to-last: Vice-Scum
- With 3 players: Only President and Scum (no Vice roles)
- Final round winner gets max(2, N-2) points instead of 1

**Tests to Write (tests/test_game.py):**
- Test game initialization with different player counts
- Test starting player identification
- Test card exchange logic
- Test rank assignment (3, 4, 5+ players)
- Test scoring (regular rounds and final round)
- Test complete round simulation
- Test complete game simulation
- Test edge cases (player winning multiple rounds, ties, etc.)

## Phase 6: User Interface

### Step 6.1: Implement UI Module (src/ui.py)

**Requirements:**
Using the `rich` library, create functions for:

- `display_welcome()`: Shows game title and rules summary
- `get_game_setup()`: Prompts for number of players and rounds
- `get_player_names(num_players)`: Prompts for each player name
- `display_hand(player)`: Shows player's current hand with nice formatting
  - Use `rich.table.Table` for card display
  - Group by rank or suit
  - Highlight special cards (2s, 3♠)
- `display_trick_state(trick)`: Shows current trick plays
- `display_rankings(players)`: Shows current social rankings
- `display_scores(players)`: Shows score table
- `get_player_action()`: Prompts player to play cards or pass
  - Return: 'pass' or list of card indices
- `display_play(player, cards)`: Announces a play
- `display_trick_winner(player)`: Announces trick winner
- `display_round_results(finished_players)`: Shows finish order
- `display_game_winner(player)`: Shows final winner with fanfare
- `display_error(message)`: Shows error messages
- `confirm_continue()`: Prompts to continue to next round

**UI Design Guidelines:**
- Use `rich.console.Console` for all output
- Use colors to distinguish:
  - Suits (red for hearts/diamonds, white for clubs/spades)
  - Player statuses (gold for President, gray for Scum, etc.)
  - Actions (green for valid, red for errors)
- Use `rich.panel.Panel` for important announcements
- Use `rich.prompt.Prompt` for user input
- Use `rich.progress.track` for any loading operations
- Clear screen between major phases for readability

### Step 6.2: Implement Main Game Loop (main.py)

**Requirements:**
- Import all necessary modules
- Create main() function:
  1. Display welcome screen
  2. Get game setup (players, rounds)
  3. Create Player objects
  4. Create Game object
  5. Run game loop with UI integration
  6. Display final results
- Handle exceptions gracefully
- Allow replaying or exiting

**Structure:**
```python
def main():
    # Welcome and setup
    # Game initialization
    # Game loop (for each round)
        # Display round start
        # Play tricks until round complete
        # Display round results
        # Handle card exchange
    # Display final winner
    # Prompt for replay

if __name__ == "__main__":
    main()
```

## Phase 7: Testing

### Step 7.1: Write Comprehensive Tests

For each test file, ensure coverage of:
- **Happy path**: Normal gameplay scenarios
- **Edge cases**: 
  - Minimum/maximum players
  - All cards same rank
  - Single player with 3♠
  - Everyone passes
  - Player wins multiple rounds
- **Error handling**:
  - Invalid plays
  - Wrong number of cards
  - Mixed ranks in set
  - Playing after passing

### Step 7.2: Integration Tests

Create `tests/test_integration.py`:
- Test complete 3-player game
- Test complete 5-player game
- Test card exchange between rounds
- Test scoring across multiple rounds
- Test final round bonus scoring

### Step 7.3: Run Tests

```bash
pytest tests/ -v
pytest --cov=src tests/ --cov-report=html
```

## Phase 8: Polish and Refinement

### Step 8.1: Add AI Players (Optional Enhancement)

Create `src/ai_player.py`:
- Inherit from Player
- Implement basic strategy:
  - Lead with lowest cards
  - Beat current play with lowest possible cards
  - Pass if cards are too valuable
  - Save high cards (2s, A♠) for later

### Step 8.2: Add Game State Persistence (Optional Enhancement)

- Save/load game state to JSON
- Allow resuming interrupted games

### Step 8.3: Performance Optimization

- Profile code for bottlenecks
- Optimize card comparison operations
- Cache valid play calculations

### Step 8.4: Documentation

- Add docstrings to all classes and methods (Google or NumPy style)
- Add type hints throughout codebase
- Create usage examples in README

## Implementation Order Summary

**Recommended implementation order:**

1. **Week 1**: Phase 1-2 (Setup, Card/Deck)
2. **Week 2**: Phase 3 (Player management)
3. **Week 3**: Phase 4 (Trick logic)
4. **Week 4**: Phase 5 (Game logic)
5. **Week 5**: Phase 6 (UI)
6. **Week 6**: Phase 7 (Testing)
7. **Week 7**: Phase 8 (Polish)

Each phase should follow TDD (Test-Driven Development):
1. Write tests first
2. Run tests (they should fail)
3. Implement code
4. Run tests (they should pass)
5. Refactor
6. Repeat

## Key Design Decisions

### Card Comparison

The card ranking system should use numeric values:
```python
3=0, 4=1, 5=2, 6=3, 7=4, 8=5, 9=6, 10=7, J=8, Q=9, K=10, A=11, 2=12
```

Special case for 3♠: Check separately when comparing single cards.

### Play Validation

A play beats another if:
1. Same number of cards
2. Higher rank value
3. OR single 3 of spades vs anything

### Card Exchange

Exchange happens before dealing new round. Order:
1. Collect cards from all players
2. Perform exchanges based on previous round ranks
3. Deal new hands
4. Find player with 3♣ to start

### State Management

Keep game state immutable where possible. Create new objects rather than modifying existing ones for easier testing and debugging.

## Common Pitfalls to Avoid

1. **Don't forget**: Player who won previous trick leads next trick
2. **Don't forget**: 3♠ is only special as a single card
3. **Don't forget**: Players can pass even with valid plays
4. **Don't forget**: Passed players can't play again in same trick
5. **Don't forget**: Card exchange happens BEFORE dealing next round
6. **Don't forget**: Final round scoring is different
7. **Don't forget**: With 3 players, there are no Vice roles

## Debugging Tips

- Add verbose logging mode to trace game state
- Use rich.print() for debugging complex data structures
- Test with small decks (e.g., only face cards) for faster iterations
- Create helper functions to set up specific game states for testing
- Use pytest fixtures for common test scenarios

## Success Criteria

The implementation is complete when:
- ✅ All tests pass with >90% coverage
- ✅ Game runs without crashes
- ✅ All rules are correctly implemented
- ✅ UI is clear and easy to use
- ✅ Code is well-documented
- ✅ Edge cases are handled gracefully
