import requests

def obtener_meme():
    url = 'https://meme-api.com/gimme/KasaneTeto'
    respuesta = requests.get(url)
    if respuesta.status_code == 200:
        meme = respuesta.json()
        return (meme['url'],meme['title'])
    return ("None","0")