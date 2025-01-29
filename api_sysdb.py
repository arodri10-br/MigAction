from flask import Blueprint, request, jsonify
#from sqlalchemy.orm import Session
from sysdb import SessionLocal, Usuario
from cryptography.fernet import Fernet

# Criando um blueprint para a API de usuários
bp_usuario = Blueprint('usuario_api', __name__, url_prefix='/api/usuarios')

# Geração da chave de criptografia (deve ser armazenada de forma segura)
key = b'GY55m6boCz8OcPZIFW2QXWreTsvhn36g8AbPBGJDBYQ='  # Fernet.generate_key()
cipher_suite = Fernet(key)

# Criar um usuário
@bp_usuario.route('/', methods=['POST'])
def create_usuario():
    try:
        data = request.json
        session = SessionLocal()
        
        if session.query(Usuario).filter_by(username=data['username']).first():
            session.close()
            return jsonify({"error": "Usuário já existe."}), 400
        
        usuario = Usuario(
            username=data['username'],
            nome=data['nome'],
            email=data['email'],
            perfil=data['perfil'],
            status=data['status'],
            passw=data['password']  # A senha será automaticamente criptografada
        )
        
        session.add(usuario)
        session.commit()
        session.close()
        return jsonify(success=True), 200
    except Exception as e:
        return jsonify(success=False, error=str(e)), 500

# Obter todos os usuários
@bp_usuario.route('/', methods=['GET'])
def get_usuarios():
    session = SessionLocal()
    usuarios = session.query(Usuario).all()
    session.close()
    return jsonify([usuario.to_dict() for usuario in usuarios])

# Obter um usuário específico
@bp_usuario.route('/<string:username>', methods=['GET'])
def get_usuario(username):
    session = SessionLocal()
    usuario = session.query(Usuario).filter_by(username=username).first()
    session.close()
    if usuario:
        return jsonify(usuario.to_dict())
    return jsonify({"error": "Usuário não encontrado."}), 404

# Atualizar um usuário
@bp_usuario.route('/<string:username>', methods=['PUT'])
def update_usuario(username):
    try:
        session = SessionLocal()
        usuario = session.query(Usuario).filter_by(username=username).first()
        if not usuario:
            session.close()
            return jsonify({"error": "Usuário não encontrado."}), 404
        
        data = request.json
        usuario.nome = data.get('nome', usuario.nome)
        usuario.email = data.get('email', usuario.email)
        usuario.perfil = data.get('perfil', usuario.perfil)
        usuario.status = data.get('status', usuario.status)
        if 'passw' in data:
            usuario.passw = data['password']  # A senha sera automaticamente criptografada
        
        session.commit()
        session.close()
        return jsonify(success=True), 200
    except Exception as e:
        return jsonify(success=False, error=str(e)), 500

# Deletar um usuário
@bp_usuario.route('/<string:username>', methods=['DELETE'])
def delete_usuario(username):
    session = SessionLocal()
    usuario = session.query(Usuario).filter_by(username=username).first()
    if not usuario:
        session.close()
        return jsonify({"error": "Usuário não encontrado."}), 404
    
    session.delete(usuario)
    session.commit()
    session.close()
    return jsonify({"message": "Usuário deletado com sucesso."})
