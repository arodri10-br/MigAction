
from flask import Blueprint, request, jsonify
from sysdb import SessionLocal, Carga
from datetime import datetime, timezone

bp_carga = Blueprint('carga_api', __name__, url_prefix='/api/carga')

# Criar carga
@bp_carga.route('/', methods=['POST'])
def create_carga():
    try:
        data = request.json
        session = SessionLocal()
        if session.query(Carga).filter_by(uniqueKeyId = data["uniqueKeyId"],).first():
            session.close()
            return jsonify({"error": "uniqueKeyId já existe."}), 400
        
        carga = Carga(
            idProjeto=data['idProjeto'], 
            ordem=data['ordem'], 
            seq=data['seq'], 
            idDSOrigem=data['idDSOrigem'], 
            idDSDestino=data['idDSDestino'], 
            operacao=data['operacao'], 
            status=data['status'], 
            dbOper=data['dbOper'], 
            dtCriacao=data['dtCriacao'], 
            dtExec=data['dtExec'],
            username=request.headers.get('username', 'admin'),
            dtAtualizacao=datetime.now(timezone.utc)
        )
        
        session.add(carga)
        session.commit()
        session.close()
        return jsonify(success=True), 200
    except Exception as e:
        return jsonify(success=False, error=str(e)), 500

# Obter carga
@bp_carga.route('/', methods=['GET'])
def get_carga_list():
    session = SessionLocal()
    cargas = session.query(Carga).all()
    session.close()
    return jsonify([carga.to_dict() for carga in cargas])

# Obter um registro específico da tabela carga
@bp_carga.route('/<string:uniqueKeyId>' , methods=['GET'])
def get_carga(uniqueKeyId):
    session = SessionLocal()
    carga = session.query(Carga).filter_by(uniqueKeyId = uniqueKeyId).first()
    session.close()
    if carga:
        return jsonify(carga.to_dict())
    return jsonify({"error": "Registro não encontrado."}), 404

# Atualizar um registro da tabela carga
@bp_carga.route('/<string:uniqueKeyId>', methods=['PUT'])
def update_carga(uniqueKeyId):
    try:
        session = SessionLocal()
        carga = session.query(Carga).filter_by(uniqueKeyId = uniqueKeyId).first()
        if not carga:
            session.close()
            return jsonify({"error": "Registro não encontrado."}), 404
        
        data = request.json
        carga.uniqueKeyId=data.get('uniqueKeyId', carga.uniqueKeyId)
        carga.idProjeto=data.get('idProjeto', carga.idProjeto)
        carga.ordem=data.get('ordem', carga.ordem)
        carga.seq=data.get('seq', carga.seq)
        carga.idDSOrigem=data.get('idDSOrigem', carga.idDSOrigem)
        carga.idDSDestino=data.get('idDSDestino', carga.idDSDestino)
        carga.operacao=data.get('operacao', carga.operacao)
        carga.status=data.get('status', carga.status)
        carga.dbOper=data.get('dbOper', carga.dbOper)
        carga.dtCriacao=data.get('dtCriacao', carga.dtCriacao)
        carga.dtExec=data.get('dtExec', carga.dtExec)
        
        session.commit()
        session.close()
        return jsonify(success=True), 200
    except Exception as e:
        return jsonify(success=False, error=str(e)), 500

# Excluir um Registro da tabela carga
@bp_carga.route('/<string:uniqueKeyId>', methods=['DELETE'])
def delete_carga(uniqueKeyId):
    session = SessionLocal()
    carga = session.query(Carga).filter_by(uniqueKeyId=uniqueKeyId).first()
    if not carga:
        session.close()
        return jsonify({"error": "Registro não encontrado."}), 404
    
    session.delete(carga)
    session.commit()
    session.close()
    return jsonify({"message": "Registro deletado com sucesso."})

# Criar carga de forma massiva baseada na tabela de scripts
@bp_carga.route('/geracao', methods=['POST'])
def geracao_carga():
    try:
        data = request.json
        session = SessionLocal()
        if session.query(Carga).filter_by(uniqueKeyId = data["uniqueKeyId"],).first():
            session.close()
            return jsonify({"error": "uniqueKeyId já existe."}), 400
        
        carga = Carga(
            idProjeto=data['idProjeto'], 
            ordem=data['ordem'], 
            seq=data['seq'], 
            idDSOrigem=data['idDSOrigem'], 
            idDSDestino=data['idDSDestino'], 
            operacao=data['operacao'], 
            status=data['status'], 
            dbOper=data['dbOper'], 
            dtCriacao=data['dtCriacao'], 
            dtExec=data['dtExec'],
            username=request.headers.get('username', 'admin'),
            dtAtualizacao=datetime.now(timezone.utc)
        )
        
        session.add(carga)
        session.commit()
        session.close()
        return jsonify(success=True), 200
    except Exception as e:
        return jsonify(success=False, error=str(e)), 500
