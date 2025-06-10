import requests
import os

TOKEN=os.setenv("TOKEN")
CHAT_ID=os.setenv("CHAT_ID")


def mandarMensaje(msg):
    URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"    
    parametros = {
        "chat_id": CHAT_ID,
        "text": msg,
        "parse_mode": "Markdown"
    }
    respuesta = requests.post(URL, data=parametros)

