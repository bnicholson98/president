"""Trick and Play classes for President card game."""

from typing import List, Optional
from src.card import Card, Rank


class Play:
    """Represents a set of cards played together."""
    
    def __init__(self, cards: List[Card], player: 'Player'):
        """Initialize a play with cards and player.
        
        Args:
            cards: List of cards being played
            player: The player who played these cards
            
        Raises:
            ValueError: If cards list is empty or cards don't have same rank
        """
        if not cards:
            raise ValueError("Cannot create play with no cards")
        
        if not self._is_valid_set(cards):
            raise ValueError("All cards in a play must have the same rank")
        
        self.cards = cards
        self.player = player
        self.num_cards = len(cards)
        self.rank = cards[0].rank
    
    def _is_valid_set(self, cards: List[Card]) -> bool:
        """Check if all cards have the same rank.
        
        Args:
            cards: List of cards to check
            
        Returns:
            True if all cards have same rank
        """
        if not cards:
            return False
        
        first_rank = cards[0].rank
        return all(card.rank == first_rank for card in cards)
    
    def beats(self, other: 'Play') -> bool:
        """Check if this play beats another play.
        
        Args:
            other: Another play to compare against
            
        Returns:
            True if this play beats the other
        """
        # Must have same number of cards
        if self.num_cards != other.num_cards:
            return False
        
        # Special case: single 3 of spades beats everything
        if self.num_cards == 1 and self.cards[0].is_three_of_spades():
            return True
        
        # If other play has 3 of spades as single, nothing else beats it
        if other.num_cards == 1 and other.cards[0].is_three_of_spades():
            return False
        
        # Otherwise, compare by rank value
        return self.rank.value > other.rank.value
    
    def is_valid(self) -> bool:
        """Check if this play is valid (all cards same rank).
        
        Returns:
            True if valid
        """
        return self._is_valid_set(self.cards)
    
    def __str__(self) -> str:
        """Return string representation of play.
        
        Returns:
            String showing cards played
        """
        cards_str = ", ".join(str(card) for card in self.cards)
        return f"{self.player.name} plays: {cards_str}"
    
    def __repr__(self) -> str:
        """Return developer-friendly representation.
        
        Returns:
            Detailed play information
        """
        return f"Play(player={self.player.name}, cards={[str(c) for c in self.cards]})"


class Trick:
    """Manages a single trick (round of plays until someone wins)."""
    
    def __init__(self, players: List['Player']):
        """Initialize a trick with active players.
        
        Args:
            players: List of players participating in this trick
        """
        self.plays: List[Play] = []
        self.current_play: Optional[Play] = None
        self.active_players = players.copy()
        
        # Reset all players' passed status
        for player in self.active_players:
            player.reset_for_new_trick()
    
    def add_play(self, play: Play) -> None:
        """Add a play to the trick.
        
        Args:
            play: The play to add
            
        Raises:
            ValueError: If play doesn't beat current play
        """
        if self.current_play is not None:
            if not play.beats(self.current_play):
                raise ValueError(f"Play {play} doesn't beat current play {self.current_play}")
        
        self.plays.append(play)
        self.current_play = play
    
    def can_play(self, player: 'Player', cards: List[Card]) -> bool:
        """Check if player can play these cards.
        
        Args:
            player: The player attempting to play
            cards: The cards to play
            
        Returns:
            True if the play is valid
        """
        # Check if player has passed
        if player.has_passed:
            return False
        
        # Check if player is still active
        if player not in self.active_players:
            return False
        
        # Check if cards are valid (all same rank)
        if not cards:
            return False
        
        first_rank = cards[0].rank
        if not all(card.rank == first_rank for card in cards):
            return False
        
        # Check if player has these cards
        for card in cards:
            if card not in player.hand:
                return False
        
        # If no current play, can play anything valid
        if self.current_play is None:
            return True
        
        # Otherwise, must beat current play
        try:
            test_play = Play(cards, player)
            return test_play.beats(self.current_play)
        except ValueError:
            return False
    
    def player_passes(self, player: 'Player') -> None:
        """Mark player as passed for this trick.
        
        Args:
            player: The player who is passing
            
        Raises:
            ValueError: If player not in active players
        """
        if player not in self.active_players:
            raise ValueError(f"Player {player.name} is not active in this trick")
        
        player.has_passed = True
    
    def is_complete(self) -> bool:
        """Check if the trick is complete.
        
        A trick is complete when:
        - Only one active player remains (hasn't passed), OR
        - All players have passed
        
        Returns:
            True if trick is complete
        """
        if not self.current_play:
            # No play yet, trick not complete
            return False
        
        # Count players who haven't passed
        active_count = sum(1 for p in self.active_players if not p.has_passed)
        
        # Trick is complete if 0 or 1 active players remain
        return active_count <= 1
    
    def get_winner(self) -> Optional['Player']:
        """Get the winner of the trick.
        
        Returns:
            The player who won, or None if trick not complete
        """
        if not self.is_complete():
            return None
        
        if not self.current_play:
            return None
        
        # Winner is the player who made the current (highest) play
        return self.current_play.player
    
    def get_active_players_count(self) -> int:
        """Get count of players who haven't passed.
        
        Returns:
            Number of active players
        """
        return sum(1 for p in self.active_players if not p.has_passed)
    
    def __str__(self) -> str:
        """Return string representation of trick.
        
        Returns:
            String showing trick state
        """
        if not self.current_play:
            return "Trick (no plays yet)"
        
        active = self.get_active_players_count()
        return f"Trick (current: {self.current_play.cards[0].rank.name}, {active} active players)"
    
    def __repr__(self) -> str:
        """Return developer-friendly representation.
        
        Returns:
            Detailed trick information
        """
        return f"Trick(plays={len(self.plays)}, active_players={len(self.active_players)})"
