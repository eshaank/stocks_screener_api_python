# Stocks Scanner API

A professional REST API for scanning stocks, retrieving SEC filings, news, and analyzing market data.

## Features

Current Features:
- ✅ SEC Filings: Retrieve latest SEC filings for any stock ticker
- ✅ Stock News: Get recent news articles for any stock ticker
- 🔜 High volume stock detection
- 🔜 High percent change detection

## Project Structure

```
stocks_scanner_api/
├── app/
│   ├── api/            # API route handlers
│   │   ├── news.py     # News endpoints
│   │   └── sec.py      # SEC filings endpoints
│   ├── services/       # Business logic
│   │   ├── news_service.py
│   │   └── sec_service.py
│   ├── models.py       # Data models
│   └── config.py       # Configuration
├── main.py             # Application entry point
├── requirements.txt
└── README.md
```

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

## API Documentation

### Root Endpoint
```
GET /
```
Returns basic API information and available endpoints.

### SEC Filings
```
GET /sec-filings/{ticker}
```
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

### Stock News
```
GET /news/{ticker}
```
Retrieves recent news articles for a specific stock ticker.

Parameters:
- `ticker`: Stock symbol (e.g., AAPL, MSFT)

Response example:
```json
{
    "ticker": "AAPL",
    "news": [
        {
            "date": "2024-01-30",
            "title": "Example News Title",
            "link": "https://example.com/news",
            "source": "Example Source",
            "description": "News description..."
        }
    ]
}
```

## Error Handling

The API uses standard HTTP status codes:
- `200`: Successful request
- `404`: Resource not found
- `500`: Server error (includes detailed error message)

Common error scenarios:
- Missing API token
- Invalid stock ticker
- Network issues with external data providers

## Development

This API is structured for easy expansion and future frontend integration. New features will be added as separate endpoints following REST principles.

### Adding New Features
1. Create new models in `app/models.py`
2. Add business logic in `app/services/`
3. Create route handlers in `app/api/`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License - See LICENSE file for details

## Author

Eshaan Kansagara 