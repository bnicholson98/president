"""Card and Deck classes for President card game."""

from enum import Enum
from typing import List
import random


class Suit(Enum):
    """Card suits with their symbols."""
    CLUBS = "♣"
    DIAMONDS = "♦"
    HEARTS = "♥"
    SPADES = "♠"


class Rank(Enum):
    """Card ranks with their values for comparison.
    
    Note: THREE has value 0, and TWO has highest value (12).
    The numeric value is used for comparison - higher value wins.
    """
    THREE = 0
    FOUR = 1
    FIVE = 2
    SIX = 3
    SEVEN = 4
    EIGHT = 5
    NINE = 6
    TEN = 7
    JACK = 8
    QUEEN = 9
    KING = 10
    ACE = 11
    TWO = 12  # 2 is higher than Ace


class Card:
    """Represents a single playing card."""
    
    def __init__(self, suit: Suit, rank: Rank):
        """Initialize a card with a suit and rank.
        
        Args:
            suit: The suit of the card
            rank: The rank of the card
        """
        self.suit = suit
        self.rank = rank
    
    def __str__(self) -> str:
        """Return a string representation of the card.
        
        Returns:
            String like "3♣" or "A♠"
        """
        rank_str = {
            Rank.THREE: "3",
            Rank.FOUR: "4",
            Rank.FIVE: "5",
            Rank.SIX: "6",
            Rank.SEVEN: "7",
            Rank.EIGHT: "8",
            Rank.NINE: "9",
            Rank.TEN: "10",
            Rank.JACK: "J",
            Rank.QUEEN: "Q",
            Rank.KING: "K",
            Rank.ACE: "A",
            Rank.TWO: "2"
        }
        return f"{rank_str[self.rank]}{self.suit.value}"
    
    def __repr__(self) -> str:
        """Return a developer-friendly representation of the card.
        
        Returns:
            String like "Card(SPADES, ACE)"
        """
        return f"Card({self.suit.name}, {self.rank.name})"
    
    def __eq__(self, other) -> bool:
        """Check if two cards are equal.
        
        Args:
            other: Another card to compare
            
        Returns:
            True if suit and rank match
        """
        if not isinstance(other, Card):
            return False
        return self.suit == other.suit and self.rank == other.rank
    
    def __hash__(self) -> int:
        """Return hash of the card for use in sets/dicts.
        
        Returns:
            Hash value based on suit and rank
        """
        return hash((self.suit, self.rank))
    
    def get_value(self) -> int:
        """Get the numeric value for comparison.
        
        Returns:
            Integer value (0-12) where higher is better
        """
        return self.rank.value
    
    def is_three_of_spades(self) -> bool:
        """Check if this card is the 3 of spades.
        
        The 3 of spades is special - it's the highest single card.
        
        Returns:
            True if this is 3♠
        """
        return self.suit == Suit.SPADES and self.rank == Rank.THREE


class Deck:
    """Represents a standard 52-card deck."""
    
    def __init__(self):
        """Initialize a deck with all 52 cards."""
        self.cards: List[Card] = []
        for suit in Suit:
            for rank in Rank:
                self.cards.append(Card(suit, rank))
    
    def shuffle(self) -> None:
        """Shuffle the deck randomly."""
        random.shuffle(self.cards)
    
    def deal(self, num_players: int) -> List[List[Card]]:
        """Deal cards to players, one at a time in rotation.
        
        Args:
            num_players: Number of players to deal to (3-8)
            
        Returns:
            List of hands, where each hand is a list of Cards.
            Some players may have one more card than others.
            
        Raises:
            ValueError: If num_players is not between 3 and 8
        """
        if not 3 <= num_players <= 8:
            raise ValueError("Number of players must be between 3 and 8")
        
        # Initialize empty hands for each player
        hands: List[List[Card]] = [[] for _ in range(num_players)]
        
        # Deal one card at a time to each player in rotation
        for i, card in enumerate(self.cards):
            player_index = i % num_players
            hands[player_index].append(card)
        
        return hands
    
    def __len__(self) -> int:
        """Return the number of cards in the deck.
        
        Returns:
            Number of cards remaining in deck
        """
        return len(self.cards)
    
    def __str__(self) -> str:
        """Return string representation of the deck.
        
        Returns:
            String showing number of cards in deck
        """
        return f"Deck({len(self.cards)} cards)"
