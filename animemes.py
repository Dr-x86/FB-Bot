import requests
import subprocess
from time import sleep

def obtener_meme(subreddit="KasaneTeto"):
    url = f'https://meme-api.com/gimme/{subreddit}'
    respuesta = requests.get(url)
    if respuesta.status_code == 200:
        meme = respuesta.json()
        return (meme['url'],meme['title'])
    return ("0","0")


url, title = obtener_meme()
subprocess.run(["start","brave",f"{url}"],shell=True)