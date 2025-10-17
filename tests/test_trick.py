"""Tests for Trick and Play classes."""

import pytest
from src.trick import Play, Trick
from src.player import Player
from src.card import Card, Suit, Rank


class TestPlay:
    """Test suite for Play class."""
    
    def test_play_creation_single(self):
        """Test creating a play with a single card."""
        player = Player("Alice")
        card = Card(Suit.SPADES, Rank.ACE)
        player.add_cards([card])
        
        play = Play([card], player)
        
        assert play.cards == [card]
        assert play.player == player
        assert play.num_cards == 1
        assert play.rank == Rank.ACE
    
    def test_play_creation_pair(self):
        """Test creating a play with a pair."""
        player = Player("Alice")
        cards = [
            Card(Suit.SPADES, Rank.KING),
            Card(Suit.HEARTS, Rank.KING)
        ]
        player.add_cards(cards)
        
        play = Play(cards, player)
        
        assert play.num_cards == 2
        assert play.rank == Rank.KING
    
    def test_play_creation_empty_cards(self):
        """Test that creating play with no cards raises error."""
        player = Player("Alice")
        
        with pytest.raises(ValueError, match="Cannot create play with no cards"):
            Play([], player)
    
    def test_play_creation_mixed_ranks(self):
        """Test that creating play with mixed ranks raises error."""
        player = Player("Alice")
        cards = [
            Card(Suit.SPADES, Rank.ACE),
            Card(Suit.HEARTS, Rank.KING)
        ]
        
        with pytest.raises(ValueError, match="All cards in a play must have the same rank"):
            Play(cards, player)
    
    def test_is_valid_same_rank(self):
        """Test that play with same rank cards is valid."""
        player = Player("Alice")
        cards = [
            Card(Suit.SPADES, Rank.FIVE),
            Card(Suit.HEARTS, Rank.FIVE),
            Card(Suit.CLUBS, Rank.FIVE)
        ]
        
        play = Play(cards, player)
        assert play.is_valid()
    
    def test_beats_higher_rank_single(self):
        """Test that higher rank beats lower rank (singles)."""
        player1 = Player("Alice")
        player2 = Player("Bob")
        
        play1 = Play([Card(Suit.SPADES, Rank.FIVE)], player1)
        play2 = Play([Card(Suit.HEARTS, Rank.KING)], player2)
        
        assert play2.beats(play1)
        assert not play1.beats(play2)
    
    def test_beats_higher_rank_pairs(self):
        """Test that higher rank beats lower rank (pairs)."""
        player1 = Player("Alice")
        player2 = Player("Bob")
        
        play1 = Play([
            Card(Suit.SPADES, Rank.QUEEN),
            Card(Suit.HEARTS, Rank.QUEEN)
        ], player1)
        
        play2 = Play([
            Card(Suit.CLUBS, Rank.ACE),
            Card(Suit.DIAMONDS, Rank.ACE)
        ], player2)
        
        assert play2.beats(play1)
        assert not play1.beats(play2)
    
    def test_beats_different_number_cards(self):
        """Test that plays with different number of cards don't beat each other."""
        player1 = Player("Alice")
        player2 = Player("Bob")
        
        play1 = Play([Card(Suit.SPADES, Rank.FIVE)], player1)
        play2 = Play([
            Card(Suit.HEARTS, Rank.TWO),
            Card(Suit.CLUBS, Rank.TWO)
        ], player2)
        
        # Even though TWO is highest, can't beat single with pair
        assert not play2.beats(play1)
        assert not play1.beats(play2)
    
    def test_three_of_spades_beats_everything_single(self):
        """Test that 3 of spades beats any single card."""
        player1 = Player("Alice")
        player2 = Player("Bob")
        
        play1 = Play([Card(Suit.HEARTS, Rank.TWO)], player1)  # Highest rank
        play2 = Play([Card(Suit.SPADES, Rank.THREE)], player2)  # 3 of spades
        
        assert play2.beats(play1)
    
    def test_three_of_spades_only_beats_singles(self):
        """Test that 3 of spades special rule only applies to singles."""
        player1 = Player("Alice")
        player2 = Player("Bob")
        
        play1 = Play([
            Card(Suit.HEARTS, Rank.FOUR),
            Card(Suit.CLUBS, Rank.FOUR)
        ], player1)
        
        # 3 of spades as single can't beat a pair
        play2 = Play([Card(Suit.SPADES, Rank.THREE)], player2)
        
        assert not play2.beats(play1)
    
    def test_nothing_beats_three_of_spades_single(self):
        """Test that nothing beats 3 of spades as a single."""
        player1 = Player("Alice")
        player2 = Player("Bob")
        
        play1 = Play([Card(Suit.SPADES, Rank.THREE)], player1)
        play2 = Play([Card(Suit.HEARTS, Rank.TWO)], player2)
        
        assert not play2.beats(play1)
    
    def test_play_str(self):
        """Test string representation of play."""
        player = Player("Alice")
        cards = [Card(Suit.SPADES, Rank.ACE)]
        
        play = Play(cards, player)
        play_str = str(play)
        
        assert "Alice" in play_str
        assert "A♠" in play_str
    
    def test_play_repr(self):
        """Test developer representation of play."""
        player = Player("Alice")
        cards = [Card(Suit.SPADES, Rank.ACE)]
        
        play = Play(cards, player)
        repr_str = repr(play)
        
        assert "Alice" in repr_str
        assert "Play" in repr_str


