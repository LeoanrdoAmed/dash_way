# agendador.py
from apscheduler.schedulers.background import BackgroundScheduler
import atexit
import subprocess

def rodar_extracao():
    print("Iniciando execução automática dos scripts...")
    subprocess.run(["python", r"scripts/func_01_extratordecentrodecustos.py"])
    subprocess.run(["python", r"scripts/func_02_extratordecontasbancárias.py"])
    subprocess.run(["python", r"scripts/func_03_extratordecontasareceber.py"])
    subprocess.run(["python", r"scripts/func_04_unificadordetabelas.py"])
    print("Extração automática finalizada.")

# Inicia agendador
scheduler = BackgroundScheduler()
scheduler.add_job(rodar_extracao, 'cron', hour=0, minute=0)  # Executa à 00h00
scheduler.start()
atexit.register(lambda: scheduler.shutdown())
