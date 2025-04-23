
import pandas as pd
import os

# Simulação de dados
base_cc = pd.DataFrame({"coluna_exemplo": [1, 2, 3]})

# Garante que a pasta 'data/' exista
os.makedirs("data", exist_ok=True)

# Verifica shape antes de salvar
print("Shape do DataFrame base_cc:", base_cc.shape)

# Salva o arquivo
base_cc.to_json("data/base_01_cc.json", orient="records")

# Verifica se o arquivo foi criado
if os.path.exists("data/base_01_cc.json"):
    print("Arquivo base_01_cc.json salvo com sucesso.")
else:
    print("Falha ao salvar base_01_cc.json.")
