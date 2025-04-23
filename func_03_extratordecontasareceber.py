import requests
import json
import pandas as pd
import sqlite3

conn = sqlite3.connect("/data/dashway.db")
centros = pd.read_sql("SELECT * FROM centros_de_custo", conn)
conn.close()
cost_center_ids = centros["centroCusto"]

all_items = []
url = "https://services.contaazul.com/finance-pro-reader/v1/installment-view"

for cost_center_id in cost_center_ids:
    page = 1
    page_size = 100
    while True:
        print(f"Consultando página {page}...")
        payload = json.dumps({
            "dateFrom": None,
            "dateTo": None,
            "search": None,
            "quickFilter": "ALL",
            "costCenterIds": [cost_center_id],
            "type": "REVENUE"
        })
        headers = {
            'accept': 'application/json',
            'content-type': 'application/json',
            'user-agent': 'Mozilla/5.0',
            'x-authorization': 'SUA_CHAVE_AQUI'
        }
        response = requests.post(f"{url}?page={page}&page_size={page_size}", headers=headers, data=payload)
        if response.status_code == 200:
            data = response.json()
            if 'totalItems' in data and 'items' in data:
                items = data['items']
                for item in items:
                    item['centroCusto'] = cost_center_id
                all_items.extend(items)
                if page >= ((data['totalItems'] - 1) // page_size + 1):
                    break
                page += 1
            else:
                break
        else:
            break

df = pd.DataFrame(all_items).rename(columns={"id": "id_lancamento"})
df_exp = pd.json_normalize(df['financialAccount']).rename(columns={"id": "financialAccountId2"})
df_final = pd.concat([df, df_exp], axis=1).rename(columns={
    "financialAccount": "financialAccountId_base",
    "financialAccountId2": "financialAccountId"
})

conn = sqlite3.connect("/data/dashway.db")
df_final.to_sql("contas_receber", conn, if_exists="replace", index=False)
conn.close()
print("Base contas a receber salva com sucesso.")