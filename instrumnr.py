import pandas as pd
import requests

# Zerodha ka public instrument link
url = "https://api.kite.trade/instruments"

print("Downloading instrument list...")
response = requests.get(url)

# CSV data ko file mein save karna ya direct pandas mein load karna
with open("instruments.csv", "wb") as f:
    f.write(response.content)

# Data load karein
df = pd.read_csv("instruments.csv")

# Sirf Stocks (Equity) filter karne ke liye:
# 1. Exchange 'NSE' ya 'BSE' ho
# 2. Segment 'NSE' ya 'BSE' ho (F&O wale segments alag hote hain)
# 3. Instrument_type 'EQ' ho
stocks_df = df[(df['exchange'] == 'NSE') & (df['instrument_type'] == 'EQ')]

# Sirf kaam ke columns dekhne ke liye
final_list = stocks_df[['tradingsymbol', 'name', 'last_price', 'tick_size']]

print(f"Total stocks found: {len(final_list)}")
print(final_list.head())

# Agar Excel/CSV mein save karna ho
# final_list.to_csv("zerodha_stocks_only.csv", index=False)