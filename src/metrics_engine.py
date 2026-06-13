import pandas as pd

def calculate_financial_ratios(ratios_dataframe, tickers):

    print("Calculating comprehensive financial metrics across all 4 pillars...")
    
    try: 
        for ticker in tickers: 
            df = ratios_dataframe[ticker]
            df = df.sort_values(by="Year", ascending=True).reset_index(drop=True)
            
            # financial pillars calculation
            df["Revenue_Growth_Pct"] = df["Total Revenue"].pct_change() * 100 
            df["Net_Income_Growth_Pct"] = df["Net Income"].pct_change() * 100
            df["Operating_Margin_Pct"] = (df["Operating Income"] / df["Total Revenue"]) * 100
            df["ROE_Pct"] = (df["Net Income"] / df["Stockholders Equity"]) * 100
            df["Current_Ratio"] = df["Current Assets"] / df["Current Liabilities"]
            df["Debt_to_Equity"] = df["Total Debt"] / df["Stockholders Equity"]
            df["Calculated_EPS"] = df["Net Income"] / df["Basic Average Shares"] 
            df["PE_Ratio"] = df["Current_Price"] / df["Calculated_EPS"]
            
            ratios_dataframe[ticker] = df 
            
        print(" All quantitative ratios have been generated.")
    except Exception as e:
        print(f" Couldn't do the calculation because: {e}")
        
    return ratios_dataframe


def build_benchmark_table(ratios_dataframe):

print("Creating master table and calculating sector benchmarks...")
for ticker, df in ratios_dataframe.items():
    print(ticker, df["Company"].unique())
# 1. Stack all individual company dataframes vertically
# pd.concat takes the dataframes from our dictionary values with the values method and stitches them together and resetting the index with ignore_index
master_table = pd.concat(ratios_dataframe.values(), ignore_index=True)
print(master_table["Company"].value_counts())
# 2. Filter down to only the columns we actually care about for our report
reporting_columns = ["Company", "Year", "Revenue_Growth_Pct", "Net_Income_Growth_Pct", "Operating_Margin_Pct", 
                     "ROE_Pct", "Current_Ratio", "Debt_to_Equity", "PE_Ratio"]
clean_master_table = master_table[reporting_columns]
clean_master_table = clean_master_table[clean_master_table['Year'].isin([2022,2023,2024,2025])]

# 3. Calculate the peer group's average for each year
# We group by "Year" so we don't mix 2023 data with 2024 data.
# We exclude the 'Company' and 'Year' columns because you can't calculate the mathematical average of text strings or dates
numeric_cols = [col for col in reporting_columns if col != "Company" and col != "Year"]
peers_averages = clean_master_table.groupby("Year")[numeric_cols].mean().reset_index()

# Tag this new dataframe so we know it represents the whole sector
peers_averages["Company"] = "PEER_AVG"

# 4. Combine companies and peers averages
# We stack the peers averages right below the company data
final_benchmark_table = pd.concat([clean_master_table, peers_averages], ignore_index=True)

# Sort by Year and Company so it's beautiful and easy to read side-by-side
final_benchmark_table = final_benchmark_table.sort_values(by=["Year", "Company"]).reset_index(drop=True)

print("The peers benchmark table is fully built.")
print("1. Liste des entreprises dans le dictionnaire :", list(ratios_dataframe.keys()))
print(final_benchmark_table)
#TO CHECK THAT ALL TICKERS' DATA HAVE BEEN UPLOADED
for ticker, df in ratios_dataframe.items():
    print("\n", ticker)
    print(df[["Company","Year"]].head())
