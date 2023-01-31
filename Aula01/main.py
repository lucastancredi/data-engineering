import requests
import pandas as pd
import collections
import sys

url = 'https://servicebus2.caixa.gov.br/portaldeloterias/api/resultados?modalidade=Lotof%C3%A1cil'

sys.argv(url)

r = requests.get(url, verify=False)

r.text
r_text = r.text.replace('\r\n', '')
r_text = r.text.replace('\\r\\n', '')
r_text = r.text.replace('{\r\n  "html": "', '')


df = pd.read_html(r_text)

type(df)
type(df[0])
df1 = df
df = df[0].copy()

new_columns = df.columns
new_columns = list(i.replace('\\r\\n', '')for i in new_columns)
new_columns
df.columns = new_columns
df = df.dropna()

df