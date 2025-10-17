"""Tests for Player class."""

import pytest
from src.player import Player
from src.card import Card, Suit, Rank
from src.trick import Play


class TestPlayer:
    """Test suite for Player class."""
    
    def test_player_creation(self):
        """Test that players can be created with a name."""
        player = Player("Alice")
        assert player.name == "Alice"
        assert player.hand == []
        assert player.score == 0
        assert player.rank is None
        assert player.has_passed is False
    
    def test_add_cards(self):
        """Test adding cards to player's hand."""
        player = Player("Alice")
        cards = [
            Card(Suit.SPADES, Rank.ACE),
            Card(Suit.HEARTS, Rank.KING)
        ]
        
        player.add_cards(cards)
        assert len(player.hand) == 2
        assert Card(Suit.SPADES, Rank.ACE) in player.hand
        assert Card(Suit.HEARTS, Rank.KING) in player.hand
    
    def test_add_cards_multiple_times(self):
        """Test adding cards multiple times."""
        player = Player("Alice")
        
        player.add_cards([Card(Suit.SPADES, Rank.ACE)])
        assert len(player.hand) == 1
        
        player.add_cards([Card(Suit.HEARTS, Rank.KING)])
        assert len(player.hand) == 2
    
    def test_remove_cards(self):
        """Test removing cards from player's hand."""
        player = Player("Alice")
        cards = [
            Card(Suit.SPADES, Rank.ACE),
            Card(Suit.HEARTS, Rank.KING),
            Card(Suit.CLUBS, Rank.QUEEN)
        ]
        player.add_cards(cards)
        
        player.remove_cards([Card(Suit.HEARTS, Rank.KING)])
        assert len(player.hand) == 2
        assert Card(Suit.HEARTS, Rank.KING) not in player.hand
        assert Card(Suit.SPADES, Rank.ACE) in player.hand
    
    def test_remove_cards_not_in_hand(self):
        """Test removing cards not in hand raises error."""
        player = Player("Alice")
        player.add_cards([Card(Suit.SPADES, Rank.ACE)])
        
        with pytest.raises(ValueError, match="not in hand"):
            player.remove_cards([Card(Suit.HEARTS, Rank.KING)])
    
    def test_sort_hand(self):
        """Test sorting hand by card value."""
        player = Player("Alice")
        cards = [
            Card(Suit.SPADES, Rank.ACE),    # value 11
            Card(Suit.HEARTS, Rank.THREE),  # value 0
            Card(Suit.CLUBS, Rank.KING),    # value 10
            Card(Suit.DIAMONDS, Rank.TWO)   # value 12
        ]
        player.add_cards(cards)
        
        player.sort_hand()
        
        # Should be sorted: THREE, KING, ACE, TWO
        assert player.hand[0].rank == Rank.THREE
        assert player.hand[1].rank == Rank.KING
        assert player.hand[2].rank == Rank.ACE
        assert player.hand[3].rank == Rank.TWO
    
    def test_has_three_of_clubs(self):
        """Test detecting 3 of clubs."""
        player = Player("Alice")
        
        # No cards
        assert player.has_three_of_clubs() is False
        
        # Has 3 of clubs
        player.add_cards([Card(Suit.CLUBS, Rank.THREE)])
        assert player.has_three_of_clubs() is True
        
        # Has other 3s but not clubs
        player2 = Player("Bob")
        player2.add_cards([Card(Suit.HEARTS, Rank.THREE)])
        assert player2.has_three_of_clubs() is False
    
    def test_is_hand_empty(self):
        """Test checking if hand is empty."""
        player = Player("Alice")
        
        assert player.is_hand_empty() is True
        
        player.add_cards([Card(Suit.SPADES, Rank.ACE)])
        assert player.is_hand_empty() is False
        
        player.remove_cards([Card(Suit.SPADES, Rank.ACE)])
        assert player.is_hand_empty() is True
    
    def test_reset_for_new_trick(self):
        """Test resetting player for new trick."""
        player = Player("Alice")
        player.has_passed = True
        
        player.reset_for_new_trick()
        assert player.has_passed is False
    
    def test_get_all_possible_plays_singles(self):
        """Test getting all possible plays with singles."""
        player = Player("Alice")
        cards = [
            Card(Suit.SPADES, Rank.ACE),
            Card(Suit.HEARTS, Rank.KING),
            Card(Suit.CLUBS, Rank.QUEEN)
        ]
        player.add_cards(cards)
        
        plays = player.get_valid_plays(None)
        
        # Should have 3 single card plays
        assert len(plays) == 3
        assert [Card(Suit.SPADES, Rank.ACE)] in plays
        assert [Card(Suit.HEARTS, Rank.KING)] in plays
        assert [Card(Suit.CLUBS, Rank.QUEEN)] in plays
    
    def test_get_all_possible_plays_with_pairs(self):
        """Test getting plays including pairs."""
        player = Player("Alice")
        cards = [
            Card(Suit.SPADES, Rank.ACE),
            Card(Suit.HEARTS, Rank.ACE),
            Card(Suit.CLUBS, Rank.KING)
        ]
        player.add_cards(cards)
        
        plays = player.get_valid_plays(None)
        
        # Should have: 1 single ace, 1 pair of aces, 1 single king (singles don't repeat per suit)
        assert len(plays) == 3
        
        # Check for pair
        pair_plays = [p for p in plays if len(p) == 2]
        assert len(pair_plays) == 1
        assert all(c.rank == Rank.ACE for c in pair_plays[0])
    
    def test_get_all_possible_plays_with_triples(self):
        """Test getting plays including triples."""
        player = Player("Alice")
        cards = [
            Card(Suit.SPADES, Rank.KING),
            Card(Suit.HEARTS, Rank.KING),
            Card(Suit.CLUBS, Rank.KING),
            Card(Suit.DIAMONDS, Rank.QUEEN)
        ]
        player.add_cards(cards)
        
        plays = player.get_valid_plays(None)
        
        # Should have: 1 single king, 1 pair of kings, 1 triple of kings, 1 single queen
        assert len(plays) == 4
        
        # Check for triple
        triple_plays = [p for p in plays if len(p) == 3]
        assert len(triple_plays) == 1
        assert all(c.rank == Rank.KING for c in triple_plays[0])
    
    def test_get_all_possible_plays_with_quads(self):
        """Test getting plays including quads."""
        player = Player("Alice")
        cards = [
            Card(Suit.SPADES, Rank.FIVE),
            Card(Suit.HEARTS, Rank.FIVE),
            Card(Suit.CLUBS, Rank.FIVE),
            Card(Suit.DIAMONDS, Rank.FIVE)
        ]
        player.add_cards(cards)
        
        plays = player.get_valid_plays(None)
        
        # Should have: 1 single, 1 pair, 1 triple, 1 quad
        assert len(plays) == 4
        
        # Check for quad
        quad_plays = [p for p in plays if len(p) == 4]
        assert len(quad_plays) == 1
        assert all(c.rank == Rank.FIVE for c in quad_plays[0])
    
    def test_get_plays_that_beat_single(self):
        """Test getting plays that beat a single card."""
        player = Player("Alice")
        player.add_cards([
            Card(Suit.SPADES, Rank.FIVE),
            Card(Suit.HEARTS, Rank.KING),
            Card(Suit.CLUBS, Rank.ACE)
        ])
        
        # Create a play to beat (single QUEEN)
        opponent = Player("Bob")
        opponent.add_cards([Card(Suit.DIAMONDS, Rank.QUEEN)])
        current_play = Play([Card(Suit.DIAMONDS, Rank.QUEEN)], opponent)
        
        # Get valid plays
        valid_plays = player.get_valid_plays(current_play)
        
        # Should be able to play KING or ACE (not FIVE)
        assert len(valid_plays) == 2
        valid_ranks = [p[0].rank for p in valid_plays]
        assert Rank.KING in valid_ranks
        assert Rank.ACE in valid_ranks
        assert Rank.FIVE not in valid_ranks
    
    def test_get_plays_that_beat_pair(self):
        """Test getting plays that beat a pair."""
        player = Player("Alice")
        player.add_cards([
            Card(Suit.SPADES, Rank.KING),
            Card(Suit.HEARTS, Rank.KING),
            Card(Suit.CLUBS, Rank.ACE),
            Card(Suit.DIAMONDS, Rank.ACE)
        ])
        
        # Create a pair of QUEENS to beat
        opponent = Player("Bob")
        opponent.add_cards([
            Card(Suit.DIAMONDS, Rank.QUEEN),
            Card(Suit.CLUBS, Rank.QUEEN)
        ])
        current_play = Play([
            Card(Suit.DIAMONDS, Rank.QUEEN),
            Card(Suit.CLUBS, Rank.QUEEN)
        ], opponent)
        
        # Get valid plays
        valid_plays = player.get_valid_plays(current_play)
        
        # Should be able to play pair of KINGS or pair of ACES
        assert len(valid_plays) == 2
        valid_ranks = [p[0].rank for p in valid_plays]
        assert Rank.KING in valid_ranks
        assert Rank.ACE in valid_ranks
    
    def test_three_of_spades_beats_everything(self):
        """Test that 3 of spades beats any single card."""
        player = Player("Alice")
        player.add_cards([Card(Suit.SPADES, Rank.THREE)])
        
        # Create a play with TWO (highest rank)
        opponent = Player("Bob")
        opponent.add_cards([Card(Suit.HEARTS, Rank.TWO)])
        current_play = Play([Card(Suit.HEARTS, Rank.TWO)], opponent)
        
        # Get valid plays
        valid_plays = player.get_valid_plays(current_play)
        
        # Should be able to play 3 of spades
        assert len(valid_plays) == 1
        assert valid_plays[0][0].is_three_of_spades()
    
    def test_choose_cards_to_give(self):
        """Test choosing strongest cards to give away."""
        player = Player("Alice")
        player.add_cards([
            Card(Suit.SPADES, Rank.THREE),  # value 0, but special - goes to end
            Card(Suit.HEARTS, Rank.FIVE),   # value 2
            Card(Suit.CLUBS, Rank.KING),    # value 10
            Card(Suit.DIAMONDS, Rank.TWO)   # value 12
        ])
        
        strongest = player.choose_cards_to_give(2)
        
        # Should give TWO and 3♠ (3♠ is moved to end since it's the only 3)
        assert len(strongest) == 2
        ranks = [c.rank for c in strongest]
        assert Rank.TWO in ranks
        assert Rank.THREE in ranks
    
    def test_choose_cards_to_give_not_enough(self):
        """Test choosing more cards than available raises error."""
        player = Player("Alice")
        player.add_cards([Card(Suit.SPADES, Rank.ACE)])
        
        with pytest.raises(ValueError, match="Cannot give"):
            player.choose_cards_to_give(2)
    
    def test_player_str(self):
        """Test string representation of player."""
        player = Player("Alice")
        player.add_cards([
            Card(Suit.SPADES, Rank.ACE),
            Card(Suit.HEARTS, Rank.KING)
        ])
        
        assert str(player) == "Alice (2 cards)"
    
    def test_player_repr(self):
        """Test developer representation of player."""
        player = Player("Alice")
        player.score = 5
        player.rank = "President"
        
        repr_str = repr(player)
        assert "Alice" in repr_str
        assert "score=5" in repr_str
        assert "rank=President" in repr_str


