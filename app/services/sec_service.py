"""
Service for handling SEC filings related operations.
"""

import csv
import io
from typing import List
import requests
from fastapi import HTTPException
from datetime import datetime

from app.config import FINVIZ_API_TOKEN, FINVIZ_SEC_FILINGS_URL


def parse_filing_date(date_str: str) -> datetime:
    """Parse filing date string into datetime object."""
    try:
        # Handle M/D/YYYY format
        return datetime.strptime(date_str, '%m/%d/%Y')
    except ValueError as e:
        print(f"Warning: Could not parse date {date_str}: {str(e)}")
        return datetime.min


def get_sec_filings(ticker: str) -> List[dict]:
    """
    Fetch SEC filings for a given ticker from Finviz.
    
    Args:
        ticker: Stock symbol to fetch filings for
        
    Returns:
        List of dictionaries containing filing information
        
    Raises:
        HTTPException: If API token is not configured or request fails
    """
    if not FINVIZ_API_TOKEN:
        raise HTTPException(status_code=500, detail="FINVIZ_API_TOKEN not configured")
    
    url = f"{FINVIZ_SEC_FILINGS_URL}?t={ticker}&o=-filingDate&auth={FINVIZ_API_TOKEN}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        # Parse CSV data
        csv_reader = csv.reader(io.StringIO(response.text))
        headers = next(csv_reader)
        filings = [dict(zip(headers, row)) for row in csv_reader]
        
        # Sort filings by date (oldest first)
        filings.sort(
            key=lambda x: parse_filing_date(x.get('Filing Date', '')),
            reverse=False  # Oldest first
        )
        
        return filings
        
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch SEC filings: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing SEC filings: {str(e)}") 