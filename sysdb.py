from sqlalchemy import create_engine, Column, String, Integer, Date, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from cryptography.fernet import Fernet

Base = declarative_base()

# Geração da chave de criptografia (deve ser armazenada de forma segura)
key = b'GY55m6boCz8OcPZIFW2QXWreTsvhn36g8AbPBGJDBYQ='  # Fernet.generate_key()
cipher_suite = Fernet(key)

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
        self.passw_encrypted = cipher_suite.encrypt(password.encode()).decode()

    def get_password(self):
        return cipher_suite.decrypt(self.passw_encrypted.encode()).decode()

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
    DescSupData = Column(String(15), nullable=False)
    Chave1 = Column(String(15), nullable=False)
    Chave2 = Column(String(15), nullable=False)
    Campo1 = Column(String(15), nullable=False)
    Campo2 = Column(String(15), nullable=False) 
    Campo3 = Column(String(15), nullable=False)
    Campo4 = Column(String(15), nullable=False)
    Campo5 = Column(String(15), nullable=False)
    Campo6 = Column(String(15), nullable=False)
    Campo7 = Column(String(15), nullable=False)
    Campo8 = Column(String(15), nullable=False)
    Campo9 = Column(String(15), nullable=False)
    Campo10 = Column(String(15), nullable=False)
    username = Column(String(10), ForeignKey('usuario.username'), nullable=False)
    dtAtualizacao = Column(Date)

    def to_dict(self):
        return {
            "codSupData": self.codSupData,
            "DescSupData": self.DescSupData,
            "Chave1": self.Chave1,
            "Chave2": self.Chave2,
            "Campo1": self.Chave1,
            "Campo2": self.Chave2,
            "Campo3": self.Chave3,
            "Campo4": self.Chave4,
            "Campo5": self.Chave5,
            "Campo6": self.Chave6,
            "Campo7": self.Chave7,
            "Campo8": self.Chave8,
            "Campo9": self.Chave9,
            "Campo10": self.Chave10,
            "username": self.username,
            "dtAtualizacao": self.dtAtualizacao.isoformat() if self.dtAtualizacao else None,
        }

class SuppDataDet(Base):
    __tablename__ = 'suppdatadet'

    IdProjeto = Column(Integer, ForeignKey('projeto.idProjeto'), primary_key=True)
    codSupData = Column(String(10), ForeignKey('suppdataconfig.codSupData'), primary_key=True)
    Chave1 = Column(String(20), nullable=False)
    Chave2 = Column(String(20))
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

class Processos(Base):
    __tablename__ = 'processos'

    idProjeto = Column(Integer, ForeignKey('projeto.idProjeto'), primary_key=True)
    seq = Column(Integer, primary_key=True)  # Removido autoincrement=True
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
    passw = Column(String(255))
    username = Column(String(10), ForeignKey('usuario.username'))
    dtAtualizacao = Column(Date)

    @property
    def passw(self):
        raise AttributeError('A senha não pode ser acessada diretamente.')

    @passw.setter
    def passw(self, password):
        self.passw_encrypted = cipher_suite.encrypt(password.encode()).decode()

    def get_password(self):
        return cipher_suite.decrypt(self.passw_encrypted.encode()).decode()

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

    idProjeto = Column(Integer, ForeignKey('processos.idProjeto'))
    seq = Column(Integer, ForeignKey('processos.seq'))
    uniqueKeyId = Column(Integer, primary_key=True, autoincrement=True)
    idDSOrigem = Column(Integer, ForeignKey('datasource.idDataSource'))
    idDSDestino = Column(Integer, ForeignKey('datasource.idDataSource'))
    operacao = Column(String(50))
    status = Column(String(20), nullable=False)
    dbOper = Column(String(50), nullable=False)
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
            passw_encrypted=cipher_suite.encrypt('admin'.encode()).decode()
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
