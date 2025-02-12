
from flask import Blueprint, request, jsonify
from sysdb import SessionLocal, Carga
from datetime import datetime, timezone
from sysdb import Script, DataSource
from sqlalchemy import create_engine
from sqlalchemy.sql import text

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
        session = SessionLocal()
        idProjeto = request.json['idProjeto']
        ordem = request.json['ordem']
        scripts = session.query(Script).filter_by(idProjeto=idProjeto, ordem=ordem).all()
        if not scripts:
            session.close()
            return jsonify({"error": "No data selected"}), 404
        
        # Iterate over each script and create a corresponding carga record
        for script in scripts:
            carga = Carga(
                uniqueKeyId=None,  # Autoincrement
                idProjeto=idProjeto,
                ordem=ordem,
                seq=script.seq,
                idDSOrigem=request.json['idDSOrigem'],
                idDSDestino=request.json['idDSDestino'],
                operacao=request.json['operacao'],
                cmdInsert=script.cmdInsert,
                status='P',
                dbOper=request.json['dbOper'],
                dtCriacao=datetime.now(timezone.utc),
                dtAtualizacao=datetime.now(timezone.utc),
                username=request.headers.get('username', 'admin')
            )
            session.add(carga)

        session.commit()
        session.close()
        return jsonify(success=True), 200
    except Exception as e:
        return jsonify(success=False, error=str(e)), 500

@bp_carga.route('/exec/<string:idProjeto>/<string:ordem>', methods=['PUT'])
def exec_carga(idProjeto,ordem):
    #from sysdb import Datasource
    try:
        session = SessionLocal()
        cargas = session.query(Carga).filter_by(idProjeto=idProjeto, ordem=ordem, status="P").all()
        if not cargas:
            session.close()
            return jsonify({"error": "No data selected."}), 404

        for carga in cargas:
            script = session.query(Script).filter_by(idProjeto=idProjeto, ordem=ordem, seq=carga.seq).first()
            if not script:
                continue

            # Open connections
            ds_origem = session.query(DataSource).filter_by(idDataSource=carga.idDSOrigem).first()
            ds_destino = session.query(DataSource).filter_by(idDataSource=carga.idDSDestino).first()
            if not ds_origem or not ds_destino:
                continue

            engine_origem = create_engine(ds_origem.connection_string)
            engine_destino = create_engine(ds_destino.connection_string)

            with engine_origem.connect() as conn_origem, engine_destino.connect() as conn_destino:
                result = conn_origem.execute(text(carga.cmdInsert))
                rows = result.fetchall()
                count_inserted = 0
                print(f"Numero de registros selecionados : {len(rows)}")

                columns = result.keys()
                values = [dict(zip(result.keys(), row)) for row in rows]
                insert_command = f"INSERT INTO {script.Tabela} ({', '.join(columns)}) VALUES ({', '.join([f':{col}' for col in columns])})"
                for row in rows:
                    print(f"Inserting Command : {insert_command}")
                    conn_destino.execute(text(insert_command), dict(zip(columns, row)))
                    count_inserted += 1

                if count_inserted == len(rows):
                    carga.status = 'S'
                else:
                    carga.status = 'E'
                carga.dtExec = datetime.now(timezone.utc)

        session.commit()
        session.close()
        return jsonify(success=True), 200
    except Exception as e:
        print(f"Erro função exec_carga : {e}")
        return jsonify(success=False, error=str(e)), 500