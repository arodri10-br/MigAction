from flask import Flask, render_template
from sysdb import init_db
import configparser

from routes import bp_routes 
from api_sysdb import bp as api_sysdb_bp
from api_database import bp_database

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
app.register_blueprint(api_sysdb_bp, url_prefix='/sys')
app.register_blueprint(bp_database, url_prefix='/sys')
app.register_blueprint(bp_routes)  # Registra o blueprint do routes


if __name__ == '__main__':
    app.run(debug=True)
