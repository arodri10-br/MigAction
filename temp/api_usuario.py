
from flask import Blueprint, request, jsonify
from sysdb import SessionLocal, Usuario

bp_usuario = Blueprint('usuario_api', __name__, url_prefix='/api/usuario')

# Criar usuario
@bp_usuario.route('/', methods=['POST'])
def create_usuario():
    try:
        data = request.json
        session = SessionLocal()
        
        if session.query(Usuario).filter_by(username=data['username']).first():
            session.close()
            return jsonify({"error": "username já existe."}), 400
        
        usuario = Usuario(
            username=data['username'], nome=data['nome'], email=data['email'], perfil=data['perfil'], status=data['status'], passw_encrypted=data['passw_encrypted']
        )
        
        session.add(usuario)
        session.commit()
        session.close()
        return jsonify(success=True), 200
    except Exception as e:
        return jsonify(success=False, error=str(e)), 500

# Obter usuario
@bp_usuario.route('/', methods=['GET'])
def get_usuario():
    session = SessionLocal()
    usuarios = session.query(Usuario).all()
    session.close()
    return jsonify([usuario.to_dict() for usuario in usuarios])

# Obter um registro específico da tabela usuario
@bp_usuario.route('/<string:username>', methods=['GET'])
def get_usuario(username):
    session = SessionLocal()
    usuario = session.query(Usuario).filter_by(username=username).first()
    session.close()
    if usuario:
        return jsonify(username.to_dict())
    return jsonify({"error": "usuario não encontrado."}), 404

# Atualizar um registro da tabela usuario
@bp_usuario.route('/<string:username>', methods=['PUT'])
def update_usuario(username):
    try:
        session = SessionLocal()
        usuario = session.query(Usuario).filter_by(username=username).first()
        if not usuario:
            session.close()
            return jsonify({"error": "Registro não encontrado."}), 404
        
        data = request.json
        usuario.username=data.get('username', usuario.username), usuario.nome=data.get('nome', usuario.nome), usuario.email=data.get('email', usuario.email), usuario.perfil=data.get('perfil', usuario.perfil), usuario.status=data.get('status', usuario.status), usuario.passw_encrypted=data.get('passw_encrypted', usuario.passw_encrypted)
        
        session.commit()
        session.close()
        return jsonify(success=True), 200
    except Exception as e:
        return jsonify(success=False, error=str(e)), 500

# Excluir um Registro da tabela usuario
@bp_usuario.route('/<string:username>', methods=['DELETE'])
def delete_usuario(username):
    session = SessionLocal()
    usuario = session.query(Usuario).filter_by(username=username).first()
    if not usuario:
        session.close()
        return jsonify({"error": "Registro não encontrado."}), 404
    
    session.delete(usuario)
    session.commit()
    session.close()
    return jsonify({"message": "Registro deletado com sucesso."})
