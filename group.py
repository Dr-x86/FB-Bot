import requests
import os
from dotenv import load_dotenv
from nsfw import obtenerNSFW
load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
GROUP_CHAT_ID = os.getenv('GROUP_CHAT_ID')

def notifyGroup():
    IMAGE_URL=obtenerNSFW()
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    payload = {
        "chat_id": GROUP_CHAT_ID,
        "photo": IMAGE_URL,
    }
    response = requests.post(url, data=payload)
    return response