class TestPlayerIntegration:
    """Integration tests for Player class."""
    
    def test_complete_play_scenario(self):
        """Test a complete scenario of playing cards."""
        player = Player("Alice")
        
        # Deal some cards
        cards = [
            Card(Suit.SPADES, Rank.ACE),
            Card(Suit.HEARTS, Rank.ACE),
            Card(Suit.CLUBS, Rank.KING)
        ]
        player.add_cards(cards)
        
        # Get valid plays
        plays = player.get_valid_plays(None)
        assert len(plays) > 0
        
        # Play a pair
        pair = [Card(Suit.SPADES, Rank.ACE), Card(Suit.HEARTS, Rank.ACE)]
        player.remove_cards(pair)
        
        # Should have one card left
        assert len(player.hand) == 1
        assert not player.is_hand_empty()
        
        # Play last card
        player.remove_cards([Card(Suit.CLUBS, Rank.KING)])
        assert player.is_hand_empty()
    
    def test_card_exchange_scenario(self):
        """Test card exchange between players."""
        scum = Player("Scum")
        president = Player("President")
        
        # Give cards to players
        scum.add_cards([
            Card(Suit.SPADES, Rank.THREE),
            Card(Suit.HEARTS, Rank.FIVE),
            Card(Suit.CLUBS, Rank.ACE),
            Card(Suit.DIAMONDS, Rank.TWO)
        ])
        
        president.add_cards([
            Card(Suit.SPADES, Rank.FOUR),
            Card(Suit.HEARTS, Rank.SIX)
        ])
        
        # Scum gives 2 strongest cards
        cards_to_give = scum.choose_cards_to_give(2)
        scum.remove_cards(cards_to_give)
        president.add_cards(cards_to_give)
        
        # President gives 2 weakest cards (manually chosen)
        president.sort_hand()
        cards_to_give_back = president.hand[:2]
        president.remove_cards(cards_to_give_back)
        scum.add_cards(cards_to_give_back)
        
        # Verify exchange happened
        assert len(scum.hand) == 4
        assert len(president.hand) == 2
