"""User Interface module using Rich library for President card game."""

from typing import List, Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt, Confirm
from rich.text import Text
from rich.layout import Layout
from rich import box

from src.card import Card
from src.player import Player
from src.trick import Play


console = Console()


def display_welcome() -> None:
    """Display welcome screen with game title."""
    welcome_text = Text()
    welcome_text.append("🎴 ", style="bold yellow")
    welcome_text.append("PRESIDENT", style="bold cyan")
    welcome_text.append(" CARD GAME ", style="bold white")
    welcome_text.append("🎴", style="bold yellow")
    
    panel = Panel(
        welcome_text,
        box=box.DOUBLE,
        border_style="cyan",
        padding=(1, 2)
    )
    console.print()
    console.print(panel)
    console.print()


def display_rules_summary() -> None:
    """Display brief rules summary."""
    rules = """
[bold cyan]Quick Rules:[/bold cyan]
• Be the first to get rid of all your cards
• Must beat the current play or pass
• 2 is the highest card, 3 is lowest
• 3♠ beats everything when played alone
• Winner becomes President, last becomes Scum
• Card exchanges happen between rounds
"""
    console.print(Panel(rules, title="How to Play", border_style="green"))
    console.print()


def get_game_setup() -> tuple:
    """Get game setup from user.
    
    Returns:
        Tuple of (num_players, num_rounds)
    """
    console.print("[bold]Game Setup[/bold]", style="cyan")
    console.print()
    
    num_players = IntPrompt.ask(
        "Number of players (3-8)",
        default=4,
        console=console
    )
    
    while not 3 <= num_players <= 8:
        console.print("[red]Please enter between 3 and 8 players[/red]")
        num_players = IntPrompt.ask(
            "Number of players (3-8)",
            default=4,
            console=console
        )
    
    num_rounds = IntPrompt.ask(
        "Number of rounds to play",
        default=3,
        console=console
    )
    
    while num_rounds < 1:
        console.print("[red]Must play at least 1 round[/red]")
        num_rounds = IntPrompt.ask(
            "Number of rounds to play",
            default=3,
            console=console
        )
    
    console.print()
    return num_players, num_rounds


def get_player_names(num_players: int) -> List[str]:
    """Get player names from user.
    
    Args:
        num_players: Number of players
        
    Returns:
        List of player names
    """
    names = []
    console.print("[bold]Enter Player Names[/bold]", style="cyan")
    console.print()
    
    for i in range(num_players):
        name = Prompt.ask(
            f"Player {i+1} name",
            default=f"Player {i+1}",
            console=console
        )
        names.append(name)
    
    console.print()
    return names


def get_card_color(card: Card) -> str:
    """Get the color style for a card based on suit.
    
    Args:
        card: The card to color
        
    Returns:
        Rich color style string
    """
    from src.card import Suit
    
    if card.suit in (Suit.HEARTS, Suit.DIAMONDS):
        return "red"
    else:
        return "white"


def format_card(card: Card) -> Text:
    """Format a card with color.
    
    Args:
        card: Card to format
        
    Returns:
        Rich Text object with colored card
    """
    text = Text()
    text.append(str(card), style=f"bold {get_card_color(card)}")
    return text


def display_hand(player: Player) -> None:
    """Display a player's hand.
    
    Args:
        player: Player whose hand to display
    """
    table = Table(title=f"{player.name}'s Hand", show_header=False, box=box.ROUNDED)
    
    # Sort and display cards
    player.sort_hand()
    
    # Group cards by rank for better display
    cards_text = Text()
    for i, card in enumerate(player.hand):
        if i > 0:
            cards_text.append(" ")
        cards_text.append(format_card(card))
    
    table.add_row(cards_text)
    table.add_row(f"[dim]Total: {len(player.hand)} cards[/dim]")
    
    console.print(table)
    console.print()


def display_trick_state(trick, current_play: Optional[Play]) -> None:
    """Display the current trick state.
    
    Args:
        trick: Current trick
        current_play: Current play to beat (if any)
    """
    if current_play:
        cards_text = Text()
        for i, card in enumerate(current_play.cards):
            if i > 0:
                cards_text.append(", ")
            cards_text.append(format_card(card))
        
        info = Text()
        info.append(f"{current_play.player.name} played: ", style="bold")
        info.append(cards_text)
        
        console.print(Panel(info, title="Current Play", border_style="yellow"))
    else:
        console.print(Panel("[dim]No current play - you can lead with any cards[/dim]", 
                          title="Current Play", border_style="yellow"))
    console.print()


def display_rankings(players: List[Player]) -> None:
    """Display current player rankings.
    
    Args:
        players: List of players
    """
    table = Table(title="Current Rankings", box=box.ROUNDED)
    table.add_column("Player", style="cyan")
    table.add_column("Rank", style="yellow")
    table.add_column("Cards", style="white")
    
    for player in players:
        rank_display = player.rank if player.rank else "Neutral"
        rank_style = {
            "President": "bold gold1",
            "Vice-President": "bold yellow",
            "Neutral": "white",
            "Vice-Scum": "dim yellow",
            "Scum": "dim red"
        }.get(rank_display, "white")
        
        table.add_row(
            player.name,
            Text(rank_display, style=rank_style),
            str(len(player.hand))
        )
    
    console.print(table)
    console.print()


