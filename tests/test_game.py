"""Tests for Game class."""

import pytest
from src.game import Game
from src.player import Player
from src.card import Card, Suit, Rank


class TestGame:
    """Test suite for Game class."""
    
    def test_game_creation(self):
        """Test creating a game."""
        game = Game(["Alice", "Bob", "Charlie"], 3)
        
        assert len(game.players) == 3
        assert game.total_rounds == 3
        assert game.current_round == 0
        assert game.players[0].name == "Alice"
        assert game.players[1].name == "Bob"
        assert game.players[2].name == "Charlie"
    
    def test_game_creation_invalid_players(self):
        """Test that invalid player count raises error."""
        with pytest.raises(ValueError, match="between 3 and 8"):
            Game(["Alice", "Bob"], 3)
        
        with pytest.raises(ValueError, match="between 3 and 8"):
            Game(["P1", "P2", "P3", "P4", "P5", "P6", "P7", "P8", "P9"], 3)
    
    def test_game_creation_invalid_rounds(self):
        """Test that invalid rounds raises error."""
        with pytest.raises(ValueError, match="at least 1 round"):
            Game(["Alice", "Bob", "Charlie"], 0)
    
    def test_setup_round(self):
        """Test setting up a round."""
        game = Game(["Alice", "Bob", "Charlie"], 3)
        game.setup_round()
        
        # All players should have cards
        for player in game.players:
            assert len(player.hand) > 0
        
        # Total cards should be 52
        total_cards = sum(len(p.hand) for p in game.players)
        assert total_cards == 52
    
    def test_find_starting_player(self):
        """Test finding player with 3 of clubs."""
        game = Game(["Alice", "Bob", "Charlie"], 3)
        game.setup_round()
        
        starting_player = game.find_starting_player()
        assert starting_player.has_three_of_clubs()
    
    def test_assign_ranks_three_players(self):
        """Test rank assignment with 3 players."""
        game = Game(["Alice", "Bob", "Charlie"], 1)
        
        # Simulate finish order
        game.finished_players = [
            game.players[0],  # Alice - President
            game.players[1],  # Bob - Neutral
            game.players[2]   # Charlie - Scum
        ]
        
        game.assign_ranks()
        
        assert game.players[0].rank == "President"
        assert game.players[1].rank == "Neutral"
        assert game.players[2].rank == "Scum"
    
    def test_assign_ranks_four_players(self):
        """Test rank assignment with 4 players."""
        game = Game(["Alice", "Bob", "Charlie", "Dave"], 1)
        
        # Simulate finish order
        game.finished_players = [
            game.players[0],  # Alice - President
            game.players[1],  # Bob - Vice-President
            game.players[2],  # Charlie - Vice-Scum
            game.players[3]   # Dave - Scum
        ]
        
        game.assign_ranks()
        
        assert game.players[0].rank == "President"
        assert game.players[1].rank == "Vice-President"
        assert game.players[2].rank == "Vice-Scum"
        assert game.players[3].rank == "Scum"
    
    def test_calculate_scores_regular_round(self):
        """Test score calculation for regular round."""
        game = Game(["Alice", "Bob", "Charlie"], 3)
        game.current_round = 1
        
        # Alice wins
        game.finished_players = [game.players[0], game.players[1], game.players[2]]
        game.assign_ranks()
        game.calculate_scores(False)
        
        assert game.players[0].score == 1
        assert game.players[1].score == 0
        assert game.players[2].score == 0
    
    def test_calculate_scores_final_round(self):
        """Test score calculation for final round."""
        game = Game(["Alice", "Bob", "Charlie"], 5)
        game.current_round = 5
        
        # Alice wins final round
        game.finished_players = [game.players[0], game.players[1], game.players[2]]
        game.assign_ranks()
        game.calculate_scores(True)
        
        # Final round bonus: max(2, 5-2) = 3
        assert game.players[0].score == 3
    
    def test_calculate_scores_final_round_low_rounds(self):
        """Test final round score with low round count."""
        game = Game(["Alice", "Bob", "Charlie"], 2)
        game.current_round = 2
        
        game.finished_players = [game.players[0], game.players[1], game.players[2]]
        game.assign_ranks()
        game.calculate_scores(True)
        
        # Final round bonus: max(2, 2-2) = 2
        assert game.players[0].score == 2
    
    def test_get_active_players(self):
        """Test getting active players."""
        game = Game(["Alice", "Bob", "Charlie"], 1)
        game.setup_round()
        
        # All players have cards initially
        active = game.get_active_players()
        assert len(active) == 3
        
        # Remove all cards from one player
        game.players[0].hand = []
        active = game.get_active_players()
        assert len(active) == 2
    
    def test_get_winner_clear(self):
        """Test getting winner with clear winner."""
        game = Game(["Alice", "Bob", "Charlie"], 1)
        
        game.players[0].score = 5
        game.players[1].score = 2
        game.players[2].score = 1
        
        winner = game.get_winner()
        assert winner == game.players[0]
    
    def test_get_winner_tie(self):
        """Test getting winner with tie."""
        game = Game(["Alice", "Bob", "Charlie"], 1)
        
        game.players[0].score = 3
        game.players[1].score = 3
        game.players[2].score = 1
        
        winner = game.get_winner()
        assert winner is None  # Tie
    
    def test_get_scores(self):
        """Test getting sorted scores."""
        game = Game(["Alice", "Bob", "Charlie"], 1)
        
        game.players[0].score = 2
        game.players[1].score = 5
        game.players[2].score = 1
        
        scores = game.get_scores()
        
        assert len(scores) == 3
        assert scores[0][0].name == "Bob"
        assert scores[0][1] == 5
        assert scores[1][0].name == "Alice"
        assert scores[1][1] == 2
        assert scores[2][0].name == "Charlie"
        assert scores[2][1] == 1
    
    def test_handle_card_exchange_three_players(self):
        """Test card exchange with 3 players (President and Scum only)."""
        game = Game(["Alice", "Bob", "Charlie"], 2)
        
        # Set up ranks
        game.players[0].rank = "President"
        game.players[1].rank = "Neutral"
        game.players[2].rank = "Scum"
        
        # Give them cards
        for player in game.players:
            player.add_cards([
                Card(Suit.SPADES, Rank.THREE),
                Card(Suit.HEARTS, Rank.FIVE),
                Card(Suit.CLUBS, Rank.KING),
                Card(Suit.DIAMONDS, Rank.ACE)
            ])
        
        initial_pres_count = len(game.players[0].hand)
        initial_scum_count = len(game.players[2].hand)
        
        game.handle_card_exchange()
        
        # Card counts should stay same (2 given, 2 received)
        assert len(game.players[0].hand) == initial_pres_count
        assert len(game.players[2].hand) == initial_scum_count
    
    def test_handle_card_exchange_four_players(self):
        """Test card exchange with 4 players (includes Vice ranks)."""
        game = Game(["Alice", "Bob", "Charlie", "Dave"], 2)
        
        # Set up ranks
        game.players[0].rank = "President"
        game.players[1].rank = "Vice-President"
        game.players[2].rank = "Vice-Scum"
        game.players[3].rank = "Scum"
        
        # Give them cards
        for player in game.players:
            player.add_cards([
                Card(Suit.SPADES, Rank.THREE),
                Card(Suit.HEARTS, Rank.FIVE),
                Card(Suit.CLUBS, Rank.KING),
                Card(Suit.DIAMONDS, Rank.ACE),
                Card(Suit.SPADES, Rank.FOUR)
            ])
        
        game.handle_card_exchange()
        
        # All should still have 5 cards (gave and received)
        assert len(game.players[0].hand) == 5
        assert len(game.players[1].hand) == 5
        assert len(game.players[2].hand) == 5
        assert len(game.players[3].hand) == 5
    
    def test_game_str(self):
        """Test string representation of game."""
        game = Game(["Alice", "Bob", "Charlie"], 5)
        game.current_round = 2
        
        game_str = str(game)
        assert "round 2/5" in game_str
        assert "3 players" in game_str
    
    def test_game_repr(self):
        """Test developer representation of game."""
        game = Game(["Alice", "Bob", "Charlie"], 5)
        game.current_round = 2
        
        repr_str = repr(game)
        assert "players=3" in repr_str
        assert "rounds=2/5" in repr_str


