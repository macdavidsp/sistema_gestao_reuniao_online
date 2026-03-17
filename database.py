from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Cria um arquivo chamado 'reunioes.db' na sua pasta para guardar os dados
SQLALCHEMY_DATABASE_URL = "sqlite:///./reunioes.db"

# Estabelece a conexão (o connect_args é necessário para o SQLite no FastAPI)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Cria uma "Sessão" para podermos adicionar e ler dados depois
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para criarmos as nossas tabelas
Base = declarative_base()