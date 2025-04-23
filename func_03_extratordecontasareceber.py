import os
import pandas as pd

DATA_DIR = "/data" if os.path.exists("/data") else "data"
os.makedirs(DATA_DIR, exist_ok=True)
base_cr = os.path.join(DATA_DIR, "base_05_cr.json")

# Simulação de extração
df = pd.DataFrame({
    "centro_de_custo": ["Comercial", "RH"],
    "valor": [2000, 1500],
    "tipo": ["Entrada", "Saída"],
    "data": ["2025-04-05", "2025-04-06"],
    "dueDate": ["2025-04-05", "2025-04-06"],
    "unpaid": [1000, 500],
    "paid": [1000, 1000],
    "status": ["PAID", "OVERDUE"]
})

df.to_json(base_cr, orient="records", indent=2)