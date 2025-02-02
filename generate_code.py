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
        fieldsPK = data.get('primary_keys')
        fieldsAI = data.get('autoincrement_fields')

        if not table_name or not selected_fields:
            return jsonify({"error": "Tabela ou campos não foram selecionados."}), 400

        # Gerar códigos baseados na tabela e campos selecionados
        html_code, py_code, menu_insert, app_route, dbo_class = generate_form_code(table_name, selected_fields, displayNames, formName, fieldsPK, fieldsAI)

        # Gravar o arquivo html 
        html_path = os.path.join(temp_dir, f"form_{table_name}.html")
        with open(html_path, 'w', encoding='utf-8') as html_file:
            html_file.write(html_code)

        # Gravar o arquivo python
        python_path = os.path.join(temp_dir, f"api_{table_name}.temp")
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
                "type": str(col["type"]),
                "primary_key": col["primary_key"],  
                "autoincrement": col.get("autoincrement", False)  
            }
            for col in columns
        ]
        return jsonify(fields=fields)
    except Exception as e:
        return jsonify(success=False, error=str(e)), 500

# Certifique-se de que todas as funções e loops terminem corretamente
def generate_form_code(table_name, fields, displayNames, formName, fieldsPK, fieldsAI):
    html_code = generate_html_code(table_name, fields, displayNames, formName, fieldsPK)
    py_code = generate_python_code(table_name, fields, fieldsPK, fieldsAI)
    menu_insert = generate_menu_insert(table_name)
    app_route = generate_app_route(table_name, formName)
    dbo_class = generate_dbo_table(table_name)
    return html_code, py_code, menu_insert, app_route, dbo_class

