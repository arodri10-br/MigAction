
from flask import Blueprint, request, jsonify
from sysdb import SessionLocal, SuppDataDet
from datetime import datetime, timezone

bp_suppdatadet = Blueprint('suppdatadet_api', __name__, url_prefix='/api/suppdatadet')

# Criar suppdatadet
@bp_suppdatadet.route('/', methods=['POST'])
def create_suppdatadet():
    try:
        data = request.json
        session = SessionLocal()
        
        if session.query(SuppDataDet).filter_by(IdProjeto=data['IdProjeto'], codSupData=data['codSupData'],Chave1=data['Chave1'],Chave2=data['Chave2']).first():
            session.close()
            return jsonify({"error": "IdProjeto já existe."}), 400
        
        suppdatadet = SuppDataDet(
            IdProjeto=data['IdProjeto'], 
            codSupData=data['codSupData'], 
            Chave1=data['Chave1'], 
            Chave2=data['Chave2'], 
            Valor1=data['Valor1'], 
            Valor2=data['Valor2'], 
            Valor3=data['Valor3'], 
            Valor4=data['Valor4'], 
            Valor5=data['Valor5'], 
            Valor6=data['Valor6'], 
            Valor7=data['Valor7'], 
            Valor8=data['Valor8'], 
            Valor9=data['Valor9'], 
            Valor10=data['Valor10'],
            username=request.headers.get('username', 'admin'),
            dtAtualizacao=datetime.now(timezone.utc)
        )
        
        session.add(suppdatadet)
        session.commit()
        session.close()
        return jsonify(success=True), 200
    except Exception as e:
        return jsonify(success=False, error=str(e)), 500

# Obter suppdatadet
@bp_suppdatadet.route('/', methods=['GET'])
def get_suppdatadet_list():
    session = SessionLocal()
    suppdatadets = session.query(SuppDataDet).all()
    session.close()
    return jsonify([suppdatadet.to_dict() for suppdatadet in suppdatadets])

# Obter um registro específico da tabela suppdatadet
@bp_suppdatadet.route('/<string:IdProjeto>/<string:codSupData>/<string:Chave1>/', methods=['GET'])
@bp_suppdatadet.route('/<string:IdProjeto>/<string:codSupData>/<string:Chave1>/<string:Chave2>', methods=['GET'])
def get_suppdatadet(IdProjeto, codSupData, Chave1, Chave2=None):
    session = SessionLocal()
    query = session.query(SuppDataDet).filter_by(
        IdProjeto=IdProjeto,
        codSupData=codSupData,
        Chave1=Chave1
    )
    if Chave2 is not None:
        query = query.filter_by(Chave2=Chave2)
    suppdatadet = query.first()
    session.close()
    if suppdatadet:
        return jsonify(suppdatadet.to_dict())
    return jsonify({"error": "Registro não encontrado."}), 404

# Atualizar um registro da tabela suppdatadet

@bp_suppdatadet.route('/<string:IdProjeto>/<string:codSupData>/<string:Chave1>/', methods=['PUT'])
@bp_suppdatadet.route('/<string:IdProjeto>/<string:codSupData>/<string:Chave1>/<string:Chave2>', methods=['PUT'])
def update_suppdatadet(IdProjeto, codSupData, Chave1, Chave2=None):
    try:
        session = SessionLocal()
        query = session.query(SuppDataDet).filter_by(
            IdProjeto=IdProjeto,
            codSupData=codSupData,
            Chave1=Chave1
        )
        if Chave2 is not None:
            query = query.filter_by(Chave2=Chave2)
        suppdatadet = query.first()
        if not suppdatadet:
            session.close()
            return jsonify({"error": "Registro não encontrado."}), 404
        
        data = request.json
        suppdatadet.IdProjeto=data.get('IdProjeto', suppdatadet.IdProjeto)
        suppdatadet.codSupData=data.get('codSupData', suppdatadet.codSupData)
        suppdatadet.Chave1=data.get('Chave1', suppdatadet.Chave1)
        suppdatadet.Chave2=data.get('Chave2', suppdatadet.Chave2)
        suppdatadet.Valor1=data.get('Valor1', suppdatadet.Valor1)
        suppdatadet.Valor2=data.get('Valor2', suppdatadet.Valor2)
        suppdatadet.Valor3=data.get('Valor3', suppdatadet.Valor3)
        suppdatadet.Valor4=data.get('Valor4', suppdatadet.Valor4)
        suppdatadet.Valor5=data.get('Valor5', suppdatadet.Valor5)
        suppdatadet.Valor6=data.get('Valor6', suppdatadet.Valor6)
        suppdatadet.Valor7=data.get('Valor7', suppdatadet.Valor7)
        suppdatadet.Valor8=data.get('Valor8', suppdatadet.Valor8)
        suppdatadet.Valor9=data.get('Valor9', suppdatadet.Valor9)
        suppdatadet.Valor10=data.get('Valor10', suppdatadet.Valor10)
        
        session.commit()
        session.close()
        return jsonify(success=True), 200
    except Exception as e:
        return jsonify(success=False, error=str(e)), 500

# Excluir um Registro da tabela suppdatadet
@bp_suppdatadet.route('/<string:IdProjeto>', methods=['DELETE'])
def delete_suppdatadet(IdProjeto):
    session = SessionLocal()
    suppdatadet = session.query(SuppDataDet).filter_by(IdProjeto=IdProjeto).first()
    if not suppdatadet:
        session.close()
        return jsonify({"error": "Registro não encontrado."}), 404
    
    session.delete(suppdatadet)
    session.commit()
    session.close()
    return jsonify({"message": "Registro deletado com sucesso."})
