from dotenv import load_dotenv
import os

# Carrega as variáveis do arquivo ".env"
load_dotenv()

# Acesse as variáveis
def GetUsuarioInstagram():
    USUARIO_INSTAGRAM = os.getenv("USUARIO_INSTAGRAM")
    return USUARIO_INSTAGRAM

def GetSenhaInstagram():
    SENHA_INSTAGRAM = os.getenv("SENHA_INSTAGRAM")
    return SENHA_INSTAGRAM

def GetApiKey():
    CHAVE_API = os.getenv("CHAVE_API")
    return CHAVE_API
