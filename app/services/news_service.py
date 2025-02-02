"""
Service for handling stock news related operations.
Author: Eshaan Kansagara
"""

import csv
import io
from typing import List, Tuple
import requests
from fastapi import HTTPException
from rich.console import Console
from rich.table import Table
from rich import print as rprint
from rich.panel import Panel
from rich.traceback import install
from datetime import datetime
import pytz

from app.config import FINVIZ_API_TOKEN, FINVIZ_NEWS_URL

# Install rich traceback handler
install(show_locals=True)

# Initialize Rich console
console = Console()


def get_current_est_date():
    """Get current date in EST timezone."""
    est = pytz.timezone('US/Eastern')
    return datetime.now(est).date()


def parse_news_date(date_str: str) -> datetime:
    """Parse news date string into datetime object."""
    try:
        # Finviz date format is: "2025-02-01 16:13:03"
        return datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
    except ValueError as e:
        console.print(f"[yellow]Warning: Could not parse date {date_str}[/yellow]")
        return None


def format_news_time(date_str: str) -> str:
    """Format the news time for display."""
    try:
        dt = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
        return dt.strftime('%m/%d/%Y %I:%M %p')  # Format as "01/31/2024 03:45 PM"
    except ValueError:
        return date_str


def print_error_to_terminal(error: str, ticker: str):
    """
    Print error information in a formatted way.
    
    Args:
        error: Error message
        ticker: Stock ticker symbol
    """
    console.print("\n")
    console.print(Panel(
        f"[bold red]Error fetching news for {ticker}[/bold red]\n\n"
        f"[yellow]{error}[/yellow]",
        title="❌ Error Details",
        border_style="red"
    ))
    console.print("\n")


def create_news_table(news_items: List[dict], title: str) -> Table:
    """Create a formatted table for news items."""
    table = Table(
        title=title,
        show_lines=True,
        title_style="bold magenta",
        header_style="bold white on blue"
    )
    
    table.add_column("Time", style="cyan", no_wrap=True, justify="right")
    table.add_column("Title", style="green")
    table.add_column("Source", style="yellow", no_wrap=True)
    table.add_column("URL", style="blue", overflow="fold")
    table.add_column("Category", style="magenta", no_wrap=True)
    
    for item in news_items:
        table.add_row(
            format_news_time(item.get('Date', '')),
            item.get('Title', ''),
            item.get('Source', ''),
            item.get('URL', ''),
            item.get('Category', '')
        )
    
    return table


def print_news_to_terminal(news_data: List[dict], ticker: str):
    """
    Print news data in a beautifully formatted table to the terminal.
    
    Args:
        news_data: List of news items
        ticker: Stock ticker symbol
    """
    # Get current EST date
    current_date = get_current_est_date()
    
    # Sort all news by date (most recent first)
    news_data.sort(
        key=lambda x: parse_news_date(x.get('Date', '')) or datetime.min,
        reverse=True
    )
    
    # Filter news for current date
    current_news = [
        news for news in news_data 
        if parse_news_date(news.get('Date', '')).date() == current_date
    ]
    
    # Get 10 most recent news items
    recent_news = news_data[:10]
    
    # Print debug information
    console.print("\n[bold blue]News Information:[/bold blue]")
    console.print(f"[cyan]• Ticker:[/cyan] {ticker}")
    console.print(f"[cyan]• Current Date (EST):[/cyan] {current_date.strftime('%Y-%m-%d')}")
    console.print(f"[cyan]• Today's News Items:[/cyan] {len(current_news)}")
    console.print(f"[cyan]• Total News Items:[/cyan] {len(news_data)}")
    
    # Print today's news if available
    if current_news:
        table = create_news_table(
            current_news,
            f"📰 Today's News for {ticker} ({current_date.strftime('%Y-%m-%d')} EST)"
        )
        console.print("\n")
        console.print(table)
    else:
        console.print(Panel(
            f"[yellow]No news found for {ticker} on {current_date.strftime('%Y-%m-%d')} (EST)[/yellow]",
            title="ℹ️ Today's News",
            border_style="yellow"
        ))
    
    # Print 10 most recent news items
    if recent_news:
        table = create_news_table(
            recent_news,
            f"📰 10 Most Recent News Items for {ticker}"
        )
        console.print("\n")
        console.print(table)


def get_stock_news(ticker: str) -> List[dict]:
    """
    Fetch news for a given ticker from Finviz.
    
    Args:
        ticker: Stock symbol to fetch news for
        
    Returns:
        List of dictionaries containing news information
        
    Raises:
        HTTPException: If API token is not configured or request fails
    """
    try:
        if not FINVIZ_API_TOKEN:
            error_msg = "FINVIZ_API_TOKEN not configured in .env file"
            print_error_to_terminal(error_msg, ticker)
            raise HTTPException(status_code=500, detail=error_msg)
        
        url = f"{FINVIZ_NEWS_URL}?v=3&t={ticker}&c=1&auth={FINVIZ_API_TOKEN}"
        
        response = requests.get(url)
        response.raise_for_status()
        
        # Parse CSV data
        csv_reader = csv.reader(io.StringIO(response.text))
        headers = next(csv_reader)
        data = [dict(zip(headers, row)) for row in csv_reader]
        
        # Print the formatted news to terminal
        print_news_to_terminal(data, ticker)
        
        return data
        
    except requests.RequestException as e:
        error_msg = f"Failed to fetch news: {str(e)}"
        print_error_to_terminal(error_msg, ticker)
        raise HTTPException(status_code=500, detail=error_msg)
    except Exception as e:
        error_msg = f"Error processing news data: {str(e)}"
        print_error_to_terminal(error_msg, ticker)
        raise HTTPException(status_code=500, detail=error_msg) 