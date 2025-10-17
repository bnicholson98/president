"""Main entry point for President card game."""

from rich.prompt import Confirm

from src.game import Game
from src.ui import (
    display_welcome,
    display_rules_summary,
    get_game_setup,
    get_player_names,
    display_round_start,
    display_starting_player,
    display_hand,
    display_trick_state,
    display_rankings,
    get_player_action,
    display_play,
    display_pass,
    display_trick_winner,
    display_round_results,
    display_scores,
    display_game_winner,
    display_card_exchange_announcement,
    display_cards_given,
    get_cards_to_give_away,
    confirm_continue,
    clear_screen,
    pause,
    console
)
from src.trick import Trick, Play
from src.player import Player


def play_trick_interactive(game: Game, starting_player: Player, is_first_trick: bool = False) -> Player:
    """Play one trick interactively.
    
    Args:
        game: The game instance
        starting_player: Player who leads
        is_first_trick: True if this is the first trick of the round
        
    Returns:
        Winner of the trick
    """
    active = game.get_active_players()
    
    # If starting player has no cards, get next active player
    if starting_player not in active:
        starting_player = active[0] if active else starting_player
    
    trick = Trick(active, is_first_trick=is_first_trick)
    
    # Reorder players to start with starting_player
    player_order = []
    start_idx = active.index(starting_player)
    for i in range(len(active)):
        player_order.append(active[(start_idx + i) % len(active)])
    
    # Play until trick is complete
    max_iterations = 100
    iterations = 0
    
    while not trick.is_complete() and iterations < max_iterations:
        iterations += 1
        
        for player in player_order:
            if trick.is_complete():
                break
            
            if player.has_passed or player.is_hand_empty():
                continue
            
            # Clear screen for new player
            clear_screen()
            
            console.print()
            console.rule(f"[cyan]{player.name}'s Turn[/cyan]")
            console.print()
            
            # Show current hand
            display_hand(player)
            
            # Show current play
            display_trick_state(trick, trick.current_play)
            
            # Get valid plays (check if first trick and no plays yet)
            is_leading_first = is_first_trick and trick.current_play is None
            valid_plays = player.get_valid_plays(trick.current_play, is_first_trick=is_leading_first)
            
            # Get player action
            chosen_cards = get_player_action(player, valid_plays)
            
            if chosen_cards:
                # Player chose to play cards
                if trick.can_play(player, chosen_cards):
                    play = Play(chosen_cards, player)
                    trick.add_play(play)
                    player.remove_cards(chosen_cards)
                    
                    display_play(player, chosen_cards)
                    
                    # Check if player finished
                    if player.is_hand_empty() and player not in game.finished_players:
                        game.finished_players.append(player)
                        console.print(f"[bold green]{player.name} is out of cards![/bold green]")
                        console.print()
                else:
                    # Shouldn't happen, but just in case
                    display_pass(player)
                    trick.player_passes(player)
            else:
                # Player chose to pass
                display_pass(player)
                trick.player_passes(player)
            
            # Pause before next player
            pause(f"Pass to next player")
    
    winner = trick.get_winner()
    if winner:
        display_trick_winner(winner)
        pause()
    
    return winner if winner else starting_player


def handle_card_exchange_ui(action_type: str, *args):
    """Handle card exchange UI interactions.
    
    Args:
        action_type: Type of exchange action
        *args: Arguments for the action
    """
    if action_type == 'scum_gives':
        scum_name, cards, president_name = args
        console.print(f"[bold]{scum_name}[/bold] (Scum) automatically gives their 2 best cards:")
        display_cards_given(scum_name, cards, president_name)
        pause()
        
    elif action_type == 'president_chooses':
        president, num_cards, scum_name = args
        clear_screen()
        console.print(f"\n[bold yellow]Card Exchange: President's Turn[/bold yellow]\n")
        console.print(f"Choose {num_cards} card(s) to give to {scum_name} (Scum)\n")
        chosen = get_cards_to_give_away(president, num_cards, scum_name)
        # Show only to president what they chose
        console.print(f"\n[dim]You will give these cards (only you can see this)[/dim]")
        pause()
        return chosen
        
    elif action_type == 'president_gives':
        president_name, cards, scum_name = args
        # Don't display the cards - only the president saw them
        console.print(f"[bold]{president_name}[/bold] (President) has chosen their cards to give.")
        pause()
        
    elif action_type == 'vscum_gives':
        vscum_name, cards, vp_name = args
        console.print(f"[bold]{vscum_name}[/bold] (Vice-Scum) automatically gives their best card:")
        display_cards_given(vscum_name, cards, vp_name)
        pause()
        
    elif action_type == 'vp_chooses':
        vp, num_cards, vscum_name = args
        clear_screen()
        console.print(f"\n[bold yellow]Card Exchange: Vice-President's Turn[/bold yellow]\n")
        console.print(f"Choose {num_cards} card(s) to give to {vscum_name} (Vice-Scum)\n")
        chosen = get_cards_to_give_away(vp, num_cards, vscum_name)
        # Show only to VP what they chose
        console.print(f"\n[dim]You will give this card (only you can see this)[/dim]")
        pause()
        return chosen
        
    elif action_type == 'vp_gives':
        vp_name, cards, vscum_name = args
        # Don't display the card - only the VP saw it
        console.print(f"[bold]{vp_name}[/bold] (Vice-President) has chosen their card to give.")
        pause()


