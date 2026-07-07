import os
import pandas as pd
import requests
from datetime import datetime

# ======================
# 設定
# ======================

ESTAT_APP_ID = os.environ["ESTAT_APP_ID"]

ESTAT_STATS_ID = "0003427113"

# ======================
# 為替取得
# ======================

def get_usd_jpy():

    url = "https://open.er-api.com/v6/latest/USD"

    r = requests.get(url, timeout=30)

    data = r.json()

    return float(data["rates"]["JPY"])


# ======================
# CPI取得
# ======================

def get_cpi():

    url = (
        "https://api.e-stat.go.jp/rest/3.0/app/json/getStatsData"
        f"?appId={ESTAT_APP_ID}"
        f"&statsDataId={ESTAT_STATS_ID}"
    )

    r = requests.get(url, timeout=60)

    data = r.json()

    values = (
        data["GET_STATS_DATA"]
        ["STATISTICAL_DATA"]
        ["DATA_INF"]
        ["VALUE"]
    )

    latest = values[-1]

    return latest["$"]


# ======================
# メイン
# ======================

today = datetime.now().strftime("%Y-%m-%d")

usd_jpy = get_usd_jpy()

try:
    cpi = get_cpi()
except Exception as e:
    print("CPI取得失敗:", e)
    cpi = None

new_row = pd.DataFrame([
    {
        "date": today,
        "usd_jpy": usd_jpy,
        "cpi": cpi
    }
])

try:

    old = pd.read_csv("data/market_data.csv")

    if today not in old["date"].astype(str).values:

        df = pd.concat(
            [old, new_row],
            ignore_index=True
        )

    else:

        print("本日のデータは既に登録済み")

        df = old

except FileNotFoundError:

    df = new_row

df.to_csv(
    "data/market_data.csv",
    index=False
)

print(df.tail())
