from flask import Blueprint, render_template, request, redirect, url_for, session
from menu import menu_items
from sysdb import SessionLocal, Usuario, Projeto, engine
from sqlalchemy import inspect


bp_routes = Blueprint('routes', __name__)

@bp_routes.route('/')
def index():
    return render_template('index.html', menu_items=menu_items)

@bp_routes.route('/users')
def users():
    return render_template('users.html', menu_items=menu_items)

@bp_routes.route('/projeto')
def call_projeto():
    return render_template('form_projeto.html', menu_items=menu_items)

@bp_routes.route('/datasource')
def call_Datasource():
    return render_template('form_datasource.html', menu_items=menu_items)

@bp_routes.route('/generate-code')
def generatecode():
    inspector = inspect(engine)  # Usamos o inspector para listar tabelas
    tables = inspector.get_table_names()  # Obtém todas as tabelas
    return render_template('generate_code.html', menu_items=menu_items, tables=tables)

@bp_routes.route('/about')
def about():
    return render_template('about.html', menu_items=menu_items)


@bp_routes.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    session_db = SessionLocal()

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        project_id = request.form.get('project', '0')  # Pega o projeto selecionado, se houver
        
        user = session_db.query(Usuario).filter_by(username=username).first()

        if user and user.get_password() == password:
            session['username'] = user.username
            session['nome'] = user.nome
            session['perfil'] = user.perfil

            # Verificar se o projeto existe
            project = session_db.query(Projeto).filter_by(idProjeto=project_id).first()
            if project:
                session['idProjeto'] = project.idProjeto
                session['nomeProjeto'] = project.descProjeto
            else:
                session['idProjeto'] = 0
                session['nomeProjeto'] = "SYS"

            return redirect(url_for('routes.index'))
        else:
            error = True

    # Buscar projetos disponíveis
    projects = session_db.query(Projeto).filter_by(status='A').all()
    return render_template('login.html', projects=projects, error=error)

@bp_routes.route('/logout')
def logout():
    """Remove os dados da sessão e redireciona para a tela de login."""
    session.clear()
    return redirect(url_for('routes.login'))

@bp_routes.route('/suppdataconfig')
def call_Suppdataconfig():
    return render_template('form_suppdataconfig.html', menu_items=menu_items)

@bp_routes.route('/suppdatadet/<string:codSupData>')
def call_Suppdatadet(codSupData=None):
    return render_template('form_suppdatadet.html', menu_items=menu_items, codSupData=codSupData)

@bp_routes.route('/processo')
def call_Processo():
    return render_template('form_processo.html', menu_items=menu_items)
