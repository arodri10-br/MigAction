from flask import Blueprint, render_template, request, jsonify, abort
#from flask_login import login_required, current_user
from sysdb import engine
import sqlalchemy as sa
from sqlalchemy import inspect
import configparser
import os
import re

# Criar Blueprint
generate_code_bp = Blueprint('generate_code', __name__, url_prefix='/generate-code')

# carregar as configurações do arquivo config.ini
config = configparser.ConfigParser()
config.read('config.ini')
temp_dir = config.get('Diretorios', 'temp', fallback='./temp')

# Se o diretorio nao exisitr faz a criacao 
os.makedirs(temp_dir, exist_ok=True)

# Obter tabelas disponíveis no banco de dados
def get_database_tables():
    metadata = sa.MetaData()
    metadata.reflect(bind=engine)
    return [{"name": table_name} for table_name in metadata.tables.keys()]

# Obter colunas de uma tabela específica
def get_table_columns(table_name):
    """
    Obtém os campos de uma tabela e suas características, incluindo tamanho e tipo.
    """
    inspector = inspect(engine) 

    try:
        columns = inspector.get_columns(table_name)
        fields = []

        for col in columns:
            column_type = str(col['type'])  # Obtemos o tipo como string para processar
            length = None

            # Extraindo o tamanho do tipo, se aplicável
            if "VARCHAR" in column_type.upper() or "CHAR" in column_type.upper():
                # Busca o número entre parênteses (exemplo: VARCHAR(20))
                match = re.search(r'\((\d+)\)', column_type)
                if match:
                    length = int(match.group(1))

            # Adiciona as características do campo ao dicionário
            fields.append({
                "name": col["name"],
                "type": column_type,
                "length": length,
                "nullable": col["nullable"],
                "default": col.get("default"),
                "comment": col.get("comment")
            })

        return fields

    except Exception as e:
        raise ValueError(f"Erro ao obter as colunas da tabela '{table_name}': {str(e)}")

@generate_code_bp.route('/', methods=['POST'])
def generate_source_code():

    if request.method == 'POST':
        data = request.json
        table_name = data.get('table_name')
        selected_fields = data.get('selected_fields')
        displayNames = data.get('displayNames')
        formName = data.get('formName')

        if not table_name or not selected_fields:
            return jsonify({"error": "Tabela ou campos não foram selecionados."}), 400

        # Gerar códigos baseados na tabela e campos selecionados
        html_code, py_code, menu_insert, app_route, dbo_class = generate_form_code(table_name, selected_fields, displayNames, formName)

        # Gravar o arquivo html 
        html_path = os.path.join(temp_dir, f"form_{table_name}.html")
        with open(html_path, 'w', encoding='utf-8') as html_file:
            html_file.write(html_code)

        # Gravar o arquivo python
        python_path = os.path.join(temp_dir, f"api_{table_name}.py")
        with open(python_path, 'w', encoding='utf-8') as python_file:
            python_file.write(py_code)

        return jsonify({
            "success": True,
            "html_code": html_code,
            "py_code": py_code,
            "menu_insert": menu_insert,
            "app_route": app_route,
            "dbo_class": dbo_class
        })

    # Para GET, renderize o formulário inicial
    tables = get_database_tables()
    return render_template('form_generate_code.html', portal_name="Code Generator", tables=tables)

@generate_code_bp.route('/fields/<table_name>', methods=['GET'])
def get_table_fields(table_name):
    inspector = inspect(engine) 

    try:
        # Obter as colunas da tabela
        columns = inspector.get_columns(table_name)
        fields = [
            {
                "name": col["name"],
                "type": str(col["type"])
            }
            for col in columns
        ]
        return jsonify(fields=fields)
    except Exception as e:
        return jsonify(success=False, error=str(e)), 500


# Certifique-se de que todas as funções e loops terminem corretamente
def generate_form_code(table_name, fields, displayNames, formName):
    html_code = generate_html_code(table_name, fields, displayNames, formName)
    py_code = generate_python_code(table_name, fields)
    menu_insert = generate_menu_insert(table_name)
    app_route = generate_app_route(table_name, formName)
    dbo_class = generate_dbo_table(table_name)
    return html_code, py_code, menu_insert, app_route, dbo_class

