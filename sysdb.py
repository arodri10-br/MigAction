from sqlalchemy import create_engine, Column, String, Integer, Date, ForeignKey, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import date
from sqlalchemy import create_engine, Column, String, Integer, Date, ForeignKey, Text, Boolean
from crypto_utils import encrypt_password, decrypt_password
Base = declarative_base()

class Usuario(Base):
    __tablename__ = 'usuario'

    username = Column(String(10), primary_key=True)
    nome = Column(String(30), nullable=False)
    email = Column(String(50), nullable=False, unique=True)
    perfil = Column(String(10), nullable=False)
    status = Column(String(1), nullable=False)
    dtAtualizacao = Column(Date)
    passw_encrypted = Column(String(255), nullable=False)

    @property
    def passw(self):
        raise AttributeError('A senha não pode ser acessada diretamente.')

    @passw.setter
    def passw(self, password):
        self.passw_encrypted = encrypt_password(password)

    def get_password(self):
        return decrypt_password(self.passw_encrypted)

    def to_dict(self):
        return {
            "username": self.username,
            "nome": self.nome,
            "email": self.email,
            "perfil": self.perfil,
            "status": self.status,
            "dtAtualizacao": self.dtAtualizacao.isoformat() if self.dtAtualizacao else None,
        }

class Projeto(Base):
    __tablename__ = 'projeto'

    idProjeto = Column(Integer, primary_key=True, autoincrement=True)
    codProjeto = Column(String(20), unique=True)
    descProjeto = Column(String(50), nullable=False)
    status = Column(String(1), nullable=False)
    username = Column(String(10), ForeignKey('usuario.username'), nullable=False)
    dtAtualizacao = Column(Date)

    def to_dict(self):
        return {
            "idProjeto": self.idProjeto,
            "codProjeto": self.codProjeto,
            "descProjeto": self.descProjeto,
            "status": self.status,
            "username": self.username,
            "dtAtualizacao": self.dtAtualizacao.isoformat() if self.dtAtualizacao else None,
        }

class SuppDataConfig(Base):
    __tablename__ = 'suppdataconfig'

    codSupData = Column(String(10), primary_key=True, unique=True)
    DescSupData = Column(String(30), nullable=False)
    Chave1 = Column(String(15), nullable=False)
    Chave2 = Column(String(15), nullable=True)
    Campo1 = Column(String(15), nullable=True)
    Campo2 = Column(String(15), nullable=True) 
    Campo3 = Column(String(15), nullable=True)
    Campo4 = Column(String(15), nullable=True)
    Campo5 = Column(String(15), nullable=True)
    Campo6 = Column(String(15), nullable=True)
    Campo7 = Column(String(15), nullable=True)
    Campo8 = Column(String(15), nullable=True)
    Campo9 = Column(String(15), nullable=True)
    Campo10 = Column(String(15), nullable=True)
    Tipo1 = Column(String(2), nullable=True)
    Tipo2 = Column(String(2), nullable=True)
    Tipo3 = Column(String(2), nullable=True)
    Tipo4 = Column(String(2), nullable=True)
    Tipo5 = Column(String(2), nullable=True)
    Tipo6 = Column(String(2), nullable=True)
    Tipo7 = Column(String(2), nullable=True)
    Tipo8 = Column(String(2), nullable=True)
    Tipo9 = Column(String(2), nullable=True)
    Tipo10 = Column(String(2), nullable=True)
    PermNull1 = Column(Boolean, default=True, nullable=True)
    PermNull2 = Column(Boolean, default=True, nullable=True)
    PermNull3 = Column(Boolean, default=True, nullable=True)
    PermNull4 = Column(Boolean, default=True, nullable=True)
    PermNull5 = Column(Boolean, default=True, nullable=True)
    PermNull6 = Column(Boolean, default=True, nullable=True)
    PermNull7 = Column(Boolean, default=True, nullable=True)
    PermNull8 = Column(Boolean, default=True, nullable=True)
    PermNull9 = Column(Boolean, default=True, nullable=True)
    PermNull10 = Column(Boolean, default=True, nullable=True)
    username = Column(String(10), ForeignKey('usuario.username'), nullable=False)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dtAtualizacao = date.today()
    dtAtualizacao = Column(Date)
    def to_dict(self):
        return {
            "codSupData": self.codSupData,
            "DescSupData": self.DescSupData,
            "Chave1": self.Chave1,
            "Chave2": self.Chave2,
            "Campo1": self.Campo1,
            "Campo2": self.Campo2,
            "Campo3": self.Campo3,
            "Campo4": self.Campo4,
            "Campo5": self.Campo5,
            "Campo6": self.Campo6,
            "Campo7": self.Campo7,
            "Campo8": self.Campo8,
            "Campo9": self.Campo9,
            "Campo10": self.Campo10,
            "Tipo1": self.Tipo1,
            "Tipo2": self.Tipo2,
            "Tipo3": self.Tipo3,
            "Tipo4": self.Tipo4,
            "Tipo5": self.Tipo5,
            "Tipo6": self.Tipo6,
            "Tipo7": self.Tipo7,
            "Tipo8": self.Tipo8,
            "Tipo9": self.Tipo9,
            "Tipo10": self.Tipo10,
            "PermNull1": self.PermNull1,
            "PermNull2": self.PermNull2,
            "PermNull3": self.PermNull3,
            "PermNull4": self.PermNull4,
            "PermNull5": self.PermNull5,
            "PermNull6": self.PermNull6,
            "PermNull7": self.PermNull7,
            "PermNull8": self.PermNull8,
            "PermNull9": self.PermNull9,
            "PermNull10": self.PermNull10,
            "username": self.username,
            "dtAtualizacao": self.dtAtualizacao.isoformat() if self.dtAtualizacao else None,
        }

