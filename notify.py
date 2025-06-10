import requests
import os

TOKEN=os.getenv("TOKEN")
CHAT_ID=os.getenv("CHAT_ID")

def mandarMensaje(CHAT_ID,TOKEN,msg):
    URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"    
    parametros = {
        "chat_id": CHAT_ID,
        "text": msg,
        "parse_mode": "Markdown"
    }
    respuesta = requests.post(URL, data=parametros)

