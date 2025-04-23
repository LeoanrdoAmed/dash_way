import pandas as pd
import sqlite3

conn = sqlite3.connect("/data/dashway.db")
df_cb = pd.read_sql("SELECT * FROM contas_bancarias", conn)
df_cc = pd.read_sql("SELECT * FROM centros_de_custo", conn)
df_rc = pd.read_sql("SELECT * FROM contas_receber", conn)

tb_rc = pd.merge(df_rc, df_cb, on='financialAccountId', how='left')
tb_rc_final = pd.merge(tb_rc, df_cc, on='centroCusto', how='left')

tb_rc_final.rename(columns={
    "date": "data", "description": "descrição", "type": "tipo", "value": "valor",
    "categoryName": "categoria", "financialAccountId": "codigo_bancario", 
    "centroCusto": "centro_de_custo_id", "nmBanco": "conta_bancaria", 
    "name": "centro_de_custo", "active": "status_da_conta"
}, inplace=True)

tb_rc_final = tb_rc_final[tb_rc_final["descrição"].str.contains(r"^Venda(?:\s.*)?$", regex=True)]

tb_rc_final.to_sql("base_unificada", conn, if_exists="replace", index=False)
conn.close()
print("Base unificada salva com sucesso.")