class SuppDataDet(Base):
    __tablename__ = 'suppdatadet'

    IdProjeto = Column(Integer, ForeignKey('projeto.idProjeto'), primary_key=True)
    codSupData = Column(String(10), ForeignKey('suppdataconfig.codSupData'), primary_key=True)
    Chave1 = Column(String(20), nullable=False, primary_key=True)
    Chave2 = Column(String(20), nullable=False, primary_key=True)
    Valor1 = Column(String(20))
    Valor2 = Column(String(20))
    Valor3 = Column(String(20))
    Valor4 = Column(String(20))
    Valor5 = Column(String(20))
    Valor6 = Column(String(20))
    Valor7 = Column(String(20))
    Valor8 = Column(String(20))
    Valor9 = Column(String(20))
    Valor10 = Column(String(20))
    username = Column(String(10), ForeignKey('usuario.username'))
    dtAtualizacao = Column(Date)

    def to_dict(self):
        return {
            "IdProjeto": self.IdProjeto,
            "codSupData": self.codSupData,
            "Chave1": self.Chave1,
            "Chave2": self.Chave2,
            "Valor1": self.Valor1,
            "Valor2": self.Valor2,
            "Valor3": self.Valor3,
            "Valor4": self.Valor4,
            "Valor5": self.Valor5,
            "Valor6": self.Valor6,
            "Valor7": self.Valor7,
            "Valor8": self.Valor8,
            "Valor9": self.Valor9,
            "Valor10": self.Valor10,
            "username": self.username,
            "dtAtualizacao": self.dtAtualizacao.isoformat() if self.dtAtualizacao else None,
        }

class Script(Base):
    __tablename__ = 'script'

    idProjeto = Column(Integer, ForeignKey('projeto.idProjeto'), primary_key=True)
    ordem = Column(Integer, primary_key=True)
    seq = Column(Integer, primary_key=True) 
    Tabela = Column(String(30), nullable=False)
    Modulo = Column(String(15))
    descProcesso = Column(String(150))
    responsavel = Column(String(30))
    programa = Column(String(30))
    selDados = Column(Text)
    cmdInsert = Column(Text)
    username = Column(String(10), ForeignKey('usuario.username'))
    dtAtualizacao = Column(Date, nullable=False)

    def to_dict(self):
        return {
            "idProjeto": self.idProjeto,
            "seq": self.seq,
            "ordem": self.ordem,
            "Tabela": self.Tabela,
            "Modulo": self.Modulo,
            "descProcesso": self.descProcesso,
            "responsavel": self.responsavel,
            "programa": self.programa,
            "selDados": self.selDados,
            "cmdInsert": self.cmdInsert,
            "username": self.username,
            "dtAtualizacao": self.dtAtualizacao.isoformat() if self.dtAtualizacao else None,
        }
    
