"""Tests for Card and Deck classes."""

import pytest
from src.card import Card, Deck, Suit, Rank


class TestCard:
    """Test suite for Card class."""
    
    def test_card_creation(self):
        """Test that cards can be created with suit and rank."""
        card = Card(Suit.SPADES, Rank.ACE)
        assert card.suit == Suit.SPADES
        assert card.rank == Rank.ACE
    
    def test_card_str(self):
        """Test string representation of cards."""
        assert str(Card(Suit.SPADES, Rank.ACE)) == "A♠"
        assert str(Card(Suit.HEARTS, Rank.KING)) == "K♥"
        assert str(Card(Suit.CLUBS, Rank.THREE)) == "3♣"
        assert str(Card(Suit.DIAMONDS, Rank.TEN)) == "10♦"
        assert str(Card(Suit.SPADES, Rank.TWO)) == "2♠"
    
    def test_card_repr(self):
        """Test developer-friendly representation."""
        card = Card(Suit.SPADES, Rank.ACE)
        assert repr(card) == "Card(SPADES, ACE)"
    
    def test_card_equality(self):
        """Test that cards with same suit and rank are equal."""
        card1 = Card(Suit.SPADES, Rank.ACE)
        card2 = Card(Suit.SPADES, Rank.ACE)
        card3 = Card(Suit.HEARTS, Rank.ACE)
        card4 = Card(Suit.SPADES, Rank.KING)
        
        assert card1 == card2
        assert card1 != card3
        assert card1 != card4
        assert card1 != "not a card"
    
    def test_card_hash(self):
        """Test that cards can be used in sets and dicts."""
        card1 = Card(Suit.SPADES, Rank.ACE)
        card2 = Card(Suit.SPADES, Rank.ACE)
        card3 = Card(Suit.HEARTS, Rank.ACE)
        
        # Same cards should have same hash
        assert hash(card1) == hash(card2)
        
        # Should be able to use in sets
        card_set = {card1, card2, card3}
        assert len(card_set) == 2  # card1 and card2 are duplicates
    
    def test_card_value(self):
        """Test that card values are correct for comparison."""
        assert Card(Suit.SPADES, Rank.THREE).get_value() == 0
        assert Card(Suit.SPADES, Rank.FOUR).get_value() == 1
        assert Card(Suit.SPADES, Rank.FIVE).get_value() == 2
        assert Card(Suit.SPADES, Rank.ACE).get_value() == 11
        assert Card(Suit.SPADES, Rank.TWO).get_value() == 12
        
        # 2 should be higher than Ace
        assert Card(Suit.SPADES, Rank.TWO).get_value() > Card(Suit.SPADES, Rank.ACE).get_value()
    
    def test_card_value_comparison(self):
        """Test comparing card values."""
        three = Card(Suit.SPADES, Rank.THREE)
        ace = Card(Suit.HEARTS, Rank.ACE)
        two = Card(Suit.CLUBS, Rank.TWO)
        
        assert three.get_value() < ace.get_value()
        assert ace.get_value() < two.get_value()
        assert three.get_value() < two.get_value()
    
    def test_three_of_spades_identification(self):
        """Test that 3♠ is correctly identified."""
        three_spades = Card(Suit.SPADES, Rank.THREE)
        three_hearts = Card(Suit.HEARTS, Rank.THREE)
        ace_spades = Card(Suit.SPADES, Rank.ACE)
        
        assert three_spades.is_three_of_spades() is True
        assert three_hearts.is_three_of_spades() is False
        assert ace_spades.is_three_of_spades() is False
    
    def test_all_suits_and_ranks(self):
        """Test that all suits and ranks can be used."""
        for suit in Suit:
            for rank in Rank:
                card = Card(suit, rank)
                assert card.suit == suit
                assert card.rank == rank
                assert isinstance(str(card), str)