def generate_html_code(table_name, fields, displayNames, formName):
    """
    Gera o código HTML de um formulário baseado na tabela e campos fornecidos.

    :param table_name: Nome da tabela.
    :param fields: Lista de campos da tabela.
    :param displayNames: Dicionário com os nomes de exibição dos campos.
    :param formName: Nome do formulário.
    :return: String com o HTML gerado.
    """
    quebraLinha = "\n"

    # Mapeamento de tipos SQL para tipos de input HTML
    def map_field_to_input_type(field_type):
        field_type = field_type.lower()
        if "int" in field_type:
            return "number"
        elif "float" in field_type or "double" in field_type or "decimal" in field_type:
            return "number"
        elif "date" in field_type and "time" not in field_type:
            return "date"
        elif "datetime" in field_type or "timestamp" in field_type:
            return "datetime-local"
        elif "bool" in field_type or "bit" in field_type:
            return "checkbox"
        else:
            return "text"  # Tipo padrão

    # Obter características dos campos do banco
    field_characteristics = {field['name']: field for field in get_table_columns(table_name)}
    
    fields_html = "\n".join(
        f"""
                <div class="mb-3">
                    <label for="{field}" class="form-label">{displayNames.get(field, field)}</label>
                    <input type="{map_field_to_input_type(field_characteristics[field]['type'])}" 
                        class="form-control" id="{field}" name="{field}">
                </div>
        """
        for field in fields
    )
    header_table = "\n".join(
        f"""        <th>{displayNames[field]}</th>"""
        for field in fields
    )
    detail_table = "\n".join(
        f"""        <td>{{{{ linha.{field} }}}}</td>"""
        for field in fields
    )

    return f"""
{{% extends "base.html" %}}

{{% block content %}}
<div class="container mt-4">
    <h2 class="mb-4">{formName}</h2>

    <!-- Toolbar -->
    <div class="d-flex mb-3">
        <button id="addConfigBtn" class="btn btn-primary me-2">
            <i class="bi bi-plus-circle"></i> Incluir
        </button>
        <button id="editConfigBtn" class="btn btn-secondary me-2" disabled>
            <i class="bi bi-pencil"></i> Editar
        </button>
        <button id="deleteConfigBtn" class="btn btn-danger" disabled>
            <i class="bi bi-trash"></i> Excluir
        </button>
    </div>

    <!-- Tabela de Registros -->
    <table class="table table-striped">
        <thead>
            <tr>
                <th></th>
                {header_table}
            </tr>
        </thead>
        <tbody id="{table_name}Table">
            {{% for linha in data %}}
            <tr>
                <td>
                    <input type="radio" name="selectedRecord" value="{{{{ linha.id }}}}">
                </td>
                {detail_table}
            </tr>
            {{% endfor %}}
        </tbody>
    </table>
</div>

<!-- Modal para Incluir/Editar Registros -->
<div class="modal fade" id="recordModal" tabindex="-1" aria-labelledby="recordModalLabel" aria-hidden="true">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title" id="recordModalLabel">Incluir Registro</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <form id="{table_name}Form">
                <div class="modal-body">
                    {fields_html}
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
                    <button type="submit" class="btn btn-primary">Salvar</button>
                </div>
            </form>
        </div>
    </div>
</div>

<script>
    const addConfigBtn = document.getElementById('addConfigBtn');
    const editConfigBtn = document.getElementById('editConfigBtn');
    const deleteConfigBtn = document.getElementById('deleteConfigBtn');
    const recordTable = document.getElementById('{table_name}Table');
    let selectedRecordId = null;

    // Selecionar Registro
    recordTable.addEventListener('change', (e) => {{
        if (e.target.name === 'selectedRecord') {{
            selectedRecordId = e.target.value;
            editConfigBtn.disabled = false;
            deleteConfigBtn.disabled = false;
        }}
    }});

    // Incluir Registro
    addConfigBtn.addEventListener('click', () => {{
        document.getElementById('recordModalLabel').textContent = 'Incluir Registro';
        document.getElementById('{table_name}Form').reset();
        selectedRecordId = null; // Garantir que será uma criação
        const recordModal = new bootstrap.Modal(document.getElementById('recordModal'));
        recordModal.show();
    }});

    // Editar Registro
    editConfigBtn.addEventListener('click', () => {{
        if (!selectedRecordId) {{
            alert('Nenhum registro foi selecionado.');
            return;
        }}

        const row = document.querySelector(`input[name="selectedRecord"][value="${{selectedRecordId}}"]`).closest('tr');
        const cells = row.cells;

        // Preencher os campos do modal
        document.getElementById('recordModalLabel').textContent = 'Editar Registro';
        { ''.join([f'        document.getElementById("{field}").value = cells[{index + 1}].textContent.trim();{quebraLinha}' for index, field in enumerate(fields)]) }

        const recordModal = new bootstrap.Modal(document.getElementById('recordModal'));
        recordModal.show();
    }});

    // Excluir Registro
    deleteConfigBtn.addEventListener('click', () => {{
        if (!selectedRecordId) return;

        if (confirm('Deseja excluir o registro?')) {{
            fetch(`/{table_name}/${{selectedRecordId}}`, {{ method: 'DELETE' }})
                .then(response => response.json())
                .then(data => {{
                    if (data.success) {{
                        location.reload();
                    }} else {{
                        alert('Erro ao excluir o registro.');
                    }}
                }});
        }}
    }});

    // Submissão do Formulário
    document.getElementById('{table_name}Form').addEventListener('submit', (e) => {{
        e.preventDefault();

        const formData = new FormData(e.target);
        const data = Object.fromEntries(formData.entries());

        const url = selectedRecordId
            ? `/{table_name}/${{selectedRecordId}}`
            : `/{table_name}/`;

        fetch(url, {{
            method: selectedRecordId ? 'PUT' : 'POST',
            headers: {{ 'Content-Type': 'application/json' }},
            body: JSON.stringify(data)
        }})
            .then(response => response.json())
            .then(data => {{
                if (data.success) {{
                    location.reload();
                }} else {{
                    alert(`Erro: ${{data.error}}`);
                }}
            }})
            .catch(error => console.error('Erro:', error));
    }});
</script>

{{% endblock %}}
"""

