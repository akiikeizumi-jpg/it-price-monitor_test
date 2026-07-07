import pandas as pd
from datetime import datetime
import requests

url = "https://open.er-api.com/v6/latest/USD"

res = requests.get(url)
rate = res.json()["rates"]["JPY"]

today = datetime.today().strftime("%Y-%m-%d")

new_data = pd.DataFrame([
    {
        "date": today,
        "usd_jpy": rate,
        "dram": "",
        "nand": ""
    }
])

try:
    old = pd.read_csv("data/market_data.csv")
    df = pd.concat([old, new_data])
except:
    df = new_data

df.to_csv(
    "data/market_data.csv",
    index=False
)