def generate_html_code(table_name, fields, displayNames, formName, fieldsPK):
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
    
    #fields_html = "\n".join(
    #    f"""
    #        <div class="form-group">
    #            <label for="{field}">{displayNames.get(field, field)}:</label>
    #            <input type="{map_field_to_input_type(field_characteristics[field]['type'])}" id="{field}" name="{field}" >
    #        </div>
    #    """
    #    for field in fields
    #)

    fields_html = []

    for field in fields:
        if field not in fieldsPK:
            fields_html.append(f"""
            <div class="form-group">
                <label for="{field}">{displayNames.get(field, field)}:</label>
                <input type="{map_field_to_input_type(field_characteristics[field]['type'])}" id="{field}" name="{field}" >
            </div>""")
        else:
            fields_html.append(f"""
            <div class="form-group" id="{field}Container">
                <label for="{field}">{displayNames.get(field, field)}:</label>
                <input type="{map_field_to_input_type(field_characteristics[field]['type'])}" id="{field}" name="{field}" readonly>
            </div>""") 

    fields_html = "\n".join(fields_html)
    #header_table = "\n".join(f"""        <th>{displayNames[field]}</th>""" for field in fields )
    detail_table = "\n".join(f"""                <th>{field}</th>""" for field in fields )
    return f"""
{{% extends "base.html" %}}

{{% block content %}}
<div class="page-header">
    <h1 class="mb-4">{formName}</h1>
</div>
<div class="toolbar">
    <button onclick="showAddModal()" class="primary">
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line></svg>
        Novo
    </button>
    <button onclick="editSelected()" class="primary">
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 3a2.828 2.828 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5L17 3z"></path></svg>
        Editar
    </button>
    <button onclick="deleteSelected()" class="secondary">
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path></svg>
        Excluir
    </button>
</div>

<div class="grid-container">
    <table class="grid">
        <thead>
            <tr>
                <th class="radio-cell"></th>
{detail_table}
            </tr>
        </thead>
        <tbody id="{table_name}Table">
            <!-- Preenchido dinamicamente -->
        </tbody>
    </table>
</div>

<!-- Modal de Formulário -->
<div id="formModal" class="modal">
    <div class="modal-content">
        <h2 id="modalTitle">Novo "{table_name}"</h2>
        <form id="{table_name}Form">
            {fields_html}
            <div class="modal-actions">
                <button type="button" class="secondary" onclick="hideModal()">Cancelar</button>
                <button type="submit" class="primary">Salvar</button>
            </div>
            <div id="errorMessage" class="error-message" style="display: none; color: red; margin-top: 10px;"></div>
        </form>
    </div>
</div>

<script>

    function getSelected{table_name}() {{
        const selected = document.querySelector('input[name="selectedUser"]:checked');
        if (!selected) {{
            return null;
        }}
        // Divide a string pelo separador para obter todos valores da chave primária
        const keyParts = selected.value.split('|');
        return {{
{','.join([f'{quebraLinha}            {field}: keyParts[{i}]' for i, field in enumerate(fieldsPK)])}
        }};

    }}

    document.addEventListener('DOMContentLoaded', function() {{
        load{table_name}();
    }});
    function load{table_name}() {{
        fetch('/api/{table_name}/')
            .then(response => response.json())
            .then(data => {{
                const {table_name}Table = document.getElementById('{table_name}Table');
                {table_name}Table.innerHTML = '';
                data.forEach(user => {{
                    const row = {table_name}Table.insertRow();
                    const radioCell = row.insertCell();
                    radioCell.className = 'radio-cell';
                    radioCell.innerHTML = `<input type="radio" name="selectedUser" value="{ "|".join([f"${{user.{field}}}" for field in fieldsPK]) }">`;

{ ''.join([f'                    row.insertCell().innerText = user.{field};{quebraLinha}' for index, field in enumerate(fields)]) }
                }});
            }})
        .catch(error => console.error('Erro ao carregar {table_name}:', error));
    }}
    

    function showAddModal() {{
        document.getElementById('modalTitle').textContent = 'Novo {table_name}';
        document.getElementById('{table_name}Form').reset();
        document.getElementById('formModal').classList.add('active');
{''.join([f"        document.getElementById('{field}').value = '';{quebraLinha}" for field in fieldsPK])}
{''.join([f"        document.getElementById('{field}').readOnly = false;{quebraLinha}" for field in fieldsPK])}

        // Esconder mensagem de erro ao abrir modal
        document.getElementById('errorMessage').style.display = 'none';
        document.getElementById('errorMessage').innerHTML = '';
    }}
    
    function hideModal() {{
        document.getElementById('formModal').classList.remove('active');
        //  Esconder e limpar a mensagem de erro ao fechar o modal
        let errorDiv = document.getElementById('errorMessage');
        errorDiv.style.display = 'none';
        errorDiv.innerHTML = '';
    }}

    function editSelected() {{
        const key = getSelected{table_name}();
        if (!key) {{
            alert('Por favor, selecione uma linha para editar.');
            return;
        }}
        const url = `/api/{table_name}/{"/".join([f"${{key.{field}}}" for field in fieldsPK])}`;
        fetch(url)
            .then(response => response.json())
            .then({table_name} => {{
                document.getElementById('modalTitle').textContent = 'Editar {formName}';
{ ''.join([f'                document.getElementById("{field}").value = {table_name}.{field};{quebraLinha}' for index, field in enumerate(fields)]) }
{ ''.join([f'                document.getElementById("{field}Container").style.display = "block";{quebraLinha}' for field in fieldsPK])}

                document.getElementById('formModal').classList.add('active');
            }})

            .catch(error => {{
                showError('Erro ao carregar {table_name} para edição.');
                console.error('Erro ao carregar {table_name}:', error);
            }});
        }}

    function deleteSelected() {{
        const {table_name} = getSelected{table_name}();
        if (!{table_name}) {{
            alert('Por favor, selecione um {table_name} para excluir.');
            return;
        }}

        if (confirm('Tem certeza que deseja excluir este {table_name}?')) {{
            fetch(`/api/{table_name}/${{{table_name}}}`, {{
                method: 'DELETE'
            }}).then(() => {{
                load{table_name}();
            }});
        }}
    }}
       
    document.getElementById('{table_name}Form').addEventListener('submit', function(event) {{
        event.preventDefault();
        const {table_name} = document.getElementById('{fieldsPK[0]}').value.trim();
        const isEdit = document.getElementById('{fieldsPK[0]}').readOnly === true;
        const method = isEdit ? 'PUT' : 'POST';
        let url = '/api/{table_name}/';
        if (isEdit) {{
{''.join([f"            const {field} = document.getElementById('{field}').value.trim();{quebraLinha}" for field in fieldsPK])}
            url = `/api/{table_name}/{"/".join([f"${{encodeURIComponent({field})}}" for field in fieldsPK])}`;
        }}            
        const formData = new FormData(this);
        const data = Object.fromEntries(formData.entries());

        fetch(url, {{
            method: method,
            headers: {{
                'Content-Type': 'application/json'
            }},
        body: JSON.stringify(data)
    }})
    .then(response => {{
        if (!response.ok) {{
            return response.json().then(err => {{ throw new Error(err.error || 'Erro desconhecido'); }});
        }}
        return response.json();
    }})
    .then(() => {{
        hideModal();
        load{table_name}();
    }})
    .catch(error => {{
        showError(error.message);
    }});
}});

function showError(message) {{
    let errorDiv = document.getElementById('errorMessage');
    errorDiv.style.display = 'block'; 
    errorDiv.innerHTML = `<strong>Erro:</strong> ${{message}}`;
}}
          
</script>

{{% endblock %}}
"""

