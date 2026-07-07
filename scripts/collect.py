import pandas as pd
from datetime import datetime
import requests

# ==========================
# 設定
# ==========================

ESTAT_APP_ID = "ここにe-StatのappIdを設定"

# CPIデータ取得用
# 実際のstatsDataIdは後で確定させる
ESTAT_STATS_ID = "0003427113"


# ==========================
# 為替取得
# ==========================

def get_usd_jpy():

    url = "https://open.er-api.com/v6/latest/USD"

    res = requests.get(url, timeout=30)

    data = res.json()

    return float(data["rates"]["JPY"])


# ==========================
# CPI取得
# ==========================

def get_cpi():

    try:

        url = (
            "https://api.e-stat.go.jp/rest/3.0/app/json/getStatsData"
            f"?appId={ESTAT_APP_ID}"
            f"&statsDataId={ESTAT_STATS_ID}"
        )

        res = requests.get(url, timeout=30)

        data = res.json()

        values = data["GET_STATS_DATA"]["STATISTICAL_DATA"]["DATA_INF"]["VALUE"]

        latest = values[-1]

        return latest["$"]

    except Exception as e:

        print(f"CPI取得失敗: {e}")

        return None


# ==========================
# CSV保存
# ==========================

def save_data():

    today = datetime.today().strftime("%Y-%m-%d")

    usd_jpy = get_usd_jpy()

    cpi = get_cpi()

    new_data = pd.DataFrame([
        {
            "date": today,
            "usd_jpy": usd_jpy,
            "cpi": cpi,
            "dram": "",
            "nand": ""
        }
    ])

    try:

        old = pd.read_csv("data/market_data.csv")

        if today not in old["date"].astype(str).values:

            df = pd.concat(
                [old, new_data],
                ignore_index=True
            )

        else:

            print("本日のデータは既に登録済み")

            df = old

    except FileNotFoundError:

        df = new_data

    df.to_csv(
        "data/market_data.csv",
        index=False
    )

    print("保存完了")


# ==========================
# 実行
# ==========================

if __name__ == "__main__":

    save_data()