class DataSource(Base):
    __tablename__ = 'datasource'

    idDataSource = Column(Integer, primary_key=True, autoincrement=True)
    dsDataSource = Column(String(30), nullable=False)
    TpBanco = Column(String(10))
    nmBanco = Column(String(30))
    server = Column(String(50))
    user = Column(String(20))
    passw_encrypted = Column(String(255), nullable=True)
    username = Column(String(10), ForeignKey('usuario.username'))
    dtAtualizacao = Column(Date)

    @property
    def passw(self):
        raise AttributeError('A senha não pode ser acessada diretamente.')

    @passw.setter
    def passw(self, password):
        self.passw_encrypted = encrypt_password(password)

    def get_password(self):
        """Retorna a senha descriptografada ou uma string vazia se for None"""
        if not self.passw_encrypted:  # Se for None, retorna string vazia
            return ""

        return decrypt_password(self.passw_encrypted)
    
    @property
    def connection_string(self):
        # Usa o método get_password para obter a senha descriptografada
        senha = self.get_password() or ""
        if self.TpBanco == "Oracle":
            return f"oracle+cx_oracle://{self.user}:{senha}@{self.server}/{self.nmBanco}"
        elif self.TpBanco == "SQLITE3":
            return f"sqlite:///{self.nmBanco}"
        return "Tipo de banco desconhecido"

    def to_dict(self):
        return {
            "idDataSource": self.idDataSource,
            "dsDataSource": self.dsDataSource,
            "TpBanco": self.TpBanco,
            "nmBanco": self.nmBanco,
            "server": self.server,
            "user": self.user,
            "username": self.username,
            "dtAtualizacao": self.dtAtualizacao.isoformat() if self.dtAtualizacao else None,
        }

class Carga(Base):
    __tablename__ = 'carga'

    uniqueKeyId = Column(Integer, primary_key=True, autoincrement=True)
    idProjeto = Column(Integer, ForeignKey('script.idProjeto'))
    ordem = Column(Integer, ForeignKey('script.ordem'))
    seq = Column(Integer, ForeignKey('script.seq'))
    idDSOrigem = Column(Integer, ForeignKey('datasource.idDataSource'))
    idDSDestino = Column(Integer, ForeignKey('datasource.idDataSource'))
    operacao = Column(String(50))
    status = Column(String(20), nullable=False)
    dbOper = Column(String(10), nullable=False)
    dtCriacao = Column(Date)
    dtExec = Column(Date)
    dtAtualizacao = Column(Date)
    username = Column(String(10), ForeignKey('usuario.username'), nullable=False)

    def to_dict(self):
        return {
            "idProjeto": self.idProjeto,
            "seq": self.seq,
            "uniqueKeyId": self.uniqueKeyId,
            "idDSOrigem": self.idDSOrigem,
            "idDSDestino": self.idDSDestino,
            "operacao": self.operacao,
            "status": self.status,
            "dbOper": self.dbOper,
            "dtCriacao": self.dtCriacao.isoformat() if self.dtCriacao else None,
            "dtExec": self.dtExec.isoformat() if self.dtExec else None,
            "dtAtualizacao": self.dtAtualizacao.isoformat() if self.dtAtualizacao else None,
            "username": self.username,
        }

class Processo(Base):
    __tablename__ = 'processo'

    idProjeto = Column(Integer, ForeignKey('projeto.idProjeto'), primary_key=True)
    ordem = Column(Integer, primary_key=True)
    dsProcesso = Column(String, nullable=False)
    statusProcesso = Column(String, nullable=False)
    dataExecucao = Column(Date)
    username = Column(String(10), ForeignKey('usuario.username'))
    dtAtualizacao = Column(Date)

    def to_dict(self):
        return {
            "idProjeto": self.idProjeto,
            "ordem": self.ordem,
            "dsProcesso": self.dsProcesso,
            "statusProcesso": self.statusProcesso,
            "dataExecucao": self.dataExecucao.isoformat() if self.dataExecucao else None,
            "username": self.username,
            "dtAtualizacao": self.dtAtualizacao.isoformat() if self.dtAtualizacao else None,
        }

# Função para verificar e criar o usuário admin
def create_admin_user(session):
    admin_user = session.query(Usuario).filter_by(username='admin').first()
    if not admin_user:
        admin_user = Usuario(
            username='admin',
            nome='Administrador',
            email='admin@actionsys.com.br',
            perfil='admin',
            status='A',
            passw_encrypted=encrypt_password('admin')
        )
        session.add(admin_user)
        session.commit()

DATABASE_URL = "sqlite:///database/sys.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    create_admin_user(session)
    session.close()

# Inicializa o banco de dados e cria o usuário admin se necessário
init_db()



