
import os
import pandas as pd

# Garantir que o diretório 'data/' exista
os.makedirs("data", exist_ok=True)

base_cc = "data/base_01_cc.json"
base_cb = "data/base_02_cb.json"
base_mv = "data/base_03_mv.json"

# Verificações de existência dos arquivos antes da leitura
for file in [base_cc, base_cb, base_mv]:
    if not os.path.exists(file):
        print(f"Arquivo não encontrado: {file}")
        exit(1)

# Leitura das bases
df1 = pd.read_json(base_cc)
df2 = pd.read_json(base_cb)
df3 = pd.read_json(base_mv)

# Concatenar as bases
tb_rc_final = pd.concat([df1, df2, df3], ignore_index=True)

# Exportar base final
tb_rc_final.to_json("data/base_final_04_rc.json", orient="records", force_ascii=False)
print("Base final salva com sucesso.")
