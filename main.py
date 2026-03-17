from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas
from database import engine, SessionLocal

# Cria as tabelas no banco de dados (se não existirem)
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Sistema de Reuniões")

# Função para abrir e fechar a conexão com o banco a cada requisição
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def ler_raiz():
    return {"mensagem": "Olá! O motor e o Banco de Dados estão funcionando!"}

# ==========================================
# ROTAS DE USUÁRIOS
# ==========================================
@app.post("/usuarios/", response_model=schemas.UsuarioResposta)
def criar_usuario(usuario: schemas.UsuarioCriar, db: Session = Depends(get_db)):
    db_usuario = db.query(models.Usuario).filter(models.Usuario.cpf_ou_matricula == usuario.cpf_ou_matricula).first()
    if db_usuario:
        raise HTTPException(status_code=400, detail="CPF ou Matrícula já cadastrado")
    
    novo_usuario = models.Usuario(**usuario.dict())
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    return novo_usuario

@app.get("/usuarios/", response_model=list[schemas.UsuarioResposta])
def listar_usuarios(db: Session = Depends(get_db)):
    usuarios = db.query(models.Usuario).all()
    return usuarios

# ==========================================
# ROTAS DE REUNIÕES
# ==========================================
@app.post("/reunioes/", response_model=schemas.ReuniaoResposta)
def criar_reuniao(reuniao: schemas.ReuniaoCriar, db: Session = Depends(get_db)):
    nova_reuniao = models.Reuniao(**reuniao.dict())
    db.add(nova_reuniao)
    db.commit()
    db.refresh(nova_reuniao)
    return nova_reuniao

@app.get("/reunioes/", response_model=list[schemas.ReuniaoResposta])
def listar_reunioes(db: Session = Depends(get_db)):
    reunioes = db.query(models.Reuniao).all()
    return reunioes

# ==========================================
# ROTAS DE PRESENÇAS (Relógio de Ponto)
# ==========================================
@app.post("/presencas/", response_model=schemas.PresencaResposta)
def registrar_presenca(presenca: schemas.PresencaCriar, db: Session = Depends(get_db)):
    presenca_existente = db.query(models.Presenca).filter(
        models.Presenca.reuniao_id == presenca.reuniao_id,
        models.Presenca.usuario_id == presenca.usuario_id
    ).first()
    
    if presenca_existente:
        raise HTTPException(status_code=400, detail="Usuário já está presente nesta reunião!")

    nova_presenca = models.Presenca(**presenca.dict())
    db.add(nova_presenca)
    db.commit()
    db.refresh(nova_presenca)
    return nova_presenca

@app.get("/presencas/{reuniao_id}", response_model=list[schemas.PresencaResposta])
def listar_presencas_da_reuniao(reuniao_id: int, db: Session = Depends(get_db)):
    presencas = db.query(models.Presenca).filter(models.Presenca.reuniao_id == reuniao_id).all()
    return presencas

# ==========================================
# ROTAS DE PAUTAS
# ==========================================
@app.post("/pautas/", response_model=schemas.PautaResposta)
def criar_pauta(pauta: schemas.PautaCriar, db: Session = Depends(get_db)):
    nova_pauta = models.Pauta(**pauta.dict())
    db.add(nova_pauta)
    db.commit()
    db.refresh(nova_pauta)
    return nova_pauta

@app.get("/pautas/{reuniao_id}", response_model=list[schemas.PautaResposta])
def listar_pautas_da_reuniao(reuniao_id: int, db: Session = Depends(get_db)):
    pautas = db.query(models.Pauta).filter(models.Pauta.reuniao_id == reuniao_id).all()
    return pautas

# ==========================================
# ROTAS DE VOTOS (A Urna com Regra de Negócio)
# ==========================================
@app.post("/votos/", response_model=schemas.VotoResposta)
def registrar_voto(voto: schemas.VotoCriar, db: Session = Depends(get_db)):
    # 1. Trava básica: impedir voto duplo
    voto_existente = db.query(models.Voto).filter(
        models.Voto.pauta_id == voto.pauta_id,
        models.Voto.usuario_id == voto.usuario_id
    ).first()
    if voto_existente:
        raise HTTPException(status_code=400, detail="Este usuário já votou nesta pauta!")

    # 2. Descobrir de qual reunião é essa pauta
    pauta = db.query(models.Pauta).filter(models.Pauta.id == voto.pauta_id).first()
    if not pauta:
        raise HTTPException(status_code=404, detail="Pauta não encontrada!")

    # 3. Buscar os dados de quem está tentando votar
    usuario = db.query(models.Usuario).filter(models.Usuario.id == voto.usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado!")

    # 4. A REGRA DE NEGÓCIO: Titular vs Suplente
    if usuario.perfil == "Suplente" and usuario.suplente_de_id:
        # Checar se o titular (suplente_de_id) bateu o ponto na mesma reunião da pauta
        titular_presente = db.query(models.Presenca).filter(
            models.Presenca.reuniao_id == pauta.reuniao_id,
            models.Presenca.usuario_id == usuario.suplente_de_id
        ).first()
        
        if titular_presente:
            raise HTTPException(
                status_code=403, 
                detail="Voto negado: O Titular está presente na reunião e tem a preferência do voto!"
            )

    # 5. Se passou por todas as travas, registra o voto!
    novo_voto = models.Voto(**voto.dict())
    db.add(novo_voto)
    db.commit()
    db.refresh(novo_voto)
    return novo_voto

@app.get("/votos/{pauta_id}", response_model=list[schemas.VotoResposta])
def listar_votos_da_pauta(pauta_id: int, db: Session = Depends(get_db)):
    votos = db.query(models.Voto).filter(models.Voto.pauta_id == pauta_id).all()
    return votos