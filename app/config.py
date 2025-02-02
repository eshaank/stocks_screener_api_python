"""
Application configuration and environment variables.
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration
API_TITLE = "Stocks Scanner API"
API_DESCRIPTION = "API for scanning stocks, retrieving SEC filings, and analyzing market data"
API_VERSION = "1.0.0"

# External API tokens
FINVIZ_API_TOKEN = os.getenv("FINVIZ_API_TOKEN")

# API URLs
FINVIZ_SEC_FILINGS_URL = "https://elite.finviz.com/export/latest-filings"
FINVIZ_NEWS_URL = "https://elite.finviz.com/news_export.ashx" 