from fastapi import FastAPI

# Cria a nossa aplicação
app = FastAPI(title="Sistema de Reuniões")

# Cria a nossa primeira rota (o nosso primeiro "link")
@app.get("/")
def ler_raiz():
    return {"mensagem": "Olá! O motor do sistema de reuniões está funcionando perfeitamente."}