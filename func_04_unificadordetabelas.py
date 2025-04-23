import os
import pandas as pd

DATA_DIR = "/data" if os.path.exists("/data") else "data"
os.makedirs(DATA_DIR, exist_ok=True)

base_cc = os.path.join(DATA_DIR, "base_01_cc.json")
base_cb = os.path.join(DATA_DIR, "base_02_cb.json")
base_mv = os.path.join(DATA_DIR, "base_03_mv.json")
base_cr = os.path.join(DATA_DIR, "base_05_cr.json")
base_final = os.path.join(DATA_DIR, "base_final_04_rc.json")

df1 = pd.read_json(base_cc)
df2 = pd.read_json(base_cb)
df3 = pd.DataFrame([])  # Não implementado ainda
df4 = pd.read_json(base_cr)

tb_rc_final = pd.concat([df1, df2, df4], ignore_index=True)
tb_rc_final.to_json(base_final, orient="records", indent=2)