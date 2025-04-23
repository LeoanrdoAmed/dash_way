import requests
import pandas as pd

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
    base_cc = pd.concat([base_cc, pd.DataFrame([{
        "id": "NONE", "version": "NONE", "code": "NONE", "name": "NONE", "parent": "NONE", "active": "NONE"
    }])], ignore_index=True)
    base_cc.rename(columns={'id': 'centroCusto'}, inplace=True)
    base_cc.to_json("/data/base_01_cc.json")
    print("Consulta de base CC finalizada com sucesso.")
else:
    print(f"Erro na requisição: {response.status_code}")