class TestGameIntegration:
    """Integration tests for Game class."""
    
    def test_complete_round(self):
        """Test playing a complete round."""
        game = Game(["Alice", "Bob", "Charlie"], 1)
        game.play_round()
        
        # Round should be complete
        assert game.current_round == 1
        
        # Should have finished players
        assert len(game.finished_players) > 0
        
        # President should have points (2 for final round of 1-round game: max(2, 1-2) = 2)
        president = game.finished_players[0]
        assert president.score == 2
        
        # Ranks should be assigned
        assert president.rank == "President"
        assert game.finished_players[-1].rank == "Scum"
    
    def test_complete_game_three_rounds(self):
        """Test playing a complete game with 3 rounds."""
        game = Game(["Alice", "Bob", "Charlie", "Dave"], 3)
        winner = game.play_game()
        
        # Game should be complete
        assert game.current_round == 3
        
        # Winner should have highest score
        assert winner.score >= 1
        
        # All players should have played
        for player in game.players:
            assert player.rank is not None
    
    def test_card_exchange_between_rounds(self):
        """Test that card exchange happens between rounds."""
        game = Game(["Alice", "Bob", "Charlie"], 2)
        
        # Play first round
        game.play_round()
        
        # Note the ranks
        president = None
        scum = None
        for player in game.players:
            if player.rank == "President":
                president = player
            elif player.rank == "Scum":
                scum = player
        
        assert president is not None
        assert scum is not None
        
        # Play second round (should do card exchange)
        game.play_round()
        
        # Round completed successfully (exchange didn't break anything)
        assert game.current_round == 2
    
    def test_final_round_bonus(self):
        """Test that final round gives bonus points."""
        game = Game(["Alice", "Bob", "Charlie"], 5)
        
        # Play all 5 rounds
        winner = game.play_game()
        
        # Winner should have some points
        assert winner.score >= 2
    
    def test_multiple_round_scoring(self):
        """Test scoring across multiple rounds."""
        game = Game(["Alice", "Bob", "Charlie"], 3)
        
        # Manually play rounds to control who wins
        for i in range(3):
            game.play_round()
        
        # At least one player should have points
        total_score = sum(p.score for p in game.players)
        assert total_score > 0
    
    def test_four_player_vice_ranks(self):
        """Test that vice ranks are assigned with 4 players."""
        game = Game(["Alice", "Bob", "Charlie", "Dave"], 1)
        game.play_round()
        
        # Check that we have all ranks
        ranks = [p.rank for p in game.finished_players]
        assert "President" in ranks
        assert "Vice-President" in ranks
        assert "Vice-Scum" in ranks
        assert "Scum" in ranks
    
    def test_three_player_no_vice_ranks(self):
        """Test that vice ranks are NOT assigned with 3 players."""
        game = Game(["Alice", "Bob", "Charlie"], 1)
        game.play_round()
        
        ranks = [p.rank for p in game.finished_players]
        assert "President" in ranks
        assert "Scum" in ranks
        assert "Vice-President" not in ranks
        assert "Vice-Scum" not in ranks
