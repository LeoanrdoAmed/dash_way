import os
import pandas as pd

# Diretório de dados: /data no Render, localmente usa ./data
DATA_DIR = "/data" if os.path.exists("/data") else "data"
os.makedirs(DATA_DIR, exist_ok=True)

# Caminhos corretos
base_cc = os.path.join(DATA_DIR, "base_01_cc.json")
base_cb = os.path.join(DATA_DIR, "base_02_cb.json")
base_rc = os.path.join(DATA_DIR, "base_03_rc.json")

# Leitura das bases
df2 = pd.read_json(base_cb)
df3 = pd.read_json(base_cc)
df4 = pd.read_json(base_rc)

# Tabela contas a receber
tb_rc = pd.merge(df4, df2, on='financialAccountId', how='left')
tb_rc_final = pd.merge(tb_rc, df3, on='centroCusto', how='left')

# Renomeando colunas
tb_rc_final.rename(columns={
    "date": "data",
    "description": "descrição",
    "type": "tipo",
    "value": "valor",
    "categoryName": "categoria",
    "financialAccountId": "codigo_bancario",
    "centroCusto": "centro_de_custo_id",
    "nmBanco": "conta_bancaria",
    "name": "centro_de_custo",
    "active": "status_da_conta"
}, inplace=True)

# Filtrando por descrições que comecem com "Venda"
tb_rc_final_01 = tb_rc_final[tb_rc_final["descrição"].str.contains(r"^Venda(?:\s.*)?$", regex=True)]

# Salvando base final
tb_rc_final_01.to_json(os.path.join(DATA_DIR, "base_final_04_rc.json"), orient="records", force_ascii=False)

print("Consulta de base UNI finalizada com sucesso.")