class TestTrick:
    """Test suite for Trick class."""
    
    def test_trick_creation(self):
        """Test creating a trick."""
        players = [Player("Alice"), Player("Bob"), Player("Charlie")]
        trick = Trick(players)
        
        assert len(trick.active_players) == 3
        assert trick.current_play is None
        assert len(trick.plays) == 0
    
    def test_trick_resets_player_passed_status(self):
        """Test that trick resets all players' passed status."""
        players = [Player("Alice"), Player("Bob")]
        players[0].has_passed = True
        players[1].has_passed = True
        
        trick = Trick(players)
        
        assert not players[0].has_passed
        assert not players[1].has_passed
    
    def test_add_play_first_play(self):
        """Test adding the first play to a trick."""
        players = [Player("Alice"), Player("Bob")]
        players[0].add_cards([Card(Suit.SPADES, Rank.ACE)])
        
        trick = Trick(players)
        play = Play([Card(Suit.SPADES, Rank.ACE)], players[0])
        
        trick.add_play(play)
        
        assert len(trick.plays) == 1
        assert trick.current_play == play
    
    def test_add_play_must_beat_current(self):
        """Test that play must beat current play."""
        players = [Player("Alice"), Player("Bob")]
        players[0].add_cards([Card(Suit.SPADES, Rank.KING)])
        players[1].add_cards([Card(Suit.HEARTS, Rank.FIVE)])
        
        trick = Trick(players)
        
        # First play
        play1 = Play([Card(Suit.SPADES, Rank.KING)], players[0])
        trick.add_play(play1)
        
        # Try to play lower card
        play2 = Play([Card(Suit.HEARTS, Rank.FIVE)], players[1])
        
        with pytest.raises(ValueError, match="doesn't beat current play"):
            trick.add_play(play2)
    
    def test_add_play_beats_current(self):
        """Test adding a play that beats current play."""
        players = [Player("Alice"), Player("Bob")]
        players[0].add_cards([Card(Suit.SPADES, Rank.FIVE)])
        players[1].add_cards([Card(Suit.HEARTS, Rank.KING)])
        
        trick = Trick(players)
        
        play1 = Play([Card(Suit.SPADES, Rank.FIVE)], players[0])
        trick.add_play(play1)
        
        play2 = Play([Card(Suit.HEARTS, Rank.KING)], players[1])
        trick.add_play(play2)
        
        assert len(trick.plays) == 2
        assert trick.current_play == play2
    
    def test_can_play_valid_cards(self):
        """Test checking if player can play valid cards."""
        players = [Player("Alice"), Player("Bob")]
        players[0].add_cards([Card(Suit.SPADES, Rank.ACE)])
        
        trick = Trick(players)
        
        assert trick.can_play(players[0], [Card(Suit.SPADES, Rank.ACE)])
    
    def test_can_play_mixed_ranks(self):
        """Test that mixed ranks are not valid."""
        players = [Player("Alice")]
        players[0].add_cards([
            Card(Suit.SPADES, Rank.ACE),
            Card(Suit.HEARTS, Rank.KING)
        ])
        
        trick = Trick(players)
        
        assert not trick.can_play(players[0], [
            Card(Suit.SPADES, Rank.ACE),
            Card(Suit.HEARTS, Rank.KING)
        ])
    
    def test_can_play_cards_not_in_hand(self):
        """Test that player can't play cards not in hand."""
        players = [Player("Alice")]
        trick = Trick(players)
        
        assert not trick.can_play(players[0], [Card(Suit.SPADES, Rank.ACE)])
    
    def test_can_play_after_passed(self):
        """Test that player can't play after passing."""
        players = [Player("Alice"), Player("Bob")]
        players[0].add_cards([Card(Suit.SPADES, Rank.ACE)])
        
        trick = Trick(players)
        trick.player_passes(players[0])
        
        assert not trick.can_play(players[0], [Card(Suit.SPADES, Rank.ACE)])
    
    def test_can_play_must_beat_current(self):
        """Test that play must beat current play."""
        players = [Player("Alice"), Player("Bob")]
        players[0].add_cards([Card(Suit.SPADES, Rank.KING)])
        players[1].add_cards([Card(Suit.HEARTS, Rank.FIVE)])
        
        trick = Trick(players)
        
        # First play
        play1 = Play([Card(Suit.SPADES, Rank.KING)], players[0])
        trick.add_play(play1)
        
        # Can't play lower card
        assert not trick.can_play(players[1], [Card(Suit.HEARTS, Rank.FIVE)])
    
    def test_player_passes(self):
        """Test marking player as passed."""
        players = [Player("Alice"), Player("Bob")]
        trick = Trick(players)
        
        trick.player_passes(players[0])
        
        assert players[0].has_passed
        assert not players[1].has_passed
    
    def test_player_passes_not_active(self):
        """Test that passing non-active player raises error."""
        players = [Player("Alice")]
        trick = Trick(players)
        
        other_player = Player("Charlie")
        
        with pytest.raises(ValueError, match="not active"):
            trick.player_passes(other_player)
    
    def test_is_complete_no_plays(self):
        """Test that trick is not complete with no plays."""
        players = [Player("Alice"), Player("Bob")]
        trick = Trick(players)
        
        assert not trick.is_complete()
    
    def test_is_complete_one_player_left(self):
        """Test that trick is complete when one player left."""
        players = [Player("Alice"), Player("Bob"), Player("Charlie")]
        players[0].add_cards([Card(Suit.SPADES, Rank.ACE)])
        
        trick = Trick(players)
        
        # Make a play
        play = Play([Card(Suit.SPADES, Rank.ACE)], players[0])
        trick.add_play(play)
        
        # Two players pass
        trick.player_passes(players[1])
        trick.player_passes(players[2])
        
        assert trick.is_complete()
    
    def test_is_complete_all_passed(self):
        """Test that trick is complete when all pass."""
        players = [Player("Alice"), Player("Bob")]
        players[0].add_cards([Card(Suit.SPADES, Rank.ACE)])
        
        trick = Trick(players)
        
        # Make a play
        play = Play([Card(Suit.SPADES, Rank.ACE)], players[0])
        trick.add_play(play)
        
        # Other player passes
        trick.player_passes(players[1])
        
        # Playing player also "passes" by not playing again
        # Actually, with 1 active player left, trick is complete
        assert trick.is_complete()
    
    def test_get_winner(self):
        """Test getting the winner of a trick."""
        players = [Player("Alice"), Player("Bob"), Player("Charlie")]
        players[0].add_cards([Card(Suit.SPADES, Rank.FIVE)])
        players[1].add_cards([Card(Suit.HEARTS, Rank.KING)])
        
        trick = Trick(players)
        
        # Alice plays
        play1 = Play([Card(Suit.SPADES, Rank.FIVE)], players[0])
        trick.add_play(play1)
        
        # Bob plays higher
        play2 = Play([Card(Suit.HEARTS, Rank.KING)], players[1])
        trick.add_play(play2)
        
        # Charlie passes
        trick.player_passes(players[2])
        
        # Alice passes (can't beat King)
        trick.player_passes(players[0])
        
        # Trick complete, Bob wins
        assert trick.is_complete()
        assert trick.get_winner() == players[1]
    
    def test_get_winner_not_complete(self):
        """Test that winner is None if trick not complete."""
        players = [Player("Alice"), Player("Bob")]
        trick = Trick(players)
        
        assert trick.get_winner() is None
    
    def test_get_active_players_count(self):
        """Test counting active players."""
        players = [Player("Alice"), Player("Bob"), Player("Charlie")]
        trick = Trick(players)
        
        assert trick.get_active_players_count() == 3
        
        trick.player_passes(players[0])
        assert trick.get_active_players_count() == 2
        
        trick.player_passes(players[1])
        assert trick.get_active_players_count() == 1
    
    def test_trick_str(self):
        """Test string representation of trick."""
        players = [Player("Alice"), Player("Bob")]
        trick = Trick(players)
        
        assert "no plays yet" in str(trick)
        
        players[0].add_cards([Card(Suit.SPADES, Rank.ACE)])
        play = Play([Card(Suit.SPADES, Rank.ACE)], players[0])
        trick.add_play(play)
        
        trick_str = str(trick)
        assert "ACE" in trick_str or "active" in trick_str
    
    def test_trick_repr(self):
        """Test developer representation of trick."""
        players = [Player("Alice"), Player("Bob")]
        trick = Trick(players)
        
        repr_str = repr(trick)
        assert "Trick" in repr_str
        assert "plays=0" in repr_str


