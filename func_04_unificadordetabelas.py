
import pandas as pd
import os

# Garante que a pasta 'data/' exista
os.makedirs("data", exist_ok=True)

# Lê os arquivos
base_cc = "data/base_01_cc.json"
base_cb = "data/base_02_cb.json"
base_cr = "data/base_03_cr.json"

print("Verificando arquivos...")
print("base_01_cc existe?", os.path.exists(base_cc))
print("base_02_cb existe?", os.path.exists(base_cb))
print("base_03_cr existe?", os.path.exists(base_cr))

df1 = pd.read_json(base_cc)
df2 = pd.read_json(base_cb)
df3 = pd.read_json(base_cr)

# Simulação da unificação
df_final = pd.concat([df1, df2, df3], axis=0, ignore_index=True)
print("Shape df_final:", df_final.shape)

df_final.to_json("data/base_final_04_rc.json", orient="records")

if os.path.exists("data/base_final_04_rc.json"):
    print("Unificação concluída e salva com sucesso.")
else:
    print("Falha ao salvar a unificação.")
