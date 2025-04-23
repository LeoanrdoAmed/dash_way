import requests
import pandas as pd

url = "https://services.contaazul.com/contaazul-bff/dashboard/v1/financial-accounts"

payload = {}
headers = {
    'accept': 'application/json',
    'content-type': 'application/json',
    'user-agent': 'Mozilla/5.0',
    'x-authorization': 'SUA_CHAVE_AQUI'
}

response = requests.request("GET", url, headers=headers, data=payload)
data = response.json()
base_cb = pd.DataFrame(data["dashboardBankAccounts"])
base_cb['ativo'] = base_cb['bankAccount'].apply(lambda x: x['ativo'])
base_cb['nmBanco'] = base_cb['bankAccount'].apply(lambda x: x['nmBanco'])
base_cb['uuid'] = base_cb['bankAccount'].apply(lambda x: x['uuid'])
base_cb.rename(columns={'uuid': 'financialAccountId'}, inplace=True)
filtered_df = base_cb[['ativo','nmBanco', 'financialAccountId']]
filtered_df.to_json("data/base_02_cb.json")
print("Consulta de base CB finalizada com sucesso.")