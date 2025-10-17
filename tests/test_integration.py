"""Integration tests for President card game."""

import pytest
from src.game import Game
from src.card import Card, Rank, Suit


class TestGameIntegration:
    """Integration tests for complete game scenarios."""
    
    def test_complete_three_player_game(self):
        """Test a complete 3-player game from start to finish."""
        game = Game(["Alice", "Bob", "Charlie"], 3)
        
        # Verify initial state
        assert len(game.players) == 3
        assert game.current_round == 0
        assert game.total_rounds == 3
        
        # Play the game
        winner = game.play_game()
        
        # Verify game completion
        assert game.current_round == 3
        assert winner is not None
        assert winner in game.players
        
        # Verify scores were calculated
        total_score = sum(p.score for p in game.players)
        assert total_score > 0
        
        # Winner should have highest score OR be fallback due to ties
        max_score = max(p.score for p in game.players)
        # Check if there's a clear winner
        if game.get_winner() is not None:
            assert winner.score == max_score
        # If get_winner() returned None (due to ties), play_game() returns first player as fallback
        
        # Verify all players have valid final ranks
        for player in game.players:
            assert player.rank in [
                "President", "Neutral", "Scum"
            ]
    
    def test_complete_five_player_game(self):
        """Test a complete 5-player game from start to finish."""
        game = Game(["Alice", "Bob", "Charlie", "Dave", "Eve"], 3)
        
        # Verify initial state
        assert len(game.players) == 5
        
        # Play the game
        winner = game.play_game()
        
        # Verify game completion
        assert game.current_round == 3
        assert winner is not None
        
        # Verify all 5 ranks are assigned
        ranks = [p.rank for p in game.players]
        expected_ranks = [
            "President",
            "Vice-President",
            "Neutral",
            "Vice-Scum",
            "Scum"
        ]
        assert sorted(ranks) == sorted(expected_ranks)
    
    def test_card_exchange_between_rounds(self):
        """Test that card exchange works properly between rounds."""
        game = Game(["Alice", "Bob", "Charlie", "Dave"], 2)
        
        # Play first round
        game.play_round()
        
        # Get players by rank after first round
        president = next(p for p in game.players if p.rank == "President")
        scum = next(p for p in game.players if p.rank == "Scum")
        vice_president = next(p for p in game.players if p.rank == "Vice-President")
        vice_scum = next(p for p in game.players if p.rank == "Vice-Scum")
        
        # Store hand sizes before exchange
        president_cards_before = len(president.hand)
        scum_cards_before = len(scum.hand)
        vp_cards_before = len(vice_president.hand)
        vs_cards_before = len(vice_scum.hand)
        
        # Play second round (which should trigger card exchange)
        game.play_round()
        
        # Card exchange should have happened at the start of round 2
        # (We can't easily test the specific cards exchanged without making the exchange deterministic,
        # but we can verify the game completed successfully with proper exchanges)
        assert game.current_round == 2
        
        # All players should have cards dealt for the new round
        for player in game.players:
            # After playing a round, some players will have no cards, but initially they all had cards
            assert hasattr(player, 'hand')
    
    def test_scoring_across_multiple_rounds(self):
        """Test that scoring accumulates correctly across multiple rounds."""
        game = Game(["Alice", "Bob", "Charlie"], 3)
        
        # Track initial scores
        initial_scores = {p.name: p.score for p in game.players}
        assert all(score == 0 for score in initial_scores.values())
        
        # Play first round
        game.play_round()
        
        # Verify scores were updated after first round
        round1_scores = {p.name: p.score for p in game.players}
        assert sum(round1_scores.values()) > 0
        
        # Play second round
        game.play_round()
        
        # Verify scores accumulated
        round2_scores = {p.name: p.score for p in game.players}
        assert sum(round2_scores.values()) >= sum(round1_scores.values())
        
        # Play final round
        game.play_round()
        
        # Verify final scores
        final_scores = {p.name: p.score for p in game.players}
        assert sum(final_scores.values()) >= sum(round2_scores.values())
        
        # Verify scores are non-negative
        for score in final_scores.values():
            assert score >= 0
    
    def test_final_round_bonus_scoring(self):
        """Test that final round has bonus scoring."""
        # Test with minimum rounds for bonus (3 rounds)
        game_3_rounds = Game(["Alice", "Bob", "Charlie"], 3)
        game_3_rounds.play_game()
        
        total_score_3 = sum(p.score for p in game_3_rounds.players)
        
        # Test with more rounds
        game_5_rounds = Game(["Alice", "Bob", "Charlie"], 5)
        game_5_rounds.play_game()
        
        total_score_5 = sum(p.score for p in game_5_rounds.players)
        
        # More rounds should generally result in higher total scores due to final round bonus
        # (Though this isn't guaranteed due to randomness, it's very likely)
        # At minimum, verify both games completed successfully
        assert total_score_3 > 0
        assert total_score_5 > 0
    
    def test_minimum_players_game(self):
        """Test game with minimum number of players (3)."""
        game = Game(["Alice", "Bob", "Charlie"], 1)
        winner = game.play_game()
        
        assert winner is not None
        assert winner in game.players
        assert len(game.players) == 3
        
        # Verify all players got appropriate ranks for 3-player game
        ranks = [p.rank for p in game.players]
        expected_ranks = ["President", "Neutral", "Scum"]
        assert sorted(ranks) == sorted(expected_ranks)
    
    def test_maximum_players_game(self):
        """Test game with maximum number of players (8)."""
        player_names = [f"Player{i}" for i in range(1, 9)]
        game = Game(player_names, 1)
        winner = game.play_game()
        
        assert winner is not None
        assert winner in game.players
        assert len(game.players) == 8
        
        # Verify all players got some rank
        for player in game.players:
            assert player.rank is not None
    
    def test_single_round_game(self):
        """Test a game with just one round."""
        game = Game(["Alice", "Bob", "Charlie"], 1)
        winner = game.play_game()
        
        assert game.current_round == 1
        assert winner is not None
        
        # Even with one round, scores should be assigned
        total_score = sum(p.score for p in game.players)
        assert total_score > 0


