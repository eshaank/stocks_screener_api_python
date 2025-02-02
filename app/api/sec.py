"""
SEC filings related API routes.
"""

from fastapi import APIRouter, HTTPException
from datetime import datetime

from app.models import SECFiling, SECFilingsResponse
from app.services.sec_service import get_sec_filings

router = APIRouter(
    prefix="/sec-filings",
    tags=["SEC Filings"]
)


def parse_filing_date(date_str: str) -> datetime:
    """Parse filing date string into datetime object."""
    try:
        return datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        return datetime.min


@router.get("/{ticker}", response_model=SECFilingsResponse)
async def get_ticker_sec_filings(ticker: str):
    """
    Retrieve SEC filings for a specific stock ticker.
    
    Parameters:
    - ticker: Stock symbol (e.g., AAPL, MSFT)
    
    Returns:
    - List of SEC filings with filing details
    """
    try:
        raw_filings = get_sec_filings(ticker)
        
        # Convert to list of SECFiling objects
        formatted_filings = [
            SECFiling(
                filing_date=filing.get('Filing Date', ''),
                report_date=filing.get('Report Date', ''),
                form=filing.get('Form', ''),
                description=filing.get('Description', ''),
                filing_url=filing.get('Filing', ''),
                document_url=filing.get('Document', '')
            )
            for filing in raw_filings
        ]
        
        # Sort filings by date (oldest first, latest at bottom)
        formatted_filings.sort(
            key=lambda x: parse_filing_date(x.filing_date),
            reverse=False
        )
        
        return SECFilingsResponse(ticker=ticker, filings=formatted_filings)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 