class TestTrickIntegration:
    """Integration tests for Trick and Play."""
    
    def test_complete_trick_scenario(self):
        """Test a complete trick with multiple players."""
        # Create players
        alice = Player("Alice")
        bob = Player("Bob")
        charlie = Player("Charlie")
        
        # Give them cards
        alice.add_cards([Card(Suit.SPADES, Rank.FIVE)])
        bob.add_cards([Card(Suit.HEARTS, Rank.KING)])
        charlie.add_cards([Card(Suit.CLUBS, Rank.THREE)])
        
        # Start trick
        trick = Trick([alice, bob, charlie])
        
        # Alice leads with 5
        play1 = Play([Card(Suit.SPADES, Rank.FIVE)], alice)
        trick.add_play(play1)
        alice.remove_cards(play1.cards)
        
        # Bob plays King
        assert trick.can_play(bob, [Card(Suit.HEARTS, Rank.KING)])
        play2 = Play([Card(Suit.HEARTS, Rank.KING)], bob)
        trick.add_play(play2)
        bob.remove_cards(play2.cards)
        
        # Charlie passes
        trick.player_passes(charlie)
        
        # Alice passes (no cards left)
        trick.player_passes(alice)
        
        # Trick complete
        assert trick.is_complete()
        assert trick.get_winner() == bob
    
    def test_three_of_spades_special_case(self):
        """Test 3 of spades special rule in trick."""
        alice = Player("Alice")
        bob = Player("Bob")
        
        alice.add_cards([Card(Suit.HEARTS, Rank.TWO)])  # Highest rank
        bob.add_cards([Card(Suit.SPADES, Rank.THREE)])  # 3 of spades
        
        trick = Trick([alice, bob])
        
        # Alice plays TWO
        play1 = Play([Card(Suit.HEARTS, Rank.TWO)], alice)
        trick.add_play(play1)
        
        # Bob can play 3 of spades to beat it
        assert trick.can_play(bob, [Card(Suit.SPADES, Rank.THREE)])
        play2 = Play([Card(Suit.SPADES, Rank.THREE)], bob)
        trick.add_play(play2)
        
        assert trick.current_play == play2
        assert play2.beats(play1)
    
    def test_pair_vs_pair_scenario(self):
        """Test playing pairs against pairs."""
        alice = Player("Alice")
        bob = Player("Bob")
        
        alice.add_cards([
            Card(Suit.SPADES, Rank.FIVE),
            Card(Suit.HEARTS, Rank.FIVE)
        ])
        bob.add_cards([
            Card(Suit.CLUBS, Rank.KING),
            Card(Suit.DIAMONDS, Rank.KING)
        ])
        
        trick = Trick([alice, bob])
        
        # Alice plays pair of 5s
        play1 = Play([
            Card(Suit.SPADES, Rank.FIVE),
            Card(Suit.HEARTS, Rank.FIVE)
        ], alice)
        trick.add_play(play1)
        
        # Bob plays pair of Kings
        play2 = Play([
            Card(Suit.CLUBS, Rank.KING),
            Card(Suit.DIAMONDS, Rank.KING)
        ], bob)
        
        assert play2.beats(play1)
        trick.add_play(play2)
        
        # Alice passes
        trick.player_passes(alice)
        
        assert trick.is_complete()
        assert trick.get_winner() == bob
    
    def test_cannot_beat_with_different_count(self):
        """Test that you can't beat a pair with a single (even higher)."""
        alice = Player("Alice")
        bob = Player("Bob")
        
        alice.add_cards([
            Card(Suit.SPADES, Rank.THREE),
            Card(Suit.HEARTS, Rank.THREE)
        ])
        bob.add_cards([Card(Suit.CLUBS, Rank.TWO)])  # Highest single
        
        trick = Trick([alice, bob])
        
        # Alice plays pair of 3s
        play1 = Play([
            Card(Suit.SPADES, Rank.THREE),
            Card(Suit.HEARTS, Rank.THREE)
        ], alice)
        trick.add_play(play1)
        
        # Bob cannot play single TWO against pair
        assert not trick.can_play(bob, [Card(Suit.CLUBS, Rank.TWO)])
        
        # Bob must pass
        trick.player_passes(bob)
        
        assert trick.is_complete()
        assert trick.get_winner() == alice
