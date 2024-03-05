import requests
import pandas as pd
from sqlalchemy import create_engine
import json


access_token = 'EAAUTzw5r6GEBO3SZAT6qZBzxZB7jwwb3mpwitMdzrn3YlSkP4HI7m7o2v2FU7UYc6zAK990GwUCjfCa1SP85fubGzbfLS2Ez5cOZBCWrzlKa8GZCdBZCZBYOvsclqsLz1fbHJ4xQWEG8dkSwzR5wj9gpD8puF8Ca3Dm1IiuIBHpOPJaMWlm2zGOwtV71ncysfVJ'
account_id = '1492131828292570'

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

database_username = 'postgres'
database_password = '1234'
database_ip = '62.72.8.194'
database_name = 'datalake'
schema_name = 'fb_ads' 
database_connection = f'postgresql://{database_username}:{database_password}@{database_ip}/{database_name}'
engine = create_engine(database_connection)
df.to_sql('kui_gender_age', engine, index=False, if_exists='replace', schema=schema_name)



