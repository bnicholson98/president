"""Player class for President card game."""

from typing import List, Optional
from src.card import Card, Rank


class Player:
    """Represents a player in the President game."""
    
    def __init__(self, name: str):
        """Initialize a player with a name.
        
        Args:
            name: The player's name
        """
        self.name = name
        self.hand: List[Card] = []
        self.score = 0
        self.rank: Optional[str] = None  # President, Vice-President, Neutral, Vice-Scum, Scum
        self.has_passed = False
    
    def add_cards(self, cards: List[Card]) -> None:
        """Add cards to the player's hand.
        
        Args:
            cards: List of cards to add
        """
        self.hand.extend(cards)
    
    def remove_cards(self, cards: List[Card]) -> None:
        """Remove cards from the player's hand.
        
        Args:
            cards: List of cards to remove
            
        Raises:
            ValueError: If any card is not in hand
        """
        for card in cards:
            if card not in self.hand:
                raise ValueError(f"Card {card} not in hand")
            self.hand.remove(card)
    
    def sort_hand(self) -> None:
        """Sort hand by card value (lowest to highest)."""
        self.hand.sort(key=lambda card: card.get_value())
    
    def has_three_of_clubs(self) -> bool:
        """Check if player has 3 of clubs.
        
        Returns:
            True if player has 3♣
        """
        from src.card import Suit
        for card in self.hand:
            if card.suit == Suit.CLUBS and card.rank == Rank.THREE:
                return True
        return False
    
    def get_valid_plays(self, current_play: Optional['Play'] = None) -> List[List[Card]]:
        """Get all valid card combinations this player can play.
        
        Args:
            current_play: The current play to beat, or None if leading
            
        Returns:
            List of valid plays, where each play is a list of cards
        """
        if current_play is None:
            # Can lead with any single card or set
            return self._get_all_possible_plays()
        else:
            # Must beat the current play
            return self._get_plays_that_beat(current_play)
    
    def _get_all_possible_plays(self) -> List[List[Card]]:
        """Get all possible plays from hand (for leading).
        
        Returns:
            List of all possible plays
        """
        plays = []
        
        # Group cards by rank
        rank_groups = {}
        for card in self.hand:
            rank = card.rank
            if rank not in rank_groups:
                rank_groups[rank] = []
            rank_groups[rank].append(card)
        
        # Generate all possible plays
        for rank, cards in rank_groups.items():
            # Single card
            for card in cards:
                plays.append([card])
            
            # Pairs
            if len(cards) >= 2:
                plays.append(cards[:2])
            
            # Triples
            if len(cards) >= 3:
                plays.append(cards[:3])
            
            # Quads
            if len(cards) == 4:
                plays.append(cards)
        
        return plays
    
    def _get_plays_that_beat(self, current_play: 'Play') -> List[List[Card]]:
        """Get all plays that can beat the current play.
        
        Args:
            current_play: The play to beat
            
        Returns:
            List of valid plays that beat current_play
        """
        from src.trick import Play
        
        valid_plays = []
        num_cards_needed = current_play.num_cards
        current_value = current_play.rank.value
        
        # Group cards by rank
        rank_groups = {}
        for card in self.hand:
            rank = card.rank
            if rank not in rank_groups:
                rank_groups[rank] = []
            rank_groups[rank].append(card)
        
        # Check if we have 3 of spades and current play is a single
        if num_cards_needed == 1:
            for card in self.hand:
                if card.is_three_of_spades():
                    valid_plays.append([card])
                    # 3 of spades beats everything as a single
                    return valid_plays
        
        # Find ranks that beat current play
        for rank, cards in rank_groups.items():
            if rank.value > current_value and len(cards) >= num_cards_needed:
                # Can play this rank
                valid_plays.append(cards[:num_cards_needed])
        
        return valid_plays
    
    def choose_cards_to_give(self, num: int) -> List[Card]:
        """Choose strongest cards to give away (for Scum).
        
        Args:
            num: Number of cards to give
            
        Returns:
            List of strongest cards from hand
            
        Raises:
            ValueError: If not enough cards in hand
        """
        if num > len(self.hand):
            raise ValueError(f"Cannot give {num} cards, only have {len(self.hand)}")
        
        # Sort hand and take the highest value cards
        self.sort_hand()
        strongest_cards = self.hand[-num:]
        return strongest_cards
    
    def is_hand_empty(self) -> bool:
        """Check if player has no cards left.
        
        Returns:
            True if hand is empty
        """
        return len(self.hand) == 0
    
    def reset_for_new_trick(self) -> None:
        """Reset player state for a new trick."""
        self.has_passed = False
    
    def __str__(self) -> str:
        """Return string representation of player.
        
        Returns:
            String with player name and card count
        """
        return f"{self.name} ({len(self.hand)} cards)"
    
    def __repr__(self) -> str:
        """Return developer-friendly representation.
        
        Returns:
            Detailed player information
        """
        return f"Player(name={self.name}, cards={len(self.hand)}, score={self.score}, rank={self.rank})"
