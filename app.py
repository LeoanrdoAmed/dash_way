import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output, dash_table  # Import atualizado conforme recomendado
import pandas as pd
from datetime import datetime, timedelta

from flask import Flask, request, redirect, url_for, flash, render_template_string
import flask_login

# ------------------------------------------------------------------
# IMPORTAÇÃO DOS DADOS (substitua pelos seus módulos)
base_rc = r"/data/base_final_04_rc.json"
tb_rc_final = pd.read_json(base_rc)
df = pd.DataFrame({
    "tipo": ["Entrada", "Saída"]
})

#from func_04_unificadordetabelas import tb_rc_final
# ------------------------------------------------------------------

# ==============================
# 1. CONFIGURAÇÃO DO SERVIDOR FLASK & FLASK-LOGIN
# ==============================
server = Flask(__name__)
server.secret_key = 'SUA_CHAVE_SECRETA_AQUI'  # Substitua por uma chave segura

login_manager = flask_login.LoginManager()
login_manager.init_app(server)
login_manager.login_view = '/login'  # Rota para redirecionamento caso não autenticado

# Classe User com atributo role ("master" ou "user")
class User(flask_login.UserMixin):
    def __init__(self, id, username, password, role='user'):
        self.id = id
        self.username = username
        self.password = password
        self.role = role

# "Banco de dados" em memória (apenas para demonstração)
users = {}

@login_manager.user_loader
def load_user(user_id):
    return users.get(user_id)

# Criação de um usuário master (login: master; senha: master)
master_user = User('1', 'master', 'master', role='master')
users[master_user.id] = master_user

# ==============================
# 2. ROTAS FLASK: LOGIN, REGISTRO, LOGOUT
# ==============================
@server.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Validação simples: em produção, utilize hash e validação robusta
        for user in users.values():
            if user.username == username and user.password == password:
                flask_login.login_user(user)
                print("Usuário autenticado:", user.username)  # Debug
                return redirect('/')
        flash('Credenciais inválidas', 'danger')
        return redirect(url_for('login'))
    
    # Tela de login com design Flatly e logo acima do "Bem-vindo"
    return '''
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
      <meta charset="UTF-8">
      <title>Login - Dashboard</title>
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootswatch/4.5.2/flatly/bootstrap.min.css">
      <style>
          body { background: #f7f7f7; font-family: "Helvetica Neue", Helvetica, Arial, sans-serif; }
          .login-container { margin-top: 80px; }
          .card { padding: 20px; border: none; border-radius: 8px; box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1); }
          .card-title { font-weight: bold; }
          .btn-primary { width: 100%; padding: 10px; border-radius: 5px; }
          .login-footer { margin-top: 15px; }
          .logo { display: block; margin: 0 auto 20px; }
      </style>
    </head>
    <body>
      <div class="container login-container">
          <div class="row justify-content-center">
              <div class="col-md-5 col-lg-4">
                  <div class="card">
                      <div class="card-body">
                          <!-- Logo da empresa -->
                          <div class="text-center">
                              <img src="/assets/WG_orig_fundo branco.png" alt="Logo da Empresa" class="logo" style="height: 80px;">
                          </div>
                          <h3 class="card-title text-center mb-4">Bem-vindo</h3>
                          <form method="post">
                              <div class="form-group">
                                  <input type="text" name="username" class="form-control" placeholder="Usuário" required>
                              </div>
                              <div class="form-group">
                                  <input type="password" name="password" class="form-control" placeholder="Senha" required>
                              </div>
                              <button type="submit" class="btn btn-primary">Entrar</button>
                          </form>
                          <!-- O link para registro foi removido, pois somente usuário master pode cadastrar novos usuários -->
                      </div>
                  </div>
              </div>
          </div>
      </div>
      <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
      <script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.1/dist/umd/popper.min.js"></script>
      <script src="https://stackpath.bootstrapcdn.com/bootswatch/4.5.2/flatly/bootstrap.min.js"></script>
    </body>
    </html>
    '''

