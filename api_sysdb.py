# api_sysdb.py
from flask import Blueprint


bp = Blueprint('api_sysdb', __name__)

@bp.route('/config', methods=['GET'])
def get_configs():
    pass

@bp.route('/config/<int:id>', methods=['GET'])
def get_config(id):
    pass

@bp.route('/config', methods=['POST'])
def add_config():
    pass

@bp.route('/config/<int:id>', methods=['PUT'])
def update_config(id):
    pass

@bp.route('/config/<int:id>', methods=['DELETE'])
def delete_config(id):
    pass

@bp.route('/config/<int:id>/password', methods=['GET'])
def get_password(id):
    pass

