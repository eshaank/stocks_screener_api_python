"""
News related API routes.
Author: Eshaan Kansagara
"""

from fastapi import APIRouter, HTTPException

from app.models import NewsItem, NewsResponse
from app.services.news_service import get_stock_news

router = APIRouter(
    prefix="/news",
    tags=["News"]
)


@router.get("/{ticker}", response_model=NewsResponse)
async def get_ticker_news(ticker: str):
    """
    Retrieve news for a specific stock ticker.
    
    Parameters:
    - ticker: Stock symbol (e.g., AAPL, MSFT)
    
    Returns:
    - List of news items with details
    """
    try:
        raw_news = get_stock_news(ticker)
        
        formatted_news = [
            NewsItem(
                date=news.get('Date', ''),
                title=news.get('Title', ''),
                url=news.get('Url', ''),
                source=news.get('Source', ''),
                category=news.get('Category', '')
            )
            for news in raw_news
        ]
        
        return NewsResponse(ticker=ticker, news=formatted_news)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 