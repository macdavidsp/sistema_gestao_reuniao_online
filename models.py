from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    cpf_ou_matricula = Column(String, unique=True, index=True)
    nome = Column(String)
    email_contato = Column(String)
    perfil = Column(String) # "Administrador", "Titular" ou "Suplente"
    
    # Se for suplente, guarda o ID do Titular aqui.
    suplente_de_id = Column(Integer, ForeignKey("usuarios.id"), nullable=True)

class Reuniao(Base):
    __tablename__ = "reunioes"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String)
    data_hora = Column(String) # Ex: "25/10/2023 14:00"
    status = Column(String, default="Agendada") # Agendada, Em Andamento, Finalizada

class Presenca(Base):
    __tablename__ = "presencas"

    id = Column(Integer, primary_key=True, index=True)
    reuniao_id = Column(Integer, ForeignKey("reunioes.id"))
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    hora_entrada = Column(String) # Ex: "14:05" (Vamos usar texto por enquanto para facilitar)

class Pauta(Base):
    __tablename__ = "pautas"

    id = Column(Integer, primary_key=True, index=True)
    reuniao_id = Column(Integer, ForeignKey("reunioes.id"))
    descricao = Column(String)
    tipo_voto = Column(String, default="Aberto") # "Aberto" ou "Secreto"
    status = Column(String, default="Aguardando") # "Aguardando", "Em Votação", "Concluída"

class Voto(Base):
    __tablename__ = "votos"

    id = Column(Integer, primary_key=True, index=True)
    pauta_id = Column(Integer, ForeignKey("pautas.id"))
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    escolha = Column(String) # "Favorável", "Contrário" ou "Abstenção"