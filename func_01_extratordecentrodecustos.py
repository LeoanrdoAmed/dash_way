import requests
import pandas as pd
import sqlite3

url = "https://services.contaazul.com/finance-pro/v1/cost-centers?search=&page_size=10&page=1&quick_filter=ACTIVE"
headers = {
    'accept': 'application/json',
    'content-type': 'application/json',
    'user-agent': 'Mozilla/5.0',
    'x-authorization': 'SUA_CHAVE_AQUI'
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()
    base_cc = pd.DataFrame(data["items"])
    new_row = pd.DataFrame([{
        "id": "NONE", "version": "NONE", "code": "NONE", "name": "NONE", "parent": "NONE", "active": "NONE"
    }])
    base_cc = pd.concat([base_cc, new_row], ignore_index=True)
    base_cc.rename(columns={'id': 'centroCusto'}, inplace=True)

    conn = sqlite3.connect("/data/dashway.db")
    base_cc.to_sql("centros_de_custo", conn, if_exists="replace", index=False)
    conn.close()
    print("Base centros de custo salva com sucesso.")
else:
    print(f"Erro na requisição: {response.status_code}")