
import pandas as pd
import os

# Simulação de dados
base_cr = pd.DataFrame({"receber": [100, 200, 300]})

# Garante que a pasta 'data/' exista
os.makedirs("data", exist_ok=True)

# Verifica shape antes de salvar
print("Shape do DataFrame base_cr:", base_cr.shape)

# Salva o arquivo
base_cr.to_json("data/base_03_cr.json", orient="records")

# Verifica se o arquivo foi criado
if os.path.exists("data/base_03_cr.json"):
    print("Arquivo base_03_cr.json salvo com sucesso.")
else:
    print("Falha ao salvar base_03_cr.json.")
