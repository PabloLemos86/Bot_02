import os

# Não versionar o token no Git
TOKEN = os.getenv("TELEGRAM_TOKEN")  # defina no Render

# Use os seus valores atuais:
REGIOES = {
    "Norte": ["AC", "AM", "AP", "PA", "RO", "RR", "TO"],
    "Nordeste": ["AL", "BA", "CE", "MA", "PB", "PE", "PI", "RN", "SE"],
    "Centro-Oeste": ["DF", "GO", "MT", "MS"],
    "Sudeste": ["ES", "MG", "RJ", "SP"],
    "Sul": ["PR", "RS", "SC"],
    "Nacional": []
}

DEFAULT_QTD = 10