from flask import Blueprint, request, jsonify
from sysdb import SessionLocal, Processo
from datetime import datetime, timezone

bp_processo = Blueprint('processo_api', __name__, url_prefix='/api/processo')

# Criar processo
@bp_processo.route('/', methods=['POST'])
def create_processo():
    try:
        data = request.json
        session = SessionLocal()
        if session.query(Processo).filter_by(idProjeto = data["idProjeto"],ordem = data["ordem"],).first():
            session.close()
            return jsonify({"error": "idProjeto já existe."}), 400
        
        processo = Processo(
            idProjeto=data['idProjeto'], 
            ordem=data['ordem'], 
            dsProcesso=data['dsProcesso'], 
            statusProcesso=data['statusProcesso'], 
            dataExecucao=data.get('dataExecucao', None),
            username=request.headers.get('username', 'admin'),
            dtAtualizacao=datetime.now(timezone.utc)
        )
        
        session.add(processo)
        session.commit()
        session.close()
        return jsonify(success=True), 200
    except Exception as e:
        return jsonify(success=False, error=str(e)), 500

# Obter processo
@bp_processo.route('/<string:idProjeto>', methods=['GET'])
def get_processo_list(idProjeto):
    session = SessionLocal()
    processos = session.query(Processo).filter_by(idProjeto = idProjeto).all()
    session.close()
    return jsonify([processo.to_dict() for processo in processos])

# Obter um registro específico da tabela processo
@bp_processo.route('/<string:idProjeto>/<string:ordem>' , methods=['GET'])
def get_processo(idProjeto,ordem):
    session = SessionLocal()
    processo = session.query(Processo).filter_by(idProjeto = idProjeto,ordem = ordem).first()
    session.close()
    if processo:
        return jsonify(processo.to_dict())
    return jsonify({"error": "Registro não encontrado."}), 404

# Atualizar um registro da tabela processo
@bp_processo.route('/<string:idProjeto>/<string:ordem>', methods=['PUT'])
def update_processo(idProjeto,ordem):
    try:
        session = SessionLocal()
        processo = session.query(Processo).filter_by(idProjeto = idProjeto,ordem = ordem).first()
        if not processo:
            session.close()
            return jsonify({"error": "Registro não encontrado."}), 404
        
        data = request.json
        processo.idProjeto=data.get('idProjeto', processo.idProjeto)
        processo.ordem=data.get('ordem', processo.ordem)
        processo.dsProcesso=data.get('dsProcesso', processo.dsProcesso)
        processo.statusProcesso=data.get('statusProcesso', processo.statusProcesso)
        processo.dataExecucao=data.get('dataExecucao', processo.dataExecucao)
        
        session.commit()
        session.close()
        return jsonify(success=True), 200
    except Exception as e:
        return jsonify(success=False, error=str(e)), 500

# Excluir um Registro da tabela processo
@bp_processo.route('/<string:idProjeto>/<string:ordem>', methods=['DELETE'])
def delete_processo(idProjeto,ordem):
    session = SessionLocal()
    processo = session.query(Processo).filter_by(idProjeto=idProjeto,ordem = ordem).first()
    if not processo:
        session.close()
        return jsonify({"error": "Registro não encontrado."}), 404
    
    session.delete(processo)
    session.commit()
    session.close()
    return jsonify({"message": "Registro deletado com sucesso."})
