# api_sysdb.py
from flask import Blueprint, request, jsonify
from sysdb import SessionLocal, DatabaseConfig

bp = Blueprint('api_sysdb', __name__)

@bp.route('/config', methods=['GET'])
def get_configs():
    session = SessionLocal()
    configs = session.query(DatabaseConfig).all()
    session.close()
    print(configs)
    return jsonify([config.__dict__ for config in configs])

@bp.route('/config/<int:id>', methods=['GET'])
def get_config(id):
    session = SessionLocal()
    config = session.query(DatabaseConfig).get(id)
    session.close()
    if config:
        return jsonify(config.__dict__)
    else:
        return jsonify({"message": "Configuração não encontrada"}), 404

@bp.route('/config', methods=['POST'])
def add_config():
    session = SessionLocal()
    data = request.json
    new_config = DatabaseConfig(
        environment=data['environment'],
        db_type=data['db_type'],
        host=data['host'],
        port=data['port'],
        database=data['database'],
        username=data['username'],
        password=data['password']  # A senha será automaticamente criptografada
    )
    session.add(new_config)
    session.commit()
    session.close()
    return jsonify({"message": "Configuração adicionada com sucesso!"})

@bp.route('/config/<int:id>', methods=['PUT'])
def update_config(id):
    session = SessionLocal()
    data = request.json
    config = session.query(DatabaseConfig).get(id)
    if config:
        config.environment = data['environment']
        config.db_type = data['db_type']
        config.host = data['host']
        config.port = data['port']
        config.database = data['database']
        config.username = data['username']
        if 'password' in data:
            config.password = data['password']  # A senha será automaticamente criptografada
        session.commit()
        session.close()
        return jsonify({"message": "Configuração atualizada com sucesso!"})
    else:
        session.close()
        return jsonify({"message": "Configuração não encontrada"}), 404

@bp.route('/config/<int:id>', methods=['DELETE'])
def delete_config(id):
    session = SessionLocal()
    config = session.query(DatabaseConfig).get(id)
    if config:
        session.delete(config)
        session.commit()
        session.close()
        return jsonify({"message": "Configuração deletada com sucesso!"})
    else:
        session.close()
        return jsonify({"message": "Configuração não encontrada"}), 404

@bp.route('/config/<int:id>/password', methods=['GET'])
def get_password(id):
    session = SessionLocal()
    config = session.query(DatabaseConfig).get(id)
    session.close()
    if config:
        return jsonify({"password": config.get_password()})
    else:
        return jsonify({"message": "Configuração não encontrada"}), 404

