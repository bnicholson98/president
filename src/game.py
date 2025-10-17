"""Game class for President card game."""

from typing import List, Optional
from src.card import Deck, Card, Suit, Rank
from src.player import Player
from src.trick import Trick, Play


class Game:
    """Manages the complete President game with multiple rounds."""
    
    def __init__(self, player_names: List[str], total_rounds: int):
        """Initialize a game with players and number of rounds.
        
        Args:
            player_names: List of player names
            total_rounds: Number of rounds to play
            
        Raises:
            ValueError: If player count not between 3 and 8
        """
        if not 3 <= len(player_names) <= 8:
            raise ValueError("Must have between 3 and 8 players")
        
        if total_rounds < 1:
            raise ValueError("Must play at least 1 round")
        
        self.players = [Player(name) for name in player_names]
        self.total_rounds = total_rounds
        self.current_round = 0
        self.deck = Deck()
        self.finished_players: List[Player] = []
    
    def setup_round(self) -> None:
        """Set up a new round: deal cards, then exchange (if not first round)."""
        # Reset player state
        for player in self.players:
            player.hand = []
            player.has_passed = False
        
        # Create new deck and deal
        self.deck = Deck()
        self.deck.shuffle()
        hands = self.deck.deal(len(self.players))
        
        for player, hand in zip(self.players, hands):
            player.add_cards(hand)
            player.sort_hand()
        
        # Card exchange (skip first round) - happens AFTER dealing
        if self.current_round > 0:
            self.handle_card_exchange()
        
        # Reset finished players list
        self.finished_players = []
    
    def find_starting_player(self) -> Player:
        """Find the player with 3 of clubs.
        
        Returns:
            Player who has 3 of clubs
            
        Raises:
            RuntimeError: If no player has 3 of clubs
        """
        for player in self.players:
            if player.has_three_of_clubs():
                return player
        
        raise RuntimeError("No player has 3 of clubs")
    
    def handle_card_exchange(self, interactive: bool = False, ui_callback=None) -> None:
        """Handle card exchange based on previous round rankings.
        
        President receives best cards from Scum.
        Vice-President receives best card from Vice-Scum (if 4+ players).
        
        Args:
            interactive: If True, allow players to choose cards
            ui_callback: Callback function for UI interactions
        
        Note: Exchange happens AFTER dealing new cards for the round.
        """
        # Find players by rank
        president = None
        vice_president = None
        vice_scum = None
        scum = None
        
        for player in self.players:
            if player.rank == "President":
                president = player
            elif player.rank == "Vice-President":
                vice_president = player
            elif player.rank == "Vice-Scum":
                vice_scum = player
            elif player.rank == "Scum":
                scum = player
        
        exchanges = []
        
        # Scum <-> President exchange (always happens if they exist and have cards)
        if president and scum and len(scum.hand) >= 2 and len(president.hand) >= 2:
            exchanges.append((scum.name, president.name, 2))
            
            if interactive and ui_callback:
                # Scum gives 2 best cards (automatic)
                cards_from_scum = scum.choose_cards_to_give(2)
                scum.remove_cards(cards_from_scum)
                president.add_cards(cards_from_scum)
                ui_callback('scum_gives', scum.name, cards_from_scum, president.name)
                
                # President chooses 2 cards to give back
                cards_from_president = ui_callback('president_chooses', president, 2, scum.name)
                president.remove_cards(cards_from_president)
                scum.add_cards(cards_from_president)
                ui_callback('president_gives', president.name, cards_from_president, scum.name)
            else:
                # Automatic exchange
                cards_from_scum = scum.choose_cards_to_give(2)
                scum.remove_cards(cards_from_scum)
                president.add_cards(cards_from_scum)
                
                president.sort_hand()
                cards_from_president = president.hand[:2]
                president.remove_cards(cards_from_president)
                scum.add_cards(cards_from_president)
        
        # Vice-Scum <-> Vice-President exchange (if they exist and have cards)
        if vice_president and vice_scum and len(vice_scum.hand) >= 1 and len(vice_president.hand) >= 1:
            exchanges.append((vice_scum.name, vice_president.name, 1))
            
            if interactive and ui_callback:
                # Vice-Scum gives 1 best card (automatic)
                cards_from_vscum = vice_scum.choose_cards_to_give(1)
                vice_scum.remove_cards(cards_from_vscum)
                vice_president.add_cards(cards_from_vscum)
                ui_callback('vscum_gives', vice_scum.name, cards_from_vscum, vice_president.name)
                
                # Vice-President chooses 1 card to give back
                cards_from_vp = ui_callback('vp_chooses', vice_president, 1, vice_scum.name)
                vice_president.remove_cards(cards_from_vp)
                vice_scum.add_cards(cards_from_vp)
                ui_callback('vp_gives', vice_president.name, cards_from_vp, vice_scum.name)
            else:
                # Automatic exchange
                cards_from_vscum = vice_scum.choose_cards_to_give(1)
                vice_scum.remove_cards(cards_from_vscum)
                vice_president.add_cards(cards_from_vscum)
                
                vice_president.sort_hand()
                cards_from_vp = vice_president.hand[:1]
                vice_president.remove_cards(cards_from_vp)
                vice_scum.add_cards(cards_from_vp)
        
        return exchanges
    
    def get_active_players(self) -> List[Player]:
        """Get players who still have cards.
        
        Returns:
            List of players with cards remaining
        """
        return [p for p in self.players if not p.is_hand_empty()]
    
    def play_trick(self, starting_player: Player) -> Player:
        """Play one complete trick.
        
        Args:
            starting_player: Player who leads the trick
            
        Returns:
            Winner of the trick
        """
        active = self.get_active_players()
        
        # If starting player has no cards, get next active player
        if starting_player not in active:
            starting_player = active[0] if active else starting_player
        
        trick = Trick(active)
        
        # Reorder players to start with starting_player
        player_order = []
        start_idx = active.index(starting_player)
        for i in range(len(active)):
            player_order.append(active[(start_idx + i) % len(active)])
        
        # Play until trick is complete
        max_iterations = 100  # Safety counter
        iterations = 0
        
        while not trick.is_complete() and iterations < max_iterations:
            iterations += 1
            
            for player in player_order:
                if trick.is_complete():
                    break
                
                if player.has_passed or player.is_hand_empty():
                    continue
                
                # For now, auto-play (this will be replaced by UI in Phase 6)
                valid_plays = player.get_valid_plays(trick.current_play)
                
                if valid_plays:
                    # Play the first valid play
                    cards_to_play = valid_plays[0]
                    
                    # Verify this is actually valid before playing
                    if trick.can_play(player, cards_to_play):
                        play = Play(cards_to_play, player)
                        trick.add_play(play)
                        player.remove_cards(cards_to_play)
                        
                        # Check if player finished
                        if player.is_hand_empty() and player not in self.finished_players:
                            self.finished_players.append(player)
                    else:
                        # Can't actually play, must pass
                        trick.player_passes(player)
                else:
                    # No valid plays, must pass
                    trick.player_passes(player)
        
        winner = trick.get_winner()
        return winner if winner else starting_player
    
    def play_round(self) -> None:
        """Play one complete round until only one player has cards."""
        self.current_round += 1
        self.setup_round()
        
        # Find starting player
        current_player = self.find_starting_player()
        
        # Play tricks until only one player has cards
        while len(self.get_active_players()) > 1:
            winner = self.play_trick(current_player)
            current_player = winner
        
        # Last player with cards is the final finisher
        remaining = self.get_active_players()
        if remaining:
            self.finished_players.append(remaining[0])
        
        # Assign ranks based on finish order
        self.assign_ranks()
        
        # Calculate and award scores
        self.calculate_scores(self.current_round == self.total_rounds)
    
    def assign_ranks(self) -> None:
        """Assign ranks based on finish order.
        
        First finisher: President
        Second finisher: Vice-President (if 4+ players)
        Second-to-last: Vice-Scum (if 4+ players)
        Last finisher: Scum
        """
        if len(self.finished_players) < 2:
            return
        
        # Clear all ranks first
        for player in self.players:
            player.rank = "Neutral"
        
        # Assign President
        self.finished_players[0].rank = "President"
        
        # Assign Scum
        self.finished_players[-1].rank = "Scum"
        
        # Assign Vice ranks if 4+ players
        if len(self.players) >= 4:
            self.finished_players[1].rank = "Vice-President"
            self.finished_players[-2].rank = "Vice-Scum"
    
    def calculate_scores(self, is_final_round: bool) -> None:
        """Calculate and award scores for the round.
        
        Args:
            is_final_round: True if this is the last round
        """
        if not self.finished_players:
            return
        
        # President gets points
        president = self.finished_players[0]
        
        if is_final_round:
            # Final round bonus: max(2, N-2) points
            bonus_points = max(2, self.total_rounds - 2)
            president.score += bonus_points
        else:
            # Regular round: 1 point
            president.score += 1
    
    def get_winner(self) -> Optional[Player]:
        """Get the player with the highest score.
        
        Returns:
            Player with highest score, or None if tie
        """
        if not self.players:
            return None
        
        max_score = max(p.score for p in self.players)
        winners = [p for p in self.players if p.score == max_score]
        
        return winners[0] if len(winners) == 1 else None
    
    def get_scores(self) -> List[tuple]:
        """Get sorted list of (player, score) tuples.
        
        Returns:
            List of (player, score) sorted by score descending
        """
        return sorted([(p, p.score) for p in self.players], 
                     key=lambda x: x[1], reverse=True)
    
    def play_game(self) -> Player:
        """Play the complete game for all rounds.
        
        Returns:
            Winner of the game
        """
        for round_num in range(self.total_rounds):
            self.play_round()
        
        winner = self.get_winner()
        return winner if winner else self.players[0]
    
    def __str__(self) -> str:
        """Return string representation of game.
        
        Returns:
            String showing game state
        """
        return f"Game(round {self.current_round}/{self.total_rounds}, {len(self.players)} players)"
    
    def __repr__(self) -> str:
        """Return developer-friendly representation.
        
        Returns:
            Detailed game information
        """
        return f"Game(players={len(self.players)}, rounds={self.current_round}/{self.total_rounds})"