# Rota de cadastro: somente acessível a usuário master
@server.route('/register', methods=['GET', 'POST'])
@flask_login.login_required
def register():
    if flask_login.current_user.role != 'master':
         flash('Acesso negado: Apenas usuário master pode cadastrar novos usuários.', 'danger')
         return redirect('/')
    
    if request.method == 'POST':
         username = request.form['username']
         password = request.form['password']
         # Verifica se o usuário já existe
         for user in users.values():
             if user.username == username:
                 flash('Usuário já existe', 'warning')
                 return redirect(url_for('register'))
         new_id = str(len(users) + 1)
         new_user = User(new_id, username, password, role='user')
         users[new_id] = new_user
         flash('Usuário cadastrado com sucesso.', 'success')
         return redirect('/user_control')
         
    return '''
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
      <meta charset="UTF-8">
      <title>Cadastro de Usuários - Dashboard</title>
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootswatch/4.5.2/flatly/bootstrap.min.css">
      <style>
          body { background: #f7f7f7; font-family: "Helvetica Neue", Helvetica, Arial, sans-serif; }
          .register-container { margin-top: 80px; }
          .card { padding: 20px; border: none; border-radius: 8px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
          .card-title { font-weight: bold; }
          .btn-primary { width: 100%; padding: 10px; border-radius: 5px; }
          .register-footer { margin-top: 15px; }
      </style>
    </head>
    <body>
      <div class="container register-container">
          <div class="row justify-content-center">
              <div class="col-md-5 col-lg-4">
                  <div class="card">
                      <div class="card-body">
                          <h3 class="card-title text-center mb-4">Cadastrar Novo Usuário</h3>
                          <form method="post">
                              <div class="form-group">
                                  <input type="text" name="username" class="form-control" placeholder="Nome de Usuário" required>
                              </div>
                              <div class="form-group">
                                  <input type="password" name="password" class="form-control" placeholder="Senha" required>
                              </div>
                              <button type="submit" class="btn btn-primary">Cadastrar</button>
                          </form>
                          <div class="register-footer text-center">
                              <small><a href="/user_control">Voltar ao Controle de Usuários</a></small>
                          </div>
                      </div>
                  </div>
              </div>
          </div>
      </div>
      <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
      <script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.1/dist/umd/popper.min.js"></script>
      <script src="https://stackpath.bootstrapcdn.com/bootswatch/4.5.2/flatly/bootstrap.min.js"></script>
    </body>
    </html>
    '''

@server.route('/logout')
@flask_login.login_required
def logout():
    flask_login.logout_user()
    print("Usuário deslogado.")  # Debug
    return redirect('/login')