def display_scores(players: List[Player]) -> None:
    """Display score table.
    
    Args:
        players: List of players
    """
    table = Table(title="Scores", box=box.DOUBLE)
    table.add_column("Rank", style="cyan", justify="center")
    table.add_column("Player", style="bold")
    table.add_column("Score", style="yellow", justify="center")
    
    # Sort by score descending
    sorted_players = sorted(players, key=lambda p: p.score, reverse=True)
    
    for i, player in enumerate(sorted_players, 1):
        rank_style = "gold1" if i == 1 else "white"
        table.add_row(
            str(i),
            Text(player.name, style=rank_style),
            Text(str(player.score), style=rank_style)
        )
    
    console.print(table)
    console.print()


def get_player_action(player: Player, valid_plays: List[List[Card]], can_pass: bool = True) -> Optional[List[Card]]:
    """Get player's action (play cards or pass).
    
    Args:
        player: Player making the action
        valid_plays: List of valid plays available
        can_pass: Whether player is allowed to pass (False when leading)
        
    Returns:
        List of cards to play, or None to pass
    """
    console.print(f"[bold cyan]{player.name}'s turn[/bold cyan]")
    console.print()
    
    if not valid_plays:
        console.print("[yellow]No valid plays available - you must pass[/yellow]")
        console.input("[dim]Press Enter to pass...[/dim] ")
        console.print()
        return None
    
    # Show valid play options
    table = Table(title="Valid Plays", box=box.SIMPLE)
    table.add_column("#", style="cyan", justify="center")
    table.add_column("Cards", style="white")
    table.add_column("Type", style="dim")
    
    for i, play in enumerate(valid_plays, 1):
        cards_text = Text()
        for j, card in enumerate(play):
            if j > 0:
                cards_text.append(", ")
            cards_text.append(format_card(card))
        
        play_type = {
            1: "Single",
            2: "Pair",
            3: "Triple",
            4: "Quad"
        }.get(len(play), "")
        
        table.add_row(str(i), cards_text, play_type)
    
    # Only show pass option if player can pass
    if can_pass:
        table.add_row("[dim]0[/dim]", "[dim]Pass[/dim]", "")
    
    console.print(table)
    console.print()
    
    if can_pass:
        prompt_text = "Choose a play (or 0 to pass)"
        default_val = 0
    else:
        prompt_text = "Choose a play (you must lead)"
        default_val = 1
    
    choice = IntPrompt.ask(
        prompt_text,
        default=default_val,
        console=console
    )
    
    console.print()
    
    if choice == 0:
        if can_pass:
            return None
        else:
            console.print("[red]You must play a card (cannot pass when leading)[/red]")
            console.print()
            return get_player_action(player, valid_plays, can_pass=False)
    
    if 1 <= choice <= len(valid_plays):
        return valid_plays[choice - 1]
    
    console.print("[red]Invalid choice, try again...[/red]")
    console.print()
    return get_player_action(player, valid_plays, can_pass)


def display_play(player: Player, cards: List[Card]) -> None:
    """Display a play that was made.
    
    Args:
        player: Player who made the play
        cards: Cards that were played
    """
    cards_text = Text()
    for i, card in enumerate(cards):
        if i > 0:
            cards_text.append(", ")
        cards_text.append(format_card(card))
    
    message = Text()
    message.append(f"{player.name} ", style="bold cyan")
    message.append("plays: ", style="white")
    message.append(cards_text)
    
    console.print(message)
    console.print()


def display_pass(player: Player) -> None:
    """Display that a player passed.
    
    Args:
        player: Player who passed
    """
    console.print(f"[dim]{player.name} passes[/dim]")
    console.print()


def display_trick_winner(player: Player) -> None:
    """Display the winner of a trick.
    
    Args:
        player: Player who won
    """
    console.print(Panel(
        f"[bold green]{player.name} wins the trick![/bold green]",
        border_style="green"
    ))
    console.print()


def display_round_start(round_num: int, total_rounds: int) -> None:
    """Display round start banner.
    
    Args:
        round_num: Current round number
        total_rounds: Total number of rounds
    """
    console.rule(f"[bold cyan]ROUND {round_num} of {total_rounds}[/bold cyan]")
    console.print()


