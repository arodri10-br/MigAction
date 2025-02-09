from flask import Blueprint, request, jsonify
from sysdb import SessionLocal, Script, DataSource
from datetime import datetime, timezone
from sqlalchemy import create_engine, text
from configparser import ConfigParser

bp_script = Blueprint('script_api', __name__, url_prefix='/api/script')

# Read configuration
config = ConfigParser()
config.read('config.ini')
rows_per_page = int(config['DEFAULT']['rows_per_page'])

# Criar script
@bp_script.route('/', methods=['POST'])
def create_script():
    try:
        data = request.json
        session = SessionLocal()
        if session.query(Script).filter_by(idProjeto = data["idProjeto"],ordem = data["ordem"],seq = data["seq"],).first():
            session.close()
            return jsonify({"error": "idProjeto já existe."}), 400
        
        script = Script(
            idProjeto=data['idProjeto'], 
            ordem=data['ordem'], 
            seq=data['seq'], 
            Tabela=data['Tabela'], 
            Modulo=data['Modulo'], 
            descProcesso=data['descProcesso'], 
            responsavel=data['responsavel'], 
            programa=data['programa'],
            selDados=data.get('selDados', None), 
            cmdInsert=data.get('cmdInsert', None), 
            username=request.headers.get('username', 'admin'),
            dtAtualizacao=datetime.now(timezone.utc)
        )
        
        session.add(script)
        session.commit()
        session.close()
        return jsonify(success=True), 200
    except Exception as e:
        return jsonify(success=False, error=str(e)), 500

# Obter script
@bp_script.route('/', methods=['GET'])
def get_script_list():
    session = SessionLocal()
    scripts = session.query(Script).all()
    session.close()
    return jsonify([script.to_dict() for script in scripts])

# Obter um registro específico da tabela script
@bp_script.route('/<string:idProjeto>/<string:ordem>/<string:seq>' , methods=['GET'])
def get_script(idProjeto,ordem,seq):
    session = SessionLocal()
    script = session.query(Script).filter_by(idProjeto = idProjeto,ordem = ordem,seq = seq).first()
    session.close()
    if script:
        return jsonify(script.to_dict())
    return jsonify({"error": "Registro não encontrado."}), 404

# Atualizar um registro da tabela script
@bp_script.route('/<string:idProjeto>/<string:ordem>/<string:seq>', methods=['PUT'])
def update_script(idProjeto,ordem,seq):
    try:
        session = SessionLocal()
        script = session.query(Script).filter_by(idProjeto = idProjeto,ordem = ordem,seq = seq).first()
        if not script:
            session.close()
            return jsonify({"error": "Registro não encontrado."}), 404
        
        data = request.json
        script.idProjeto=data.get('idProjeto', script.idProjeto)
        script.ordem=data.get('ordem', script.ordem)
        script.seq=data.get('seq', script.seq)
        script.Tabela=data.get('Tabela', script.Tabela)
        script.Modulo=data.get('Modulo', script.Modulo)
        script.descProcesso=data.get('descProcesso', script.descProcesso)
        script.responsavel=data.get('responsavel', script.responsavel)
        script.programa=data.get('programa', script.programa)
        script.selDados=data.get('selDados', script.selDados)
        script.cmdInsert=data.get('cmdInsert', script.cmdInsert)
        script.username=data.get('username', script.username)
        script.dtAtualizacao=data.get('dtAtualizacao', script.dtAtualizacao)
        
        session.commit()
        session.close()
        return jsonify(success=True), 200
    except Exception as e:
        return jsonify(success=False, error=str(e)), 500

# Excluir um Registro da tabela script
@bp_script.route('/<string:idProjeto>/<string:ordem>/<string:seq>', methods=['DELETE'])
def delete_script(idProjeto,ordem,seq):
    session = SessionLocal()
    script = session.query(Script).filter_by(idProjeto=idProjeto, ordem=ordem, seq=seq).first()
    if not script:
        session.close()
        return jsonify({"error": "Registro não encontrado."}), 404
    
    session.delete(script)
    session.commit()
    session.close()
    return jsonify({"message": "Registro deletado com sucesso."})

@bp_script.route('/validateSQL/', methods=['PUT'])
def validate_sql():
    try:
        data = request.json
        idDataSource = data.get('idDataSource')
        sql = data.get('sql')

        session = SessionLocal()
        datasource = session.query(DataSource).filter_by(idDataSource=idDataSource).first()
        session.close()

        if not datasource:
            return jsonify({"error": "Registro do Data Source não encontrado."}), 404

        strConn = datasource.connection_string
        # Criar engine do SQLAlchemy com a conexão correta
        engine = create_engine(strConn)

        # Executar SQL sem paginação
        with engine.connect() as connection:
            #result = connection.execute(text(sql))
            result = connection.execute(text(sql)).mappings().all()
            data = [dict(row) for row in result]

        return jsonify(data)
    
    except Exception as e:
        return jsonify(success=False, error=str(e)), 500