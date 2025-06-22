import requests
import notify

def obtener_waifu(respaldo=False):
    url = "https://api.waifu.pics/sfw/waifu"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data["url"]
    except Exception as e:
        notify.Me(f"Error con API {url}: {e}")
        if not respaldo:
            return solicitar_waifu(respaldo=True)
        return "None"

def solicitar_waifu(respaldo=False):
    url = 'https://api.waifu.im/search'
    params = {'included_tags': ['oppai', 'waifu']}
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()['images'][0]['url']
    except Exception as e:
        notify.Me(f"Error con API {url}: {e}")
        if not respaldo:
            return obtener_waifu(respaldo=True)
        return "None"

def obtenerNSFW():
    url="https://api.waifu.pics/nsfw/waifu"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()["url"]
    except Exception as e:
        notify.Me(f"Error en la API {url}: {e}")
        return "None"
        
################################################ LADO DE LOS MOMOS ######################################

def obtener_meme(sub):
    url = f'https://meme-api.com/gimme/{sub}'
    try:
        respuesta = requests.get(url)
        respuesta.raise_for_status()
        meme = respuesta.json()
        return (meme['url'],meme['title'])
    except Exception as e:
        notify.Me(f"Error en la API {url}: {e}\nMomos :(")
        return ("None","None")
