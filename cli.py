#!/usr/bin/env python3
"""
Command Line Interface for Stock Scanner
Author: Eshaan Kansagara
"""

import click
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from datetime import datetime
from app.services.news_service import get_stock_news
from app.services.sec_service import get_sec_filings

console = Console()


def parse_filing_date(date_str: str) -> datetime:
    """Parse filing date string into datetime object."""
    try:
        return datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        return datetime.min


def print_welcome():
    """Print welcome message and available commands."""
    console.print(Panel(
        "[bold green]Welcome to Stock Scanner CLI![/bold green]\n\n"
        "[yellow]Available commands:[/yellow]\n"
        "• [cyan]/news TICKER[/cyan] - Get latest news for a stock\n"
        "• [cyan]/sec TICKER[/cyan]  - Get SEC filings for a stock\n"
        "• [cyan]/exit[/cyan]        - Exit the application\n"
        "• [cyan]/help[/cyan]        - Show this help message",
        title="🚀 Stock Scanner",
        border_style="blue"
    ))


@click.command()
def cli():
    """Stock Scanner Command Line Interface."""
    print_welcome()
    
    while True:
        try:
            # Get user input
            command = Prompt.ask("\n[bold green]Enter command[/bold green]")
            
            # Split command into parts
            parts = command.strip().split()
            if not parts:
                continue
                
            cmd = parts[0].lower()
            
            # Handle commands
            if cmd == '/exit':
                console.print("[yellow]Goodbye! 👋[/yellow]")
                break
                
            elif cmd == '/help':
                print_welcome()
                
            elif cmd == '/news':
                if len(parts) < 2:
                    console.print("[red]Please provide a ticker symbol. Example: /news AAPL[/red]")
                    continue
                    
                ticker = parts[1].upper()
                try:
                    get_stock_news(ticker)
                except Exception as e:
                    console.print(f"[red]Error: {str(e)}[/red]")
                    
            elif cmd == '/sec':
                if len(parts) < 2:
                    console.print("[red]Please provide a ticker symbol. Example: /sec AAPL[/red]")
                    continue
                    
                ticker = parts[1].upper()
                try:
                    filings = get_sec_filings(ticker)
                    
                    # Print debug info
                    console.print("\n[bold blue]SEC Filings Information:[/bold blue]")
                    console.print(f"[cyan]• Total Filings:[/cyan] {len(filings)}")
                    if filings:
                        console.print(f"[cyan]• Oldest:[/cyan] {filings[0].get('Filing Date', '')}")
                        console.print(f"[cyan]• Most Recent:[/cyan] {filings[-1].get('Filing Date', '')}")
                    
                    # Create a table to display SEC filings
                    from rich.table import Table
                    table = Table(
                        title=f"📄 SEC Filings for {ticker} (Oldest → Latest)",
                        show_lines=True,
                        title_style="bold magenta",
                        header_style="bold white on blue"
                    )
                    
                    table.add_column("Filing Date", style="cyan", no_wrap=True)
                    table.add_column("Form", style="yellow", no_wrap=True)
                    table.add_column("Description", style="green")
                    table.add_column("URL", style="blue", overflow="fold")
                    
                    for filing in filings:
                        table.add_row(
                            filing.get('Filing Date', ''),
                            filing.get('Form', ''),
                            filing.get('Description', ''),
                            filing.get('Filing', '')
                        )
                    
                    console.print(table)
                    
                except Exception as e:
                    console.print(f"[red]Error: {str(e)}[/red]")
            
            else:
                console.print("[red]Unknown command. Type /help for available commands.[/red]")
                
        except KeyboardInterrupt:
            console.print("\n[yellow]Goodbye! 👋[/yellow]")
            break
        except Exception as e:
            console.print(f"[red]Error: {str(e)}[/red]")


if __name__ == "__main__":
    cli() 