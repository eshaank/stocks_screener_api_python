"""
Pydantic models for request/response validation.
"""

from typing import List
from pydantic import BaseModel


class SECFiling(BaseModel):
    """Model representing a single SEC filing."""
    filing_date: str
    report_date: str
    form: str
    description: str
    filing_url: str
    document_url: str


class SECFilingsResponse(BaseModel):
    """Response model for SEC filings endpoint."""
    ticker: str
    filings: List[SECFiling] 