import pandas as pd

# Corrigir os caminhos de leitura dos arquivos JSON
base_cc = "/data/base_01_cc.json"
base_cb = "/data/base_02_cb.json"
base_mv = "/data/base_03_mv.json"
base_cr = "/data/base_05_cr.json"

# Leitura
df1 = pd.read_json(base_cc)
df2 = pd.read_json(base_cb)
df3 = pd.read_json(base_mv)
df4 = pd.read_json(base_cr)

# Unificação dos dados
tb_rc_final = pd.concat([df1, df2, df3, df4], ignore_index=True)

# Exportação do resultado final
tb_rc_final.to_json("/data/base_final_04_rc.json", orient="records", indent=2)