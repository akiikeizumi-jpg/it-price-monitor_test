import requests
import json
import os

APP_ID = os.environ["ESTAT_APP_ID"]

url = (
    "https://api.e-stat.go.jp/rest/3.0/app/json/getStatsData"
    f"?appId={APP_ID}"
    "&statsDataId=0003425913"
    "&metaGetFlg=Y"
    "&cntGetFlg=N"
)

r = requests.get(url)

data = r.json()

print(json.dumps(data, indent=2, ensure_ascii=False))