def play_round_interactive(game: Game) -> None:
    """Play one round interactively.
    
    Args:
        game: The game instance
    """
    game.current_round += 1
    
    clear_screen()
    display_round_start(game.current_round, game.total_rounds)
    
    # Show current rankings if not first round
    if game.current_round > 1:
        console.print("[bold]Current Rankings:[/bold]")
        display_rankings(game.players)
    
    # Setup round (deals cards)
    game.setup_round()
    
    # Handle card exchange if not first round
    if game.current_round > 1:
        clear_screen()
        console.print()
        console.rule("[bold yellow]Card Exchange[/bold yellow]")
        console.print()
        
        # Get exchanges info
        exchanges = []
        for player in game.players:
            if player.rank == "President":
                president = player
            elif player.rank == "Scum":
                scum = player
            elif player.rank == "Vice-President":
                vice_president = player
            elif player.rank == "Vice-Scum":
                vice_scum = player
        
        # Announce exchanges
        if any(p.rank in ["President", "Scum"] for p in game.players):
            exchanges.append(("Scum", "President", 2))
        if any(p.rank in ["Vice-President", "Vice-Scum"] for p in game.players):
            exchanges.append(("Vice-Scum", "Vice-President", 1))
        
        if exchanges:
            display_card_exchange_announcement(exchanges)
            pause()
            
            # Do the actual exchange with UI
            game.handle_card_exchange(interactive=True, ui_callback=handle_card_exchange_ui)
            
            clear_screen()
            console.print("[bold green]Card exchange complete![/bold green]\n")
            pause()
    
    # Find starting player
    clear_screen()
    current_player = game.find_starting_player()
    display_starting_player(current_player)
    pause()
    
    # Play tricks until only one player has cards
    first_trick = True
    while len(game.get_active_players()) > 1:
        winner = play_trick_interactive(game, current_player, is_first_trick=first_trick)
        current_player = winner
        first_trick = False
    
    # Last player with cards is the final finisher
    remaining = game.get_active_players()
    if remaining:
        game.finished_players.append(remaining[0])
    
    # Assign ranks and scores
    game.assign_ranks()
    game.calculate_scores(game.current_round == game.total_rounds)
    
    # Display results
    clear_screen()
    console.print()
    display_round_results(game.finished_players)
    display_scores(game.players)
    
    if game.current_round < game.total_rounds:
        pause("Press Enter to continue to next round")
        if not confirm_continue():
            return


def main():
    """Main game loop."""
    # Welcome screen
    clear_screen()
    display_welcome()
    
    # Show rules and get confirmation to continue
    show_rules = Confirm.ask("Would you like to see the rules?", default=True, console=console)
    console.print()
    
    if show_rules:
        display_rules_summary()
        pause()
    
    # Get game setup
    clear_screen()
    num_players, num_rounds = get_game_setup()
    player_names = get_player_names(num_players)
    
    # Create game
    game = Game(player_names, num_rounds)
    
    # Play all rounds
    for round_num in range(num_rounds):
        play_round_interactive(game)
        
        if game.current_round >= num_rounds:
            break
    
    # Display final winner
    clear_screen()
    console.print()
    display_scores(game.players)
    
    winner = game.get_winner()
    if winner:
        display_game_winner(winner)
    else:
        console.print("[yellow]Game ended in a tie![/yellow]")
        console.print()
    
    # Ask to play again
    play_again = Confirm.ask("Play again?", default=False, console=console)
    console.print()
    
    if play_again:
        main()
    else:
        console.print("\n[bold cyan]Thanks for playing President![/bold cyan]\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n\n[yellow]Game interrupted. Thanks for playing![/yellow]\n")
    except Exception as e:
        console.print(f"\n[bold red]Error: {e}[/bold red]\n")
        import traceback
        traceback.print_exc()