def generate_python_code(table_name, fields):
    fields_definitions = "\n    ".join(
        f"{field} = db.Column(db.String(255))"
        for field in fields
    )
    fields_to_dict = "\n            ".join(
        f'"{field}": self.{field}'
        for field in fields
    )
    fields_assignment = "\n        ".join(
        f"record.{field} = data.get('{field}', record.{field})"
        for field in fields
    )
    fields_creation = ", ".join(
        f"{field}=data.get('{field}')"
        for field in fields
    )

    return f"""
from flask import Blueprint, request, jsonify, abort
from db import db, {table_name.capitalize()}

{table_name}_bp = Blueprint('{table_name}', __name__, url_prefix='/{table_name}')

@{table_name}_bp.route('/', methods=['GET'])
def list_{table_name}():
    try:
        records = {table_name.capitalize()}.query.all()
        return jsonify([record.to_dict() for record in records]), 200
    except Exception as e:
        return jsonify(success=False, error=str(e)), 500

@{table_name}_bp.route('/<int:record_id>', methods=['GET'])
def get_{table_name}(record_id):
    try:
        record = {table_name.capitalize()}.query.get(record_id)
        if not record:
            return jsonify(success=False, error="Record not found"), 404
        return jsonify(record.to_dict()), 200
    except Exception as e:
        return jsonify(success=False, error=str(e)), 500

@{table_name}_bp.route('/', methods=['POST'])
def create_{table_name}():
    try:
        data = request.json
        new_record = {table_name.capitalize()}(
            {fields_creation}
        )
        db.session.add(new_record)
        db.session.commit()
        return jsonify(success=True, id=new_record.id), 201
    except Exception as e:
        return jsonify(success=False, error=str(e)), 500

@{table_name}_bp.route('/<int:record_id>', methods=['PUT'])
def update_{table_name}(record_id):
    try:
        data = request.json
        record = {table_name.capitalize()}.query.get(record_id)
        if not record:
            return jsonify(success=False, error="Record not found"), 404

        {fields_assignment}

        db.session.commit()
        return jsonify(success=True), 200
    except Exception as e:
        return jsonify(success=False, error=str(e)), 500

@{table_name}_bp.route('/<int:record_id>', methods=['DELETE'])
def delete_{table_name}(record_id):
    try:
        record = {table_name.capitalize()}.query.get(record_id)
        if not record:
            return jsonify(success=False, error="Record not found"), 404
        db.session.delete(record)
        db.session.commit()
        return jsonify(success=True), 200
    except Exception as e:
        return jsonify(success=False, error=str(e)), 500
"""

