import requests
import pandas as pd
import sqlite3

url = "https://services.contaazul.com/contaazul-bff/dashboard/v1/financial-accounts"
headers = {
    'accept': 'application/json',
    'content-type': 'application/json',
    'user-agent': 'Mozilla/5.0',
    'x-authorization': 'SUA_CHAVE_AQUI'
}

response = requests.get(url, headers=headers)
data = response.json()
base_cb = pd.DataFrame(data["dashboardBankAccounts"])
base_cb['ativo'] = base_cb['bankAccount'].apply(lambda x: x['ativo'])
base_cb['nmBanco'] = base_cb['bankAccount'].apply(lambda x: x['nmBanco'])
base_cb['uuid'] = base_cb['bankAccount'].apply(lambda x: x['uuid'])
base_cb.rename(columns={'uuid': 'financialAccountId'}, inplace=True)
filtered_df = base_cb[['ativo','nmBanco', 'financialAccountId']]

conn = sqlite3.connect("/data/dashway.db")
filtered_df.to_sql("contas_bancarias", conn, if_exists="replace", index=False)
conn.close()
print("Base contas bancárias salva com sucesso.")