def display_round_results(finished_players: List[Player]) -> None:
    """Display results of a round.
    
    Args:
        finished_players: Players in finish order
    """
    table = Table(title="Round Results", box=box.DOUBLE)
    table.add_column("Position", style="cyan", justify="center")
    table.add_column("Player", style="bold")
    table.add_column("Rank", style="yellow")
    
    for i, player in enumerate(finished_players, 1):
        rank = player.rank if player.rank else "Neutral"
        rank_style = {
            "President": "bold gold1",
            "Vice-President": "bold yellow",
            "Neutral": "white",
            "Vice-Scum": "dim yellow",
            "Scum": "dim red"
        }.get(rank, "white")
        
        table.add_row(
            str(i),
            player.name,
            Text(rank, style=rank_style)
        )
    
    console.print(table)
    console.print()


def display_card_exchange_announcement(exchanges: List[tuple]) -> None:
    """Display card exchange announcement.
    
    Args:
        exchanges: List of (from_player, to_player, num_cards) tuples
    """
    if not exchanges:
        return
    
    console.print("[bold yellow]Card Exchange Time![/bold yellow]")
    console.print()
    for from_player, to_player, num_cards in exchanges:
        console.print(f"  {from_player} → {to_player}: {num_cards} card(s)")
    console.print()


def display_cards_given(player_name: str, cards: List[Card], recipient: str) -> None:
    """Display cards being given.
    
    Args:
        player_name: Name of player giving cards
        cards: Cards being given
        recipient: Name of recipient
    """
    cards_text = Text()
    for i, card in enumerate(cards):
        if i > 0:
            cards_text.append(", ")
        cards_text.append(format_card(card))
    
    message = Text()
    message.append(f"{player_name} ", style="bold cyan")
    message.append("gives to ", style="white")
    message.append(f"{recipient}", style="bold yellow")
    message.append(": ", style="white")
    message.append(cards_text)
    
    console.print(message)
    console.print()


def get_cards_to_give_away(player: Player, num_cards: int, recipient: str) -> List[Card]:
    """Let player choose which cards to give away.
    
    Args:
        player: Player giving cards
        num_cards: Number of cards to give
        recipient: Name of recipient
        
    Returns:
        List of cards chosen
    """
    console.print(f"[bold cyan]{player.name}[/bold cyan], choose {num_cards} card(s) to give to [bold yellow]{recipient}[/bold yellow]")
    console.print()
    
    display_hand(player)
    
    # Create table of choices
    table = Table(title="Choose Cards", box=box.SIMPLE)
    table.add_column("#", style="cyan", justify="center")
    table.add_column("Card", style="white")
    
    for i, card in enumerate(player.hand, 1):
        table.add_row(str(i), format_card(card))
    
    console.print(table)
    console.print()
    
    chosen_cards = []
    for i in range(num_cards):
        while True:
            try:
                choice = IntPrompt.ask(
                    f"Choose card {i+1} of {num_cards}",
                    console=console
                )
                
                if 1 <= choice <= len(player.hand):
                    card = player.hand[choice - 1]
                    if card not in chosen_cards:
                        chosen_cards.append(card)
                        console.print(f"  Selected: {format_card(card)}")
                        console.print()
                        break
                    else:
                        console.print("[red]Card already selected, choose another[/red]")
                else:
                    console.print(f"[red]Please enter 1-{len(player.hand)}[/red]")
            except Exception:
                console.print("[red]Invalid input[/red]")
    
    return chosen_cards


def display_game_winner(player: Player) -> None:
    """Display the game winner with fanfare.
    
    Args:
        player: Winner of the game
    """
    winner_text = Text()
    winner_text.append("🎉 ", style="bold yellow")
    winner_text.append(player.name.upper(), style="bold gold1")
    winner_text.append(" WINS THE GAME! ", style="bold white")
    winner_text.append("🎉", style="bold yellow")
    
    panel = Panel(
        winner_text,
        box=box.DOUBLE,
        border_style="gold1",
        padding=(1, 2)
    )
    
    console.print()
    console.rule("[bold gold1]GAME OVER[/bold gold1]")
    console.print()
    console.print(panel)
    console.print()


def display_error(message: str) -> None:
    """Display an error message.
    
    Args:
        message: Error message to display
    """
    console.print(f"[bold red]Error:[/bold red] {message}")
    console.print()


def confirm_continue() -> bool:
    """Prompt to continue to next round.
    
    Returns:
        True if user wants to continue
    """
    return Confirm.ask(
        "[bold]Continue to next round?[/bold]",
        default=True,
        console=console
    )


def clear_screen() -> None:
    """Clear the screen and prevent scrollback."""
    import os
    # Use system clear to prevent scrollback
    os.system('clear' if os.name != 'nt' else 'cls')
    # Also use console.clear for good measure
    console.clear()


def display_starting_player(player: Player) -> None:
    """Display which player starts (has 3 of clubs).
    
    Args:
        player: Player who starts
    """
    console.print(Panel(
        f"[bold]{player.name}[/bold] has the [bold red]3♣[/bold red] and starts!",
        border_style="cyan"
    ))
    console.print()


def pause(message: str = "Press Enter to continue") -> None:
    """Pause and wait for user to press Enter.
    
    Args:
        message: Message to display
    """
    console.input(f"[dim]{message}...[/dim] ")
    console.print()
