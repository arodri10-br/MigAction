
from flask import Blueprint, request, jsonify
from sysdb import SessionLocal, SuppDataConfig
from datetime import datetime, timezone

bp_suppdataconfig = Blueprint('suppdataconfig_api', __name__, url_prefix='/api/suppdataconfig')

# Criar suppdataconfig
@bp_suppdataconfig.route('/', methods=['POST'])
def create_suppdataconfig():
    try:
        data = request.json
        session = SessionLocal()
        
        if session.query(SuppDataConfig).filter_by(codSupData=data['codSupData']).first():
            session.close()
            return jsonify({"error": "codSupData já existe."}), 400
        
        suppdataconfig = SuppDataConfig(
            codSupData=data['codSupData'], 
            DescSupData=data['DescSupData'], 
            Chave1=data['Chave1'], 
            Chave2=data['Chave2'], 
            Campo1=data['Campo1'], 
            Campo2=data['Campo2'], 
            Campo3=data['Campo3'], 
            Campo4=data['Campo4'], 
            Campo5=data['Campo5'], 
            Campo6=data['Campo6'], 
            Campo7=data['Campo7'], 
            Campo8=data['Campo8'], 
            Campo9=data['Campo9'], 
            Campo10=data['Campo10'], 
            Tipo1=data['Tipo1'], 
            Tipo2=data['Tipo2'], 
            Tipo3=data['Tipo3'], 
            Tipo4=data['Tipo4'], 
            Tipo5=data['Tipo5'], 
            Tipo6=data['Tipo6'], 
            Tipo7=data['Tipo7'], 
            Tipo8=data['Tipo8'], 
            Tipo9=data['Tipo9'], 
            Tipo10=data['Tipo10'], 
            PermNull1=data['PermNull1'], 
            PermNull2=data['PermNull2'], 
            PermNull3=data['PermNull3'], 
            PermNull4=data['PermNull4'], 
            PermNull5=data['PermNull5'], 
            PermNull6=data['PermNull6'], 
            PermNull7=data['PermNull7'], 
            PermNull8=data['PermNull8'], 
            PermNull9=data['PermNull9'], 
            PermNull10=data['PermNull10']
        )
        
        session.add(suppdataconfig)
        session.commit()
        session.close()
        return jsonify(success=True), 200
    except Exception as e:
        return jsonify(success=False, error=str(e)), 500

# Obter suppdataconfig
@bp_suppdataconfig.route('/', methods=['GET'])
def get_suppdataconfig_list():
    session = SessionLocal()
    suppdataconfigs = session.query(SuppDataConfig).all()
    session.close()
    return jsonify([suppdataconfig.to_dict() for suppdataconfig in suppdataconfigs])

# Obter um registro específico da tabela suppdataconfig
@bp_suppdataconfig.route('/<string:codSupData>', methods=['GET'])
def get_suppdataconfig(codSupData):
    session = SessionLocal()
    suppdataconfig = session.query(SuppDataConfig).filter_by(codSupData=codSupData).first()
    session.close()
    if suppdataconfig:
        return jsonify(suppdataconfig.to_dict())
    return jsonify({"error": "suppdataconfig não encontrado."}), 404

# Atualizar um registro da tabela suppdataconfig
@bp_suppdataconfig.route('/<string:codSupData>', methods=['PUT'])
def update_suppdataconfig(codSupData):
    try:
        session = SessionLocal()
        suppdataconfig = session.query(SuppDataConfig).filter_by(codSupData=codSupData).first()
        if not suppdataconfig:
            session.close()
            return jsonify({"error": "Registro não encontrado."}), 404
        
        data = request.json
        suppdataconfig.codSupData=data.get('codSupData', suppdataconfig.codSupData)
        suppdataconfig.DescSupData=data.get('DescSupData', suppdataconfig.DescSupData)
        suppdataconfig.Chave1=data.get('Chave1', suppdataconfig.Chave1)
        suppdataconfig.Chave2=data.get('Chave2', suppdataconfig.Chave2)
        suppdataconfig.Campo1=data.get('Campo1', suppdataconfig.Campo1)
        suppdataconfig.Campo2=data.get('Campo2', suppdataconfig.Campo2)
        suppdataconfig.Campo3=data.get('Campo3', suppdataconfig.Campo3)
        suppdataconfig.Campo4=data.get('Campo4', suppdataconfig.Campo4)
        suppdataconfig.Campo5=data.get('Campo5', suppdataconfig.Campo5)
        suppdataconfig.Campo6=data.get('Campo6', suppdataconfig.Campo6)
        suppdataconfig.Campo7=data.get('Campo7', suppdataconfig.Campo7)
        suppdataconfig.Campo8=data.get('Campo8', suppdataconfig.Campo8)
        suppdataconfig.Campo9=data.get('Campo9', suppdataconfig.Campo9)
        suppdataconfig.Campo10=data.get('Campo10', suppdataconfig.Campo10)
        suppdataconfig.Tipo1=data.get('Tipo1', suppdataconfig.Tipo1)
        suppdataconfig.Tipo2=data.get('Tipo2', suppdataconfig.Tipo2)
        suppdataconfig.Tipo3=data.get('Tipo3', suppdataconfig.Tipo3)
        suppdataconfig.Tipo4=data.get('Tipo4', suppdataconfig.Tipo4)
        suppdataconfig.Tipo5=data.get('Tipo5', suppdataconfig.Tipo5)
        suppdataconfig.Tipo6=data.get('Tipo6', suppdataconfig.Tipo6)
        suppdataconfig.Tipo7=data.get('Tipo7', suppdataconfig.Tipo7)
        suppdataconfig.Tipo8=data.get('Tipo8', suppdataconfig.Tipo8)
        suppdataconfig.Tipo9=data.get('Tipo9', suppdataconfig.Tipo9)
        suppdataconfig.Tipo10=data.get('Tipo10', suppdataconfig.Tipo10)
        suppdataconfig.PermNull1=data.get('PermNull1', suppdataconfig.PermNull1)
        suppdataconfig.PermNull2=data.get('PermNull2', suppdataconfig.PermNull2)
        suppdataconfig.PermNull3=data.get('PermNull3', suppdataconfig.PermNull3)
        suppdataconfig.PermNull4=data.get('PermNull4', suppdataconfig.PermNull4)
        suppdataconfig.PermNull5=data.get('PermNull5', suppdataconfig.PermNull5)
        suppdataconfig.PermNull6=data.get('PermNull6', suppdataconfig.PermNull6)
        suppdataconfig.PermNull7=data.get('PermNull7', suppdataconfig.PermNull7)
        suppdataconfig.PermNull8=data.get('PermNull8', suppdataconfig.PermNull8)
        suppdataconfig.PermNull9=data.get('PermNull9', suppdataconfig.PermNull9)
        suppdataconfig.PermNull10=data.get('PermNull10', suppdataconfig.PermNull10)
        
        session.commit()
        session.close()
        return jsonify(success=True), 200
    except Exception as e:
        return jsonify(success=False, error=str(e)), 500

# Excluir um Registro da tabela suppdataconfig
@bp_suppdataconfig.route('/<string:codSupData>', methods=['DELETE'])
def delete_suppdataconfig(codSupData):
    session = SessionLocal()
    suppdataconfig = session.query(SuppDataConfig).filter_by(codSupData=codSupData).first()
    if not suppdataconfig:
        session.close()
        return jsonify({"error": "Registro não encontrado."}), 404
    
    session.delete(suppdataconfig)
    session.commit()
    session.close()
    return jsonify({"message": "Registro deletado com sucesso."})
