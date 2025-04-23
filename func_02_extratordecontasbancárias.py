
import pandas as pd
import os

# Simulação de dados
base_cb = pd.DataFrame({"banco": ["Itau", "Bradesco"]})

# Garante que a pasta 'data/' exista
os.makedirs("data", exist_ok=True)

# Verifica shape antes de salvar
print("Shape do DataFrame base_cb:", base_cb.shape)

# Salva o arquivo
base_cb.to_json("data/base_02_cb.json", orient="records")

# Verifica se o arquivo foi criado
if os.path.exists("data/base_02_cb.json"):
    print("Arquivo base_02_cb.json salvo com sucesso.")
else:
    print("Falha ao salvar base_02_cb.json.")
