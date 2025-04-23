import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output, dash_table, ctx
import pandas as pd
from datetime import datetime, timedelta
from flask import Flask, request, redirect, url_for, flash, render_template_string
import flask_login
import os
import threading
import subprocess

DATA_PATH = "/data/base_final_04_rc.json"

def carregar_dados():
    if os.path.exists(DATA_PATH):
        tb = pd.read_json(DATA_PATH)
        tb['data'] = pd.to_datetime(tb['dueDate'])
        tb['data'] = tb['data'].dt.date
        tb["faturamento"] = tb["unpaid"] + tb["paid"]
        tb['ano'] = pd.to_datetime(tb['data']).dt.year
        return tb
    return pd.DataFrame()

# ==============================
# 1. CONFIGURAÇÃO DO FLASK E LOGIN
# ==============================
server = Flask(__name__)
server.secret_key = 'SEGREDO_DASH_RENDER'
login_manager = flask_login.LoginManager()
login_manager.init_app(server)
login_manager.login_view = '/login'

class User(flask_login.UserMixin):
    def __init__(self, id, username, password, role='user'):
        self.id = id
        self.username = username
        self.password = password
        self.role = role

users = {}
master_user = User('1', 'master', 'master', role='master')
users[master_user.id] = master_user

@login_manager.user_loader
def load_user(user_id):
    return users.get(user_id)

# ==============================
# 2. ROTAS DE LOGIN, LOGOUT, REGISTRO
# ==============================
@server.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        for user in users.values():
            if user.username == username and user.password == password:
                flask_login.login_user(user)
                return redirect('/')
        flash('Credenciais inválidas', 'danger')
        return redirect(url_for('login'))
    return render_template_string('''
    <html><head><title>Login</title></head><body>
    <form method="post">
        <input name="username" placeholder="Usuário"><br>
        <input name="password" type="password" placeholder="Senha"><br>
        <button type="submit">Entrar</button>
    </form></body></html>
    ''')

@server.route('/logout')
@flask_login.login_required
def logout():
    flask_login.logout_user()
    return redirect('/login')

@server.route('/register', methods=['GET', 'POST'])
@flask_login.login_required
def register():
    if flask_login.current_user.role != 'master':
        flash("Apenas o master pode registrar usuários.")
        return redirect('/')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        for user in users.values():
            if user.username == username:
                flash("Usuário já existe.")
                return redirect(url_for('register'))
        new_id = str(len(users) + 1)
        users[new_id] = User(new_id, username, password)
        flash("Usuário criado com sucesso.")
        return redirect('/')
    return "<form method='post'><input name='username'><input name='password'><button type='submit'>Cadastrar</button></form>"

# ==============================
# 3. DASH APP
# ==============================
app = dash.Dash(__name__, server=server, external_stylesheets=[dbc.themes.FLATLY], suppress_callback_exceptions=True)

def serve_layout():
    if not flask_login.current_user.is_authenticated:
        return dcc.Location(pathname="/login", id="redir-login")
    tb_rc = carregar_dados()
    anos_disponiveis = sorted(tb_rc['ano'].unique()) if not tb_rc.empty else []
    df_tipo = pd.DataFrame({"tipo": ["Entrada", "Saída"]})
    return html.Div([
        dbc.NavbarSimple(brand="Dashboard", color="primary", dark=True, children=[
            dbc.NavItem(dbc.NavLink("Logout", href="/logout"))
        ]),
        html.Div([
            dbc.Button("Atualizar Dados", id="btn-atualizar", color="primary", className="mb-3"),
            html.Div(id="mensagem-atualizacao")
        ], style={"margin": "20px"}),
        html.Div(id="dashboard-content")
    ])

app.layout = serve_layout

# ==============================
# 4. CALLBACK DE ATUALIZAÇÃO MANUAL
# ==============================
atualizacao_em_andamento = False
@app.callback(
    Output("mensagem-atualizacao", "children"),
    Input("btn-atualizar", "n_clicks"),
    prevent_initial_call=True
)
def atualizar_base(n_clicks):
    global atualizacao_em_andamento
    if atualizacao_em_andamento:
        return dbc.Alert("Atualização em andamento...", color="warning")
    atualizacao_em_andamento = True

    def executar():
        global atualizacao_em_andamento
        try:
            subprocess.run(["python", "func_01_extratordecentrodecustos.py"], check=True)
            subprocess.run(["python", "func_02_extratordecontasbancarias.py"], check=True)
            subprocess.run(["python", "func_03_extratordecontasareceber.py"], check=True)
            subprocess.run(["python", "func_04_unificadordetabelas.py"], check=True)
        except Exception as e:
            print("Erro:", e)
        finally:
            atualizacao_em_andamento = False

    threading.Thread(target=executar).start()
    return dbc.Alert("Atualização iniciada. Aguarde alguns segundos...", color="info")

if __name__ == "__main__":
    app.run(debug=True)