def generate_menu_insert(table_name):
    return f"""
INSERT INTO menus (id, parent_id, title, url, order_num, is_active)
VALUES (NULL, NULL, '{table_name.capitalize()}', '/{table_name}/manage', 1, TRUE);
"""

def generate_app_route(table_name, formName):
    return f"""
# Import the generated blueprint
from api_{table_name} import {table_name}_bp

# Register the blueprint
app.register_blueprint({table_name}_bp)

@app.route('/{table_name}/manage', methods=['GET'])
@admin_required
def manage_{table_name}():
    \"\"\"Render the management page for {formName}.\"\"\"
    # Fetch all records for rendering in the table
    records = {table_name.capitalize()}.query.all()
    return render_template(
        'form_{table_name.lower()}.html',
        portal_name=config['portal']['name'],
        data=records
    )
"""

def generate_dbo_table(table_name):
    """
    Gera a definição da classe SQLAlchemy para o arquivo db.py com base na tabela do banco de dados.

    :param table_name: Nome da tabela.
    :return: Código Python da classe.
    """
    # Obter características dos campos da tabela
    field_characteristics = {field['name']: field for field in get_table_columns(table_name)}

    # Verifica se os campos foram encontrados
    if not field_characteristics:
        raise ValueError(f"A tabela '{table_name}' não foi encontrada ou não possui colunas.")

    # Função auxiliar para determinar o tipo de coluna SQLAlchemy
    def get_sqlalchemy_column_type(field):
        column_type = field.get('type', '').lower()
        length = field.get('length')  # Verifica se há um tamanho definido

        if 'int' in column_type:
            return 'db.Integer'
        elif 'varchar' in column_type or 'text' in column_type:
            if length:  # Se houver tamanho, inclui no tipo
                return f'db.String({length})'
            return 'db.String'
        elif 'float' in column_type or 'double' in column_type or 'decimal' in column_type:
            return 'db.Float'
        elif 'date' in column_type and 'time' not in column_type:
            return 'db.Date'
        elif 'datetime' in column_type or 'timestamp' in column_type:
            return 'db.DateTime'
        elif 'bool' in column_type or 'bit' in column_type:
            return 'db.Boolean'
        elif 'enum' in column_type:  # Para campos ENUM
            options = field.get('options', [])
            if options:
                options_repr = ', '.join([f"'{opt}'" for opt in options])
                return f"db.Enum({options_repr})"
            return 'db.Enum'
        else:
            return 'db.String'  # Tipo padrão

    # Determinar se algum campo é chave primária (por inspeção manual)
    primary_key_fields = [
        field
        for field, attributes in field_characteristics.items()
        if not attributes.get('nullable', True) and attributes['name'] == 'id'
    ]
    has_primary_key = len(primary_key_fields) > 0

    # Gera a definição dos campos com base nas características
    fields_definitions = "\n    ".join(
        f"{field} = db.Column({get_sqlalchemy_column_type(field_characteristics[field])}"
        f"{', primary_key=True' if field in primary_key_fields else ''})"
        for field in field_characteristics
    )

    # Adiciona uma chave primária padrão se nenhuma estiver definida
    primary_key_definition = ""
    if not has_primary_key:
        primary_key_definition = "id = db.Column(db.Integer, primary_key=True, autoincrement=True)"

    # Cria a classe com SQLAlchemy
    class_code = f"""
class {table_name.capitalize()}(db.Model):
    __tablename__ = '{table_name}'

    {primary_key_definition}
    {fields_definitions}

    def __repr__(self):
        return f"<{table_name.capitalize()} id={{self.id}}>"  # Representação legível

    def to_dict(self):
        return {{
            {', '.join(f"'{field}': self.{field}" for field in field_characteristics)}
        }}
"""
    return class_code
