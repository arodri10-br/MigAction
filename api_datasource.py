
from flask import Blueprint, request, jsonify
from sysdb import SessionLocal, DataSource
from datetime import datetime, timezone
from crypto_utils import encrypt_password

bp_datasource = Blueprint('datasource_api', __name__, url_prefix='/api/datasource')

# Criar datasource
@bp_datasource.route('/', methods=['POST'])
def create_datasource():
    try:
        data = request.json
        session = SessionLocal()
        if session.query(DataSource).filter_by(idDataSource = data["idDataSource"],).first():
            session.close()
            return jsonify({"error": "idDataSource já existe."}), 400
        
        datasource = DataSource(
            dsDataSource=data['dsDataSource'], 
            TpBanco=data['TpBanco'], 
            nmBanco=data['nmBanco'], 
            server=data['server'], 
            user=data['user'], 
            username=request.headers.get('username', 'admin'),
            dtAtualizacao=datetime.now(timezone.utc)
        )
        
        session.add(datasource)
        session.commit()
        session.close()
        return jsonify(success=True), 200
    except Exception as e:
        return jsonify(success=False, error=str(e)), 500

# Obter datasource
@bp_datasource.route('/', methods=['GET'])
def get_datasource_list():
    session = SessionLocal()
    datasources = session.query(DataSource).all()
    
    # Descriptografar a senha antes de enviar os dados para o frontend
    result = []
    for datasource in datasources:
        data = datasource.to_dict()
        result.append(data)    
    session.close()
    return jsonify([datasource.to_dict() for datasource in datasources])

# Obter um registro específico da tabela datasource
@bp_datasource.route('/<string:idDataSource>' , methods=['GET'])
def get_datasource(idDataSource):
    session = SessionLocal()
    datasource = session.query(DataSource).filter_by(idDataSource = idDataSource).first()
    session.close()
    if datasource:
        data = datasource.to_dict()
        return jsonify(data)
    
    return jsonify({"error": "Registro não encontrado."}), 404

# Atualizar um registro da tabela datasource
@bp_datasource.route('/<string:idDataSource>', methods=['PUT'])
def update_datasource(idDataSource):
    try:
        session = SessionLocal()
        datasource = session.query(DataSource).filter_by(idDataSource = idDataSource).first()
        if not datasource:
            session.close()
            return jsonify({"error": "Registro não encontrado."}), 404
        
        data = request.json
        datasource.idDataSource=data.get('idDataSource', datasource.idDataSource)
        datasource.dsDataSource=data.get('dsDataSource', datasource.dsDataSource)
        datasource.TpBanco=data.get('TpBanco', datasource.TpBanco)
        datasource.nmBanco=data.get('nmBanco', datasource.nmBanco)
        datasource.server=data.get('server', datasource.server)
        datasource.user=data.get('user', datasource.user)

        session.commit()
        session.close()
        return jsonify(success=True), 200
    except Exception as e:
        return jsonify(success=False, error=str(e)), 500

# Excluir um Registro da tabela datasource
@bp_datasource.route('/<string:idDataSource>', methods=['DELETE'])
def delete_datasource(idDataSource):
    session = SessionLocal()
    datasource = session.query(DataSource).filter_by(idDataSource=idDataSource).first()
    if not datasource:
        session.close()
        return jsonify({"error": "Registro não encontrado."}), 404
    
    session.delete(datasource)
    session.commit()
    session.close()
    return jsonify({"message": "Registro deletado com sucesso."})

@bp_datasource.route('/update-password/<string:idDataSource>', methods=['PUT'])
def update_password(idDataSource):
    """
    Atualiza a senha de um DataSource específico sem expor o valor na interface.
    """
    try:
        data = request.json
        new_password = data.get('new_password')

        # Verificação: Senha não pode ser vazia
        if not new_password:
            return jsonify({"error": "A nova senha não pode estar vazia."}), 400

        session = SessionLocal()
        datasource = session.query(DataSource).filter_by(idDataSource=idDataSource).first()

        if not datasource:
            session.close()
            return jsonify({"error": "Registro não encontrado."}), 404

        # Criptografar a nova senha antes de salvar
        datasource.passw = encrypt_password(new_password)
        datasource.dtAtualizacao = datetime.now(timezone.utc)  # Atualizar timestamp

        session.commit()
        session.close()
        return jsonify({"message": "Senha atualizada com sucesso."}), 200

    except Exception as e:
        return jsonify(success=False, error=str(e)), 500
