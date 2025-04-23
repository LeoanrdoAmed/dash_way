import pandas as pd


base_cc = r"/data/base_01_cc.json"
base_cb = r"/data/base_02_cb.json"
base_rc = r"/data/base_03_rc.json"


df2 = pd.read_json(base_cb)
df3 = pd.read_json(base_cc)
df4 = pd.read_json(base_rc)


# Tabela contas a receber
tb_rc = pd.merge(df4, df2, on='financialAccountId', how='left')
tb_rc_final = pd.merge(tb_rc, df3, on='centroCusto', how='left')

#tb_rc_final = tb_rc_final.drop(columns=["digitalReceiptId","paymentRequest", "reconciliationId", "financialAccount", "installmentId", "renegotiation", "transferId", "chargeRequest", "acquittanceScheduled", "authorizedBankSlipId", "installmentsCount","version_x", "origin", "recurrenceIndex", "categoryCount", "version_y", "code", "parent", "emailSent", "emailVisualization",  "hasAttachment", "scheduled", "chargeViewStatus", "negotiator", "financialEvent", "installmentIndex", "installmentValueComposition", "installmentPaid"])
tb_rc_final.rename(columns={"date": "data", "description" : "descrição", "type" : "tipo","value" : "valor", "categoryName" : "categoria", "financialAccountId": "codigo_bancario", "centroCusto" : "centro_de_custo_id", "nmBanco" : "conta_bancaria", "name" : "centro_de_custo", "active" : 'status_da_conta'}, inplace=True)

#tb_rc_final_01 = tb_rc_final[tb_rc_final["descrição"].str.contains(r"^Venda(\s.*)?$", regex=True)]
#tb_rc_final_01 = tb_rc_final[tb_rc_final["descrição"].str.contains(r"^Venda(?:\s.*)?$", regex=True)]
#tb_rc_final_01 = tb_rc_final[tb_rc_final["descrição"].str.contains(r"^Venda(?:\\s.*)?$", regex=True)]
tb_rc_final_01 = tb_rc_final[tb_rc_final["descrição"].str.contains(r"\bVenda\b", case=False, na=False)]


tb_rc_final_01.to_json("/data/base_final_04_rc.json")
#tb_rc_final_01.to_excel("base_final_04_rc.xlsx")
#tb_rc_final.to_excel("base_final_05_rc.xlsx")
print("Consulta de base UNI finalizada  com sucesso.")