class TestDeck:
    """Test suite for Deck class."""
    
    def test_deck_initialization(self):
        """Test that deck initializes with 52 cards."""
        deck = Deck()
        assert len(deck) == 52
        assert len(deck.cards) == 52
    
    def test_deck_has_all_cards(self):
        """Test that deck contains exactly one of each card."""
        deck = Deck()
        
        # Count cards of each suit and rank
        suit_counts = {suit: 0 for suit in Suit}
        rank_counts = {rank: 0 for rank in Rank}
        
        for card in deck.cards:
            suit_counts[card.suit] += 1
            rank_counts[card.rank] += 1
        
        # Each suit should appear 13 times (one per rank)
        for suit, count in suit_counts.items():
            assert count == 13, f"{suit} appears {count} times, expected 13"
        
        # Each rank should appear 4 times (one per suit)
        for rank, count in rank_counts.items():
            assert count == 4, f"{rank} appears {count} times, expected 4"
    
    def test_deck_shuffle(self):
        """Test that shuffling changes card order."""
        deck1 = Deck()
        original_order = [str(card) for card in deck1.cards]
        
        deck1.shuffle()
        shuffled_order = [str(card) for card in deck1.cards]
        
        # Very unlikely that shuffle produces same order
        assert original_order != shuffled_order
        
        # But should still have same cards
        assert sorted(original_order) == sorted(shuffled_order)
    
    def test_deck_shuffle_maintains_count(self):
        """Test that shuffling doesn't lose or duplicate cards."""
        deck = Deck()
        deck.shuffle()
        
        assert len(deck) == 52
        
        # Check no duplicates
        card_set = set(deck.cards)
        assert len(card_set) == 52
    
    def test_deal_to_three_players(self):
        """Test dealing to 3 players."""
        deck = Deck()
        hands = deck.deal(3)
        
        assert len(hands) == 3
        
        # Total cards dealt should be 52
        total_cards = sum(len(hand) for hand in hands)
        assert total_cards == 52
        
        # With 52 cards and 3 players: 17, 17, 18 or similar distribution
        hand_sizes = [len(hand) for hand in hands]
        assert max(hand_sizes) - min(hand_sizes) <= 1
    
    def test_deal_to_four_players(self):
        """Test dealing to 4 players."""
        deck = Deck()
        hands = deck.deal(4)
        
        assert len(hands) == 4
        
        # Each player should get 13 cards (52 / 4 = 13)
        for hand in hands:
            assert len(hand) == 13
    
    def test_deal_to_five_players(self):
        """Test dealing to 5 players."""
        deck = Deck()
        hands = deck.deal(5)
        
        assert len(hands) == 5
        
        # Total cards dealt should be 52
        total_cards = sum(len(hand) for hand in hands)
        assert total_cards == 52
        
        # With 52 cards and 5 players: 10-11 cards each
        hand_sizes = [len(hand) for hand in hands]
        assert max(hand_sizes) - min(hand_sizes) <= 1
    
    def test_deal_to_eight_players(self):
        """Test dealing to maximum 8 players."""
        deck = Deck()
        hands = deck.deal(8)
        
        assert len(hands) == 8
        
        # Total cards dealt should be 52
        total_cards = sum(len(hand) for hand in hands)
        assert total_cards == 52
        
        # With 52 cards and 8 players: 6-7 cards each
        hand_sizes = [len(hand) for hand in hands]
        assert max(hand_sizes) - min(hand_sizes) <= 1
    
    def test_deal_distribution_is_fair(self):
        """Test that dealing distributes cards as evenly as possible."""
        deck = Deck()
        hands = deck.deal(5)
        
        # 52 cards / 5 players = 10 remainder 2
        # So 2 players get 11 cards, 3 get 10 cards
        hand_sizes = sorted([len(hand) for hand in hands])
        assert hand_sizes == [10, 10, 10, 11, 11]
    
    def test_deal_rotation(self):
        """Test that cards are dealt one at a time in rotation."""
        # Use unshuffled deck to test dealing order
        deck = Deck()
        hands = deck.deal(4)
        
        # First 4 cards should go to different players
        first_cards = [hand[0] for hand in hands]
        
        # These should be the first 4 cards from the deck
        expected_first_cards = Deck().cards[:4]
        
        for i in range(4):
            assert first_cards[i] == expected_first_cards[i]
    
    def test_deal_invalid_player_count(self):
        """Test that dealing with invalid player count raises error."""
        deck = Deck()
        
        with pytest.raises(ValueError, match="Number of players must be between 3 and 8"):
            deck.deal(2)
        
        with pytest.raises(ValueError, match="Number of players must be between 3 and 8"):
            deck.deal(9)
        
        with pytest.raises(ValueError, match="Number of players must be between 3 and 8"):
            deck.deal(0)
    
    def test_deal_no_duplicates(self):
        """Test that dealing doesn't create duplicate cards."""
        deck = Deck()
        deck.shuffle()
        hands = deck.deal(4)
        
        # Collect all dealt cards
        all_dealt_cards = []
        for hand in hands:
            all_dealt_cards.extend(hand)
        
        # Check for duplicates
        assert len(all_dealt_cards) == 52
        assert len(set(all_dealt_cards)) == 52
    
    def test_deck_str(self):
        """Test string representation of deck."""
        deck = Deck()
        assert str(deck) == "Deck(52 cards)"
        
        # After dealing, deck still reports original size
        # (In this implementation, deal doesn't remove cards from deck)
        hands = deck.deal(4)
        assert str(deck) == "Deck(52 cards)"


class TestCardIntegration:
    """Integration tests for Card and Deck together."""
    
    def test_full_game_setup(self):
        """Test a complete game setup scenario."""
        # Create and shuffle deck
        deck = Deck()
        deck.shuffle()
        
        # Deal to 5 players
        hands = deck.deal(5)
        
        # Verify all hands are valid
        assert len(hands) == 5
        for hand in hands:
            assert len(hand) >= 10
            assert len(hand) <= 11
            for card in hand:
                assert isinstance(card, Card)
    
    def test_three_of_spades_exists_in_deck(self):
        """Test that 3 of spades exists in every deck."""
        deck = Deck()
        
        three_of_spades_found = False
        for card in deck.cards:
            if card.is_three_of_spades():
                three_of_spades_found = True
                break
        
        assert three_of_spades_found, "3 of spades not found in deck"
    
    def test_three_of_spades_dealt_to_someone(self):
        """Test that 3 of spades is dealt to one of the players."""
        deck = Deck()
        deck.shuffle()
        hands = deck.deal(4)
        
        three_of_spades_found = False
        for hand in hands:
            for card in hand:
                if card.is_three_of_spades():
                    three_of_spades_found = True
                    break
        
        assert three_of_spades_found, "3 of spades not dealt to any player"
