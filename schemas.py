from pydantic import BaseModel
from typing import Optional

# ==========================================
# ESQUEMAS PARA USUÁRIOS
# ==========================================
class UsuarioCriar(BaseModel):
    cpf_ou_matricula: str
    nome: str
    email_contato: str
    perfil: str 
    suplente_de_id: Optional[int] = None 

class UsuarioResposta(BaseModel):
    id: int
    cpf_ou_matricula: str
    nome: str
    email_contato: str
    perfil: str
    suplente_de_id: Optional[int] = None

    class Config:
        from_attributes = True

# ==========================================
# ESQUEMAS PARA REUNIÕES
# ==========================================
class ReuniaoCriar(BaseModel):
    titulo: str
    data_hora: str 

class ReuniaoResposta(BaseModel):
    id: int
    titulo: str
    data_hora: str
    status: str

    class Config:
        from_attributes = True

# ==========================================
# ESQUEMAS PARA PRESENÇAS
# ==========================================
class PresencaCriar(BaseModel):
    reuniao_id: int
    usuario_id: int
    hora_entrada: str

class PresencaResposta(BaseModel):
    id: int
    reuniao_id: int
    usuario_id: int
    hora_entrada: str

    class Config:
        from_attributes = True

# ==========================================
# ESQUEMAS PARA PAUTAS
# ==========================================
class PautaCriar(BaseModel):
    reuniao_id: int
    descricao: str
    tipo_voto: str = "Aberto"

class PautaResposta(BaseModel):
    id: int
    reuniao_id: int
    descricao: str
    tipo_voto: str
    status: str

    class Config:
        from_attributes = True

# ==========================================
# ESQUEMAS PARA VOTOS
# ==========================================
class VotoCriar(BaseModel):
    pauta_id: int
    usuario_id: int
    escolha: str

class VotoResposta(BaseModel):
    id: int
    pauta_id: int
    usuario_id: int
    escolha: str

    class Config:
        from_attributes = True