def generate_python_code(table_name, fields, fieldsPK, fieldsAI):
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

    # fields_create = ", ".join(f"{field}=data['{field}']" for field in fields)
    fields_create_list = []  # Lista para armazenar os campos formatados

    for field in fields:
        if field not in fieldsAI:  # Os campos que sao do tipo autoincremento nao sao inseridos
            if field == "dtAtualizacao":
                fields_create_list.append(f"            {field}=datetime.now(timezone.utc)")
            elif field == "username":
                fields_create_list.append(f"            {field}=request.headers.get('username', 'admin')")  
            else:
                fields_create_list.append(f"            {field}=data['{field}']") 
    fields_create = ", \n".join(fields_create_list)  

    fields_update = "\n        ".join(f"{table_name}.{field}=data.get('{field}', {table_name}.{field})" for field in fields)

    fields_route = "/".join([f"<string:{field}>" for field in fieldsPK])
    fields_list_pk = ",".join(fieldsPK)


    return f"""
from flask import Blueprint, request, jsonify
from sysdb import SessionLocal, {table_name.capitalize()}
from datetime import datetime, timezone

bp_{table_name} = Blueprint('{table_name}_api', __name__, url_prefix='/api/{table_name}')

# Criar {table_name}
@bp_{table_name}.route('/', methods=['POST'])
def create_{table_name}():
    try:
        data = request.json
        session = SessionLocal()
        if session.query({table_name.capitalize()}).filter_by({ ''.join([f'{field} = data["{field}"],' for field in fieldsPK])}).first():
            session.close()
            return jsonify({{"error": "{fields[0]} já existe."}}), 400
        
        {table_name} = {table_name.capitalize()}(
{fields_create},
            username=request.headers.get('username', 'admin'),
            dtAtualizacao=datetime.now(timezone.utc)
        )
        
        session.add({table_name})
        session.commit()
        session.close()
        return jsonify(success=True), 200
    except Exception as e:
        return jsonify(success=False, error=str(e)), 500

# Obter {table_name}
@bp_{table_name}.route('/', methods=['GET'])
def get_{table_name}_list():
    session = SessionLocal()
    {table_name}s = session.query({table_name.capitalize()}).all()
    session.close()
    return jsonify([{table_name}.to_dict() for {table_name} in {table_name}s])

# Obter um registro específico da tabela {table_name}
@bp_{table_name}.route('/{fields_route}' , methods=['GET'])
def get_{table_name}({fields_list_pk}):
    session = SessionLocal()
    {table_name} = session.query({table_name.capitalize()}).filter_by({ ','.join([f'{field} = {field}' for field in fieldsPK])}).first():
    session.close()
    if {table_name}:
        return jsonify({table_name}.to_dict())
    return jsonify({{"error": "Registro não encontrado."}}), 404

# Atualizar um registro da tabela {table_name}
@bp_{table_name}.route('/{fields_route}', methods=['PUT'])
def update_{table_name}({fields_list_pk}):
    try:
        session = SessionLocal()
        {table_name} = session.query({table_name.capitalize()}).filter_by({ ','.join([f'{field} = {field}' for field in fieldsPK])}).first():
        if not {table_name}:
            session.close()
            return jsonify({{"error": "Registro não encontrado."}}), 404
        
        data = request.json
        {fields_update}
        
        session.commit()
        session.close()
        return jsonify(success=True), 200
    except Exception as e:
        return jsonify(success=False, error=str(e)), 500

# Excluir um Registro da tabela {table_name}
@bp_{table_name}.route('/<string:{fields[0]}>', methods=['DELETE'])
def delete_{table_name}({fields[0]}):
    session = SessionLocal()
    {table_name} = session.query({table_name.capitalize()}).filter_by({fields[0]}={fields[0]}).first()
    if not {table_name}:
        session.close()
        return jsonify({{"error": "Registro não encontrado."}}), 404
    
    session.delete({table_name})
    session.commit()
    session.close()
    return jsonify({{"message": "Registro deletado com sucesso."}})
"""

def generate_menu_insert(table_name):
    return f"""
        {{"name": "{table_name.capitalize()}", "url": "/{table_name}"}},
"""

def generate_app_route(table_name, formName):
    return f"""
@bp_routes.route('/{table_name}')
def call_{table_name.capitalize()}():
    return render_template('form_{table_name}.html', menu_items=menu_items)

"""

def generate_dbo_table(table_name):
    class_code = f"""
from api_{table_name} import bp_{table_name}

app.register_blueprint(bp_{table_name})
"""
    return class_code
