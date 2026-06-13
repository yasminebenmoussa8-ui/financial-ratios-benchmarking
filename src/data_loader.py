import pandas as pd
import yfinance as yf

def fetch_financial_statements (tickers) :
# list of benchmark companies - tech companies
tickers = ["MSFT", "AAPL", "GOOGL", "META"]
ratios_dataframe = {}  # storage dictionary

    # Loop directly through the input variable 'tickers'
for ticker in tickers:
    print(f" data retrieval for {ticker}...")
        
    # 1. connection to financial API
    company_data = yf.Ticker(ticker)
    
    # 2. Download of 3 financial statements (historical annual data)
    income_statement = company_data.financials.T
    balance_sheet = company_data.balance_sheet.T
    cash_flow = company_data.cashflow.T
    
    # price retrieval in real time
    current_price = company_data.info.get("currentPrice")
    
    # 4. index cleaning
    income_statement.index = pd.to_datetime(income_statement.index).year
    balance_sheet.index = pd.to_datetime(balance_sheet.index).year
    cash_flow.index = pd.to_datetime(cash_flow.index).year
        
    # 5. Combination of the three statements with "combine_first" method
    merged_df = income_statement.combine_first(balance_sheet)
    full_financials_df = merged_df.combine_first(cash_flow)
    
    # 6. Add two columns corresponding to the current price, and the ticker
    full_financials_df['Current_Price'] = current_price
    full_financials_df['Company'] = ticker
        
    # retrieve the year column to facilitate visualization afterward
    full_financials_df = full_financials_df.reset_index().rename(columns={"index": "Year"})
    
    # we store each company's table in the dictionary before ending the loop
    ratios_dataframe[ticker] = full_financials_df.copy()
    
print("\n gross data are ready.")
