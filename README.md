# Stock Scanner CLI

A command-line interface for scanning stocks, retrieving SEC filings, and analyzing market news using Finviz API.

## Installation

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

## Usage

Start the CLI:
```bash
python cli.py
```

### Available Commands

1. `/news TICKER`
   - Shows news for a specific stock ticker
   - Displays two tables:
     1. Today's news (if available)
     2. 10 most recent news items
   - Example: `/news AAPL`
   ```
   News Information:
   • Ticker: AAPL
   • Current Date (EST): 2024-01-31
   • Today's News Items: 5
   • Total News Items: 50

   📰 Today's News for AAPL (2024-01-31 EST)
   [Table with today's news]

   📰 10 Most Recent News Items for AAPL
   [Table with recent news]
   ```

2. `/sec TICKER`
   - Shows SEC filings for a specific stock ticker
   - Displays filings in chronological order (oldest to latest)
   - Example: `/sec AAPL`
   ```
   SEC Filings Information:
   • Total Filings: 154
   • Oldest: 11/19/2018
   • Most Recent: 1/31/2025

   📄 SEC Filings for AAPL (Oldest → Latest)
   [Table with SEC filings]
   ```

3. `/help`
   - Shows available commands and usage information

4. `/exit`
   - Exits the application

## Display Features

### News Display
- Time shown in EST timezone
- Full date and time format: MM/DD/YYYY HH:MM AM/PM
- Color-coded information:
  - 🔵 Time (cyan)
  - 🟢 Title (green)
  - 🟡 Source (yellow)
  - 🔵 URL (blue)
  - 🟣 Category (magenta)

### SEC Filings Display
- Chronological order (oldest to latest)
- Color-coded information:
  - 🔵 Filing Date (cyan)
  - 🟡 Form Type (yellow)
  - 🟢 Description (green)
  - 🔵 URL (blue)

## Error Handling

The CLI provides clear error messages for common issues:
- Invalid ticker symbols
- Network connectivity issues
- Missing API token
- Data parsing errors

## Tips

1. Use uppercase or lowercase for ticker symbols (automatically converted to uppercase)
2. Press Ctrl+C at any time to exit the application
3. Use the up arrow key to recall previous commands


## Author

Eshaan Kansagara 