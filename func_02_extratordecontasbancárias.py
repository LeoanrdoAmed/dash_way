import os
import pandas as pd

DATA_DIR = "/data" if os.path.exists("/data") else "data"
os.makedirs(DATA_DIR, exist_ok=True)
base_cb = os.path.join(DATA_DIR, "base_02_cb.json")

# Simulação de extração
df = pd.DataFrame({
    "centro_de_custo": ["Financeiro", "TI"],
    "valor": [3000, 4000],
    "tipo": ["Entrada", "Saída"],
    "data": ["2025-04-03", "2025-04-04"],
    "dueDate": ["2025-04-03", "2025-04-04"],
    "unpaid": [3000, 2000],
    "paid": [0, 2000],
    "status": ["OVERDUE", "PAID"]
})

df.to_json(base_cb, orient="records", indent=2)