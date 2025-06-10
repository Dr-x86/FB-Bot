import requests

def obtener_meme():
    url = 'https://meme-api.com/gimme/animememes'
    respuesta = requests.get(url)
    if respuesta.status_code == 200:
        meme = respuesta.json()
        return (meme['url'],meme['title'])
    return ("0","0")

def obtener_momo():
    url = 'https://meme-api.com/gimme/memes'
    respuesta = requests.get(url)
    if respuesta.status_code == 200:
        meme = respuesta.json()
        return (meme['url'],meme['title'])
    return ("0","0")