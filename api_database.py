# api_database.py
from flask import Blueprint, jsonify
from sqlalchemy import create_engine, inspect, text
from sysdb import SessionLocal

bp_database = Blueprint('api_database', __name__)

@bp_database.route('/first_config', methods=['GET'])
def get_first_config():
    pass

@bp_database.route('/execute_query', methods=['GET'])
def execute_query():
    pass
