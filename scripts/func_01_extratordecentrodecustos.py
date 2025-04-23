import requests
import pandas as pd
import json

url = "https://services.contaazul.com/finance-pro/v1/cost-centers?search=&page_size=10&page=1&quick_filter=ACTIVE"

payload = {}
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

response = requests.get(url, headers=headers)

# Verifica se a requisição foi bem-sucedida
if response.status_code == 200:
    data = response.json()
    
    # Cria um DataFrame a partir dos dados recebidos
    base_cc = pd.DataFrame(data["items"])
    
    # Criar uma nova linha com valores "NONE"
    new_row = pd.DataFrame([{
        "id": "NONE",  # Supondo que o id deve ser None
        "version": "NONE",
        "code": "NONE",
        "name": "NONE",
        "parent": "NONE",
        "active": "NONE"
    }])
    
    # Usar pd.concat para adicionar a nova linha ao DataFrame
    base_cc = pd.concat([base_cc, new_row], ignore_index=True)
    base_cc.rename(columns={'id': 'centroCusto'}, inplace=True)
    
    # Salva o DataFrame atualizado em arquivos JSON e Excel
    base_cc.to_json(r"/data/base_01_cc.json")
 
    
    print("Consulta de base CC finalizada  com sucesso.")
else:
    print(f"Erro na requisição: {response.status_code}")
    print("Resposta:", response.text)

with open("/data/debug_log.txt", "a") as f:
    f.write("Script func_01 executado\\n")
