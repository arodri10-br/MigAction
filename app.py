from flask import Flask
from sysdb import init_db
import configparser

from routes import bp_routes 
from api_sysdb import bp_usuario
from api_database import bp_database
from api_projeto import bp_projeto
from api_suppdataconfig import bp_suppdataconfig
from api_suppdatadet import bp_suppdatadet
from api_datasource import bp_datasource
from generate_code import generate_code_bp

app = Flask(__name__, 
    static_folder='./static',
    template_folder='./templates')

# Ler configurações do arquivo config.ini
config = configparser.ConfigParser()
config.read("config.ini")

# Definir a chave secreta do Flask
app.secret_key = config["flask"].get("SECRET_KEY", "chave_padrao_segura")

# Inicializa o banco de dados
init_db()

# Registra o blueprint
#app.register_blueprint(api_sysdb_bp, url_prefix='/sys')
app.register_blueprint(bp_routes)  
app.register_blueprint(bp_database, url_prefix='/sys')
app.register_blueprint(bp_usuario)
app.register_blueprint(generate_code_bp)
app.register_blueprint(bp_projeto)
app.register_blueprint(bp_suppdataconfig)
app.register_blueprint(bp_suppdatadet)
app.register_blueprint(bp_datasource)

if __name__ == '__main__':
    app.run(debug=True)
