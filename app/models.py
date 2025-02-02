"""
Pydantic models for request/response validation.
Author: Eshaan Kansagara
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


class NewsItem(BaseModel):
    """Model representing a single news item."""
    date: str
    title: str
    url: str
    source: str
    category: str


class NewsResponse(BaseModel):
    """Response model for news endpoint."""
    ticker: str
    news: List[NewsItem] 