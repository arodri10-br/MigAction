from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from cryptography.fernet import Fernet

Base = declarative_base()

# Geração da chave de criptografia (deve ser armazenada de forma segura)
key = b'GY55m6boCz8OcPZIFW2QXWreTsvhn36g8AbPBGJDBYQ=' # Fernet.generate_key()
cipher_suite = Fernet(key)
# print(f"Key = <{key}>")

class DatabaseConfig(Base):
    __tablename__ = 'database_config'

    id = Column(Integer, primary_key=True)
    environment = Column(String(20), nullable=False)
    db_type = Column(String(20), nullable=False)
    host = Column(String(100), nullable=False)
    port = Column(Integer, nullable=False)
    database = Column(String(100), nullable=False)
    username = Column(String(50), nullable=False)
    password_encrypted = Column(String(256), nullable=False)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_encrypted = cipher_suite.encrypt(password.encode()).decode()

    def get_password(self):
        return cipher_suite.decrypt(self.password_encrypted.encode()).decode()

# Configuração do banco de dados SQLite para armazenar as configurações
DATABASE_URL = "sqlite:///database/sys.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)