import requests
import json
import pandas as pd

url = "https://services.contaazul.com/finance-pro-reader/v1/installment-view"
all_items = []

# Lendo a lista de centros de custo
base_centros_de_custos = r"data/data/base_01_cc.json"
centro_custo_json = pd.read_json(base_centros_de_custos)
cost_center_ids = centro_custo_json["centroCusto"]

# Iterando sobre cada centro de custo
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
            "type": "REVENUE",
        })

        headers = {
            'accept': 'application/json',
            'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
            'content-type': 'application/json',
            'origin': 'https://app.contaazul.com',
            'priority': 'u=1, i',
            'referer': 'https://app.contaazul.com/',
            'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
            'x-authorization': '922b3bb3-b3e4-4c2e-8c80-deaa12467c10',
            'Cookie': 'cookiesession1=678A3E1D15F61BBFF890AF8274FDEDC5; login-redirect=/#/dashboard; _ga=GA1.1.1183683136.1744051842; _uetsid=4fa9a86013be11f087d375a1af427428|1sty7l8|2|fuv|0|1923; _uetvid=45c82dd0067711f0b8200fa17f40b1fe|sdx75r|1744051842635|1|1|bat.bing.com/p/insights/c/e; voxusmediamanager_id=17407702971110.21421433609881757gf511u2gwii; _gcl_au=1.1.1621269716.1744051842.272532220.1744051844.1744051844; voxus_last_impression_timestamp_2575=1742585350; vx_session_id=1183683136.1744051842; vx_session_start=1744051841; auth-token-accountancy=005bd053-fdf5-4630-8dee-4f0664334a7d; measurement_id=G-0ZF31QJEMG; ca-pro-auth-token-306702=922b3bb3-b3e4-4c2e-8c80-deaa12467c10; auth-token-pd=922b3bb3-b3e4-4c2e-8c80-deaa12467c10; vx_identifier=5; vx_session_pages_qt=4; vx_user_sessions={%221183683136.1744051842%22:{%22sessionTime%22:23%2C%22timestamp%22:1744051864}}; redirect_token=922b3bb3-b3e4-4c2e-8c80-deaa12467c10; auth-token=922b3bb3-b3e4-4c2e-8c80-deaa12467c10; _hjSession_213761=eyJpZCI6IjA1ZDNjYTRmLWIwN2UtNGMwZC05YTRjLTdkNmQwYjVkOGRlNyIsImMiOjE3NDQwNTE4Njc3NDksInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjoxLCJzcCI6MH0=; _hjSessionUser_213761=eyJpZCI6IjU0MDg4N2MxLWMzMDgtNTliYS05NmUxLTFiZjJiMjc0YjYzNiIsImNyZWF0ZWQiOjE3NDQwNTE4Njc3NDgsImV4aXN0aW5nIjp0cnVlfQ==; _ga_0ZF31QJEMG=GS1.1.1744051841.1.1.1744054308.57.0.0; ctid=MjY1NjU4Ng==; JSESSIONID=CA6D8CCC552C4D4F6BAE70775E892512.contaazul-app-6cd99868fb-ghcrj'
        }


        response = requests.post(f"{url}?page={page}&page_size={page_size}", headers=headers, data=payload)

        if response.status_code == 200:
            data = response.json()

            if 'totalItems' in data and 'items' in data:
                total_items = data['totalItems']
                items = data['items']

                print(f"Página {page} recebida com {len(items)} itens.")

                for item in items:
                    item['centroCusto'] = cost_center_id

                all_items.extend(items)

                total_pages = (total_items // page_size) + (1 if total_items % page_size > 0 else 0)

                if page >= total_pages:
                    print("Centro de custo finalizado.\n")
                    break
                page += 1
            else:
                print("Chaves 'items' ou 'totalItems' ausentes na resposta.")
                break
        else:
            print(f"Erro {response.status_code} na requisição.")
            break

# Transformando os dados em DataFrame
df = pd.DataFrame(all_items)
df = df.rename(columns={"id": "id_lançamento"})
df_expanded = pd.json_normalize(df['financialAccount'])
df_expanded = df_expanded.rename(columns={"id": "financialAccountId2"})
df_final = pd.concat([df, df_expanded], axis=1)
df_final = df_final.rename(columns={
    "financialAccount": "financialAccountId_base",
    "financialAccountId2": "financialAccountId"
})

# Salvando resultado
df_final.to_json(r"data/base_03_rc.json", orient="records", force_ascii=False)