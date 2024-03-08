import requests
import pandas as pd
from sqlalchemy import create_engine
import json


access_token = '####################'
account_id = '###################'

url = f"https://graph.facebook.com/v19.0/act_{account_id}/insights?fields=campaign_name,spend,actions,impressions,clicks,reach,conversions&level=campaign&time_increment=1&time_range={{'since':'2024-02-01','until':'2024-03-01'}}&breakdowns=gender,age&limit=100000&access_token={access_token}"

response = requests.get(url)
data = response.json()

if response.status_code == 200:
    print("Requisição bem-sucedida!")
else:
    print("Houve um erro na requisição:", response.status_code)


df = pd.json_normalize(data['data'])
for col in df.columns:
    if df[col].apply(lambda x: isinstance(x, dict) or isinstance(x, list)).any():
        df[col] = df[col].apply(lambda x: json.dumps(x) if isinstance(x, dict) or isinstance(x, list) else x)
df.head(10)

####