# ==============================
# 3. CONTROLE DE USUÁRIOS (APENAS PARA USUÁRIO MASTER)
# ==============================
@server.route('/user_control', methods=['GET'])
@flask_login.login_required
def user_control():
    if flask_login.current_user.role != 'master':
         flash("Acesso negado: apenas usuários master podem acessar essa página.", "danger")
         return redirect('/')
    
    html_table = '<table class="table table-striped"><thead><tr><th>ID</th><th>Usuário</th><th>Papel</th><th>Ações</th></tr></thead><tbody>'
    for user in users.values():
        actions = ''
        if user.id != flask_login.current_user.id:
            actions += f'<a href="/delete_user/{user.id}" class="btn btn-danger btn-sm" onclick="return confirm(\'Tem certeza?\');">Excluir</a> '
            if user.role != 'master':
                actions += f'<a href="/set_role/{user.id}/master" class="btn btn-success btn-sm">Tornar Master</a>'
            else:
                actions += f'<a href="/set_role/{user.id}/user" class="btn btn-warning btn-sm">Tornar Padrão</a>'
        html_table += f'<tr><td>{user.id}</td><td>{user.username}</td><td>{user.role}</td><td>{actions}</td></tr>'
    html_table += '</tbody></table>'
    
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
      <meta charset="UTF-8">
      <title>Controle de Usuários</title>
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootswatch/4.5.2/flatly/bootstrap.min.css">
    </head>
    <body>
      <div class="container">
          <h2 class="mt-4">Controle de Usuários</h2>
          <div>''' + html_table + '''</div>
          <a href="/register" class="btn btn-primary">Cadastrar Novo Usuário</a>
          <a href="/" class="btn btn-secondary">Voltar ao Dashboard</a>
      </div>
    </body>
    </html>
    ''')

@server.route('/delete_user/<user_id>', methods=['GET'])
@flask_login.login_required
def delete_user(user_id):
    if flask_login.current_user.role != 'master':
         flash("Acesso negado: apenas usuários master podem excluir.", "danger")
         return redirect('/')
    if user_id == flask_login.current_user.id:
         flash("Você não pode se excluir.", "warning")
         return redirect('/user_control')
    if user_id in users:
         del users[user_id]
         flash("Usuário excluído com sucesso.", "success")
    else:
         flash("Usuário não encontrado.", "warning")
    return redirect('/user_control')

@server.route('/set_role/<user_id>/<role>', methods=['GET'])
@flask_login.login_required
def set_role(user_id, role):
    if flask_login.current_user.role != 'master':
         flash("Acesso negado: apenas usuários master podem alterar papéis.", "danger")
         return redirect('/')
    if user_id in users:
         user = users[user_id]
         user.role = role
         flash("Papel do usuário atualizado.", "success")
    else:
         flash("Usuário não encontrado.", "warning")
    return redirect('/user_control')

# ==============================
# 4. PREPARAÇÃO DOS DADOS DO DASHBOARD
# ==============================
ano_atual = str(datetime.now().year)
tb_rc_final['data'] = pd.to_datetime(tb_rc_final['dueDate'])
tb_rc_final['data'] = tb_rc_final['data'].dt.date
tb_rc_final["faturamento"] = tb_rc_final["unpaid"] + tb_rc_final["paid"]
tb_rc_final['ano'] = pd.to_datetime(tb_rc_final['data']).dt.year
anos_disponiveis = sorted(tb_rc_final['ano'].unique())

def get_date_range(option):
    today = datetime.today().date()
    ranges = {
        "Hoje": (today, today),
        "Últimos 7 dias": (today - timedelta(days=7), today),
        "Último mês": (today - timedelta(days=30), today),
        "Últimos 3 meses": (today - timedelta(days=90), today),
        "Últimos 6 meses": (today - timedelta(days=180), today),
        "Último ano": (today - timedelta(days=365), today),
        "Todo o período": (None, None)
    }
    # Se o valor for um ano (string numérica), retorna o intervalo daquele ano
    return ranges.get(option, (datetime(int(option), 1, 1).date(), datetime(int(option), 12, 31).date()) if option.isdigit() else (None, None))

# ==============================
# 5. CONFIGURAÇÃO DO DASH (Integrado ao Flask)
# ==============================
app = dash.Dash(
    __name__,
    server=server,
    external_stylesheets=[dbc.themes.FLATLY],
    suppress_callback_exceptions=True
)

# Layout dinâmico: reavaliado sempre que a página for carregada
def serve_dashboard():
    print("Layout acessado. Usuário autenticado?", flask_login.current_user.is_authenticated)  # Debug
    if not flask_login.current_user.is_authenticated:
         return html.Div([ dcc.Location(pathname='/login', id='redirect-location', refresh=True) ])
    
    return html.Div([
        dbc.NavbarSimple(
            children=[
                dbc.NavItem(dbc.NavLink("Controle Usuários", href="/user_control", external_link=True)),
                dbc.NavItem(dbc.NavLink("Logout", href="/logout", external_link=True))
            ],
            brand="Dashboard",
            color="primary",
            dark=True,
            fluid=True
        ),
        html.Div([
            html.Div([
                html.Img(src="/assets/WG_orig_fundo branco.png",
                         style={"height": "60px", "margin": "10px"}),
            ], style={"textAlign": "left", "padding": "10px 30px"}),
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.Label("Centro de Custo", className="form-label"),
                            dcc.Dropdown(
                                id="dropdown-centro-custo",
                                options=[{"label": c, "value": c} for c in tb_rc_final["centro_de_custo"].unique()],
                                value=[],
                                multi=True,
                                placeholder="Todos",
                                className="mb-3"
                            )
                        ], md=4),
                        dbc.Col([
                            html.Label("Período da Movimentação", className="form-label"),
                            dcc.Dropdown(
                                id="dropdown-data-filtro",
                                options=[{"label": i, "value": i} for i in [
                                    "Hoje", "Todo o período", "Últimos 7 dias", "Último mês",
                                    "Últimos 3 meses", "Últimos 6 meses", "Último ano"
                                ]] + [{"label": str(ano), "value": str(ano)} for ano in anos_disponiveis],
                                value=ano_atual,
                                className="mb-3"
                            )
                        ], md=4),
                        dbc.Col([
                            html.Label("Tipo de Movimentação", className="form-label"),
                            dcc.Dropdown(
                                id="dropdown-tipo-movimentacao",
                                options=[{"label": t, "value": t} for t in df["tipo"].unique()],
                                value=[],
                                multi=True,
                                placeholder="Todos",
                                className="mb-3"
                            )
                        ], md=4)
                    ])
                ])
            ], style={"margin": "0px 30px 30px 30px", "borderRadius": "16px",
                      "backgroundColor": "#fdfbf9", "boxShadow": "0 4px 12px rgba(0,0,0,0.05)"}),
            html.Div([
        dbc.Button("Atualizar Dados Manualmente", id="btn-atualizar", color="primary", className="mb-3"),
        html.Div(id="mensagem-atualizacao", style={"marginBottom": "20px"})
    ], style={"margin": "20px 30px 0 30px"}),

    dbc.Container([
                dbc.Row([
                    dbc.Col(dcc.Graph(id="grafico-movimentacoes"), width=6),
                    dbc.Col(dcc.Graph(id="grafico-quantidade-lancamentos"), width=6)
                ], className="mb-3"),
                dbc.Row([
                    dbc.Col(dcc.Graph(id="grafico-ticket-medio"), width=6),
                    dbc.Col(dcc.Graph(id="grafico-total-centro-custo"), width=6)
                ], className="mb-3"),
                dbc.Row([
                    dbc.Col([
                        html.H5("Resumo de Inadimplentes", className="mb-3"),
                        dash_table.DataTable(
                            id="tabela-inadimplentes",
                            style_table={"overflowX": "auto"},
                            style_cell={"textAlign": "center", "padding": "8px"},
                            style_header={"fontWeight": "bold", "backgroundColor": "#f8f9fa"},
                            style_data={"backgroundColor": "#fdfbf9", "border": "1px solid #eee"},
                            style_as_list_view=True
                        )
                    ])
                ])
            ], fluid=True)
        ], style={"fontFamily": "Arial, sans-serif", "backgroundColor": "#fdfbf9"})
    ])

app.layout = serve_dashboard

# ==============================
# 6. CALLBACK DO DASHBOARD
# ==============================
@app.callback(
    [Output("grafico-movimentacoes", "figure"),
     Output("grafico-total-centro-custo", "figure"),
     Output("grafico-ticket-medio", "figure"),
     Output("grafico-quantidade-lancamentos", "figure"),
     Output("tabela-inadimplentes", "data"),
     Output("tabela-inadimplentes", "columns")],
    [Input("dropdown-centro-custo", "value"),
     Input("dropdown-data-filtro", "value"),
     Input("dropdown-tipo-movimentacao", "value")]
)
def atualizar_graficos(centros_custo_selecionados, data_filtro, tipos_selecionados):
    start_date, end_date = get_date_range(data_filtro)
    tb_rc = tb_rc_final.copy()

    if centros_custo_selecionados:
        tb_rc = tb_rc[tb_rc["centro_de_custo"].isin(centros_custo_selecionados)]
    if start_date and end_date:
        tb_rc['data'] = pd.to_datetime(tb_rc['data'], errors='coerce').dt.date
        tb_rc = tb_rc[(tb_rc["data"] >= start_date) & (tb_rc["data"] <= end_date)]
    if tipos_selecionados:
        tb_rc = tb_rc[tb_rc["tipo"].isin(tipos_selecionados)]
    
    tb_rc['data'] = pd.to_datetime(tb_rc['data'])
    
    # Gráfico de faturamento mensal
    df_agrupado_mes = tb_rc.groupby(pd.Grouper(key='data', freq='ME'))['faturamento'].sum().reset_index()
    fig_mes = {
        "data": [{
            "x": df_agrupado_mes["data"],
            "y": df_agrupado_mes["faturamento"],
            "type": "bar",
            "marker": {"color": "#4b657f"}
        }],
        "layout": {
            "title": {"text": "Faturamento Mensal", "x": 0.5},
            "xaxis": {"title": "Data"},
            "yaxis": {"title": "Valor Total"}
        }
    }
    
    # Gráfico de faturamento por centro de custo
    df_agrupado_centro = tb_rc.groupby("centro_de_custo")["faturamento"].sum().reset_index().sort_values(by="faturamento", ascending=True)
    fig_centro = {
        "data": [{
            "x": df_agrupado_centro["faturamento"],
            "y": df_agrupado_centro["centro_de_custo"],
            "type": "bar",
            "orientation": "h",
            "marker": {"color": "#4b657f"}
        }],
        "layout": {
            "title": {"text": "Faturamento por Centro de Custo", "x": 0.5},
            "xaxis": {"title": "Valor Total"},
            "yaxis": {"title": "Centro de Custo"}
        }
    }
    
    # Gráfico do ticket médio e quantidade de lançamentos
    df_agrupado_mes['qtd'] = tb_rc.groupby(pd.Grouper(key='data', freq='ME'))['faturamento'].count().reset_index()['faturamento']
    df_agrupado_mes['ticket_medio'] = df_agrupado_mes['faturamento'] / df_agrupado_mes['qtd']
    fig_ticket = {
        "data": [{
            "x": df_agrupado_mes["data"],
            "y": df_agrupado_mes["ticket_medio"],
            "type": "line",
            "line": {"color": "#d6ae60", "shape": "spline"}
        }],
        "layout": {
            "title": {"text": "Ticket Médio Mensal", "x": 0.5},
            "xaxis": {"title": "Mês"},
            "yaxis": {"title": "Ticket Médio"}
        }
    }
    fig_qtd = {
        "data": [{
            "x": df_agrupado_mes["data"],
            "y": df_agrupado_mes['qtd'],
            "type": "line",
            "line": {"color": "#4b657f", "shape": "spline"}
        }],
        "layout": {
            "title": {"text": "Quantidade de Projetos", "x": 0.5},
            "xaxis": {"title": "Mês"},
            "yaxis": {"title": "Quantidade"}
        }
    }
    
    # Resumo de inadimplentes
    tb_rc_inad = tb_rc[tb_rc['status'] == 'OVERDUE']
    df_valores = tb_rc_inad.groupby(pd.Grouper(key='data', freq='ME'))['faturamento'].sum().reset_index()
    df_qtd = tb_rc_inad.groupby(pd.Grouper(key='data', freq='ME')).size().reset_index(name='Qtd. de Inadimplentes')
    df_inad = pd.merge(df_valores, df_qtd, on='data')
    df_inad['data'] = df_inad['data'].dt.strftime('%b/%Y')
    df_inad.rename(columns={'data': 'Mês', 'faturamento': 'Valor Inadimplente (R$)'}, inplace=True)
    df_inad['Valor Inadimplente (R$)'] = df_inad['Valor Inadimplente (R$)'].apply(
        lambda x: f'R$ {x:,.2f}'.replace('.', '#').replace(',', '.').replace('#', ',')
    )
    
    total_valor = df_inad['Valor Inadimplente (R$)'].apply(
        lambda x: float(x.replace('R$ ', '').replace('.', '').replace(',', '.'))
    ).sum()
    total_qtd = df_inad['Qtd. de Inadimplentes'].sum()
    df_inad = pd.concat([df_inad, pd.DataFrame([{
        'Mês': 'Total', 
        'Valor Inadimplente (R$)': f'R$ {total_valor:,.2f}'.replace('.', '#').replace(',', '.').replace('#', ','),
        'Qtd. de Inadimplentes': total_qtd
    }])])
    
    columns = [{"name": col, "id": col} for col in df_inad.columns]
    return fig_mes, fig_centro, fig_ticket, fig_qtd, df_inad.to_dict('records'), columns

# ==============================
# 7. EXECUÇÃO DO APLICATIVO
# ==============================

import agendador_06  # Importa o agendador para execução automática diária

import threading
import subprocess
from dash import ctx
import dash_bootstrap_components as dbc
from dash import dcc, Output, Input, State

# Variável global opcional para evitar concorrência de atualizações
atualizacao_em_andamento = False

@app.callback(
    Output("mensagem-atualizacao", "children"),
    Input("btn-atualizar", "n_clicks"),
    prevent_initial_call=True
)
def iniciar_atualizacao(n_clicks):
    global atualizacao_em_andamento
    if atualizacao_em_andamento:
        return dbc.Alert("Atualização já em andamento...", color="warning", duration=25000)

    atualizacao_em_andamento = True
    
    def rodar_scripts():
        global atualizacao_em_andamento
        try:
            subprocess.run(["python", "scripts/func_01_extratordecentrodecustos.py"], check=True)
            subprocess.run(["python", "scripts/func_02_extratordecontasbancárias.py"], check=True)
            subprocess.run(["python", "scripts/func_03_extratordecontasareceber.py"], check=True)
            subprocess.run(["python", "scripts/func_04_unificadordetabelas.py"], check=True)
            print("Atualização concluída com sucesso.")
        except Exception as e:
            print(f"Erro na atualização: {e}")
        finally:
            atualizacao_em_andamento = False

    threading.Thread(target=rodar_scripts).start()

    return dbc.Alert("Atualização iniciada. Aguarde alguns segundos...", color="info", duration=25000)


if __name__ == "__main__":
    app.run(debug=True)