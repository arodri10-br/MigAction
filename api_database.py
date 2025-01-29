# api_database.py
from flask import Blueprint, jsonify
from sqlalchemy import create_engine, inspect, text
from sysdb import SessionLocal, DatabaseConfig

bp_database = Blueprint('api_database', __name__)

@bp_database.route('/first_config', methods=['GET'])
def get_first_config():
    session = SessionLocal()
    config = session.query(DatabaseConfig).first()
    session.close()
    if config:
        return jsonify(config.to_dict())
    else:
        return jsonify({"message": "Nenhuma configuração encontrada"}), 404

@bp_database.route('/execute_query', methods=['GET'])
def execute_query():
    session = SessionLocal()
    config = session.query(DatabaseConfig).first()
    session.close()
    
    if not config:
        return jsonify({"message": "Nenhuma configuração encontrada"}), 404
    
    # Conectar ao banco de dados usando as informações da configuração
    if config.db_type == 'sqlite':
        db_url = f"sqlite:///{config.database}"
    elif config.db_type == 'oracle':
        db_url = f"oracle://{config.username}:{config.get_password()}@{config.host}:{config.port}/{config.database}"
    elif config.db_type == 'sqlserver':
        db_url = f"mssql+pyodbc://{config.username}:{config.get_password()}@{config.host}:{config.port}/{config.database}?driver=ODBC+Driver+17+for+SQL+Server"
    else:
        return jsonify({"message": "Tipo de banco de dados não suportado"}), 400
    
    engine = create_engine(db_url)
    connection = engine.connect()
    
    # Executar a consulta SQL
    query = text("SELECT * FROM testctl.F0005 WHERE ROWNUM < 11")
    result = connection.execute(query)
    
    # Converter os resultados em uma lista de dicionários
    rows = [dict(zip(result.keys(), row)) for row in result]

    
    connection.close()
    
    return jsonify(rows)