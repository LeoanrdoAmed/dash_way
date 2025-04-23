
import subprocess

scripts = [
    "func_01_extratordecentrodecustos.py",
    "func_02_extratordecontasbancárias.py",
    "func_03_extratordecontasareceber.py",
    "func_04_unificadordetabelas.py"
]

print("🔄 Iniciando execução dos scripts de preparação de dados...\n")

for script in scripts:
    try:
        print(f"▶️ Executando {script}...")
        subprocess.run(["python", script], check=True)
        print(f"✅ {script} executado com sucesso.\n")
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao executar {script}: {e}\n")
        break

print("🏁 Finalizado.")