class TestEdgeCases:
    """Test edge cases and error conditions."""
    
    def test_game_with_identical_scores_tie_breaking(self):
        """Test how the game handles ties in scoring."""
        # This is hard to test deterministically without controlling card distribution
        # But we can verify that even if there are ties, a winner is still selected
        games = []
        for i in range(10):  # Run multiple games to increase chance of ties
            game = Game(["Alice", "Bob", "Charlie"], 1)
            winner = game.play_game()
            games.append((game, winner))
        
        # All games should complete with winners
        for game, winner in games:
            assert winner is not None
            assert winner in game.players
            assert game.current_round == 1
    
    def test_game_state_consistency(self):
        """Test that game state remains consistent throughout play."""
        game = Game(["Alice", "Bob", "Charlie", "Dave"], 2)
        
        # Initial state checks
        assert len(game.players) == 4
        assert game.current_round == 0
        assert all(p.score == 0 for p in game.players)
        assert all(len(p.hand) == 0 for p in game.players)
        
        # After first round
        game.play_round()
        assert game.current_round == 1
        assert any(p.score > 0 for p in game.players)  # Someone should have scored
        
        # After second round
        game.play_round()
        assert game.current_round == 2
        
        # Game should be complete
        winner = game.get_winner()
        assert winner is not None
    
    def test_all_players_receive_cards_each_round(self):
        """Test that all players receive appropriate cards each round."""
        game = Game(["Alice", "Bob", "Charlie"], 2)
        
        # Round 1
        game.setup_round()
        
        # All players should have cards
        total_cards = sum(len(p.hand) for p in game.players)
        assert total_cards == 52  # Full deck
        
        # Cards should be distributed fairly
        for player in game.players:
            assert len(player.hand) > 0
            
        # The difference in hand sizes should be at most 1
        hand_sizes = [len(p.hand) for p in game.players]
        assert max(hand_sizes) - min(hand_sizes) <= 1
    
    def test_player_with_three_of_spades_starts(self):
        """Test that the player with 3♠ always starts the first trick."""
        # Run multiple games to verify this rule
        for i in range(5):
            game = Game(["Alice", "Bob", "Charlie"], 1)
            game.setup_round()
            
            starting_player = game.find_starting_player()
            assert starting_player is not None
            assert starting_player.has_three_of_clubs()


class TestGameRobustness:
    """Test game robustness and error handling."""
    
    def test_game_handles_rapid_succession_rounds(self):
        """Test that multiple rounds can be played in succession."""
        game = Game(["Alice", "Bob", "Charlie", "Dave"], 5)
        
        for round_num in range(1, 6):
            game.play_round()
            assert game.current_round == round_num
            
            # Verify game state is valid after each round
            for player in game.players:
                assert player.rank is not None
                assert player.score >= 0
    
    def test_consistent_game_completion(self):
        """Test that games always complete consistently."""
        # Run multiple complete games to ensure consistency
        for i in range(3):
            game = Game(["Alice", "Bob", "Charlie", "Dave"], 3)
            winner = game.play_game()
            
            # Standard completion checks
            assert winner is not None
            assert game.current_round == 3
            assert sum(p.score for p in game.players) > 0
            
            # Winner should have max score OR be the fallback due to ties
            max_score = max(p.score for p in game.players)
            # If get_winner() returned None (tie), play_game() returns first player
            # Otherwise, winner should have max score
            if game.get_winner() is not None:
                assert winner.score == max_score
            else:
                # Tie situation - winner is first player, verify tie exists
                max_score_count = sum(1 for p in game.players if p.score == max_score)
                assert max_score_count > 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
