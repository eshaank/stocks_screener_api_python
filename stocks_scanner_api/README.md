# Stocks Scanner API

A professional REST API for scanning stocks, retrieving SEC filings, and analyzing market data.

## Features

- Retrieve SEC filings for any stock ticker
- (Coming soon) High volume stock detection
- (Coming soon) High percent change detection
- (Coming soon) News aggregation

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory with your Finviz API token:
```
FINVIZ_API_TOKEN=your_token_here
```

## Running the API

Start the API server:
```bash
python main.py
```

The API will be available at `http://localhost:8000`

## API Endpoints

### GET /
Returns basic API information and available endpoints.

### GET /sec-filings/{ticker}
Retrieves SEC filings for a specific stock ticker.

Parameters:
- `ticker`: Stock symbol (e.g., AAPL, MSFT)

Response example:
```json
{
    "ticker": "AAPL",
    "filings": [
        {
            "filing_date": "2024-01-30",
            "report_date": "2023-12-30",
            "form": "10-Q",
            "description": "Quarterly Report",
            "filing_url": "https://...",
            "document_url": "https://..."
        }
    ]
}
```

## Development

This API is structured for easy expansion and future frontend integration. New features will be added as separate endpoints following REST principles. 