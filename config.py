# config.py

# TOKEN do Bot - já embutido diretamente para rodar localmente
TOKEN = "7832475512:AAFeprDYq4ztM8rCjR0drF7YtFf9nscNXNw"

# Como está no PyDroid, não usamos webhook
USE_WEBHOOK = "0"

# Webhook URL não é usada no local
WEBHOOK_URL = None

# Quantidade padrão de licitações retornadas
DEFAULT_QTD = 5

# Regiões e estados
REGIOES = {
    "Norte": ["AC", "AP", "AM", "PA", "RO", "RR", "TO"],
    "Nordeste": ["AL", "BA", "CE", "MA", "PB", "PE", "PI", "RN", "SE"],
    "Centro-Oeste": ["DF", "GO", "MT", "MS"],
    "Sudeste": ["ES", "MG", "RJ", "SP"],
    "Sul": ["PR", "RS", "SC"],
    "Nacional": []
}