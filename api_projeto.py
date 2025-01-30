
from flask import Blueprint, request, jsonify
from sysdb import SessionLocal, Projeto
from datetime import datetime, timezone

bp_projeto = Blueprint('projeto_api', __name__, url_prefix='/api/projeto')

# Criar projeto
@bp_projeto.route('/', methods=['POST'])
def create_projeto():
    try:
        data = request.json
        session = SessionLocal()
        
        if session.query(Projeto).filter_by(idProjeto=data['idProjeto']).first():
            session.close()
            return jsonify({"error": "idProjeto já existe."}), 400
        
        projeto = Projeto(
                    idProjeto=data['idProjeto'], 
                    codProjeto=data['codProjeto'], 
                    descProjeto=data['descProjeto'], 
                    status=data['status'], 
                    username=request.headers.get('username', 'admin'),
                    dtAtualizacao=datetime.now(timezone.utc)
                )
        
        session.add(projeto)
        session.commit()
        session.close()
        return jsonify(success=True), 200
    except Exception as e:
        print(f"Error: {str(e)}")
        jsonify(success=False, error=str(e)), 500

# Obter projeto
@bp_projeto.route('/', methods=['GET'])
def get_projeto_list():
    session = SessionLocal()
    projetos = session.query(Projeto).all()
    session.close()
    return jsonify([projeto.to_dict() for projeto in projetos])

# Obter um registro específico da tabela projeto
@bp_projeto.route('/<string:idProjeto>', methods=['GET'])
def get_projeto(idProjeto):
    session = SessionLocal()
    projeto = session.query(Projeto).filter_by(idProjeto=idProjeto).first()
    session.close()
    if projeto:
        return jsonify(idProjeto.to_dict())
    return jsonify({"error": "projeto não encontrado."}), 404

# Atualizar um registro da tabela projeto
@bp_projeto.route('/<string:idProjeto>', methods=['PUT'])
def update_projeto(idProjeto):
    try:
        session = SessionLocal()
        projeto = session.query(Projeto).filter_by(idProjeto=idProjeto).first()
        if not projeto:
            session.close()
            return jsonify({"error": "Registro não encontrado."}), 404
        
        data = request.json
        projeto.idProjeto=data.get('idProjeto', projeto.idProjeto)
        projeto.codProjeto=data.get('codProjeto', projeto.codProjeto)
        projeto.descProjeto=data.get('descProjeto', projeto.descProjeto)
        projeto.status=data.get('status', projeto.status)
        
        session.commit()
        session.close()
        return jsonify(success=True), 200
    except Exception as e:
        return jsonify(success=False, error=str(e)), 500

# Excluir um Registro da tabela projeto
@bp_projeto.route('/<string:idProjeto>', methods=['DELETE'])
def delete_projeto(idProjeto):
    session = SessionLocal()
    projeto = session.query(Projeto).filter_by(idProjeto=idProjeto).first()
    if not projeto:
        session.close()
        return jsonify({"error": "Registro não encontrado."}), 404
    
    session.delete(projeto)
    session.commit()
    session.close()
    return jsonify({"message": "Registro deletado com sucesso."})
