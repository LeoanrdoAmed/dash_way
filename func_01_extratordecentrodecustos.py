import os
import pandas as pd

DATA_DIR = "/data" if os.path.exists("/data") else "data"
os.makedirs(DATA_DIR, exist_ok=True)
base_cc = os.path.join(DATA_DIR, "base_01_cc.json")

# Simulação de extração
base_cc_df = pd.DataFrame({
    "centro_de_custo": ["Administrativo", "Operacional"],
    "valor": [1000, 2500],
    "tipo": ["Entrada", "Saída"],
    "data": ["2025-04-01", "2025-04-02"],
    "dueDate": ["2025-04-01", "2025-04-02"],
    "unpaid": [500, 1000],
    "paid": [500, 1500],
    "status": ["PAID", "OVERDUE"]
})

base_cc_df.to_json(base_cc, orient="records", indent=2)