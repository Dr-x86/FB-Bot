import requests
import notify
import random

# print(">>> SCRIPT INICIADO")

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

def meme_api():
    sources = ["bluearchive","ZenlessZoneZero","hatsunemiku","kasaneteto","frieren"]
    subreddit=random.choice(sources)
    
    url = f"https://meme-api.com/gimme/{subreddit}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        data = response.json()
        title = data.get('title')
        meme_url = data.get('url')
        
        if(not title or not url):
            return None, None
        
        return title, meme_url
        
    except requests.exceptions.RequestException as req_err:
        notify.Me(f"Error de red o HTTP: {req_err}")
    except ValueError:
        notify.Me("Error al decodificar JSON.")
    except Exception as e:
        notify.Me(f"Error inesperado: {e}")
    
    return None,None
    
def es_imagen(post_data):
    url = post_data.get("url", "")
    if not url:
        return False
    # Solo considerar imágenes directas alojadas en Reddit o fuentes confiables
    extensiones_validas = (".jpg", ".jpeg", ".png", ".gif")
    dominios_validos = ("i.redd.it", "i.imgur.com", "media.tenor.com")
    
    return url.lower().endswith(extensiones_validas) and any(d in url for d in dominios_validos)

def meme_respaldo():
    subs = ["bluearchive","ZenlessZoneZero","hatsunemiku","kasaneteto","frieren"]
    subreddit=random.choice(subs)
    
    url = f"https://www.reddit.com/r/{subreddit}/new/.json?limit=100"
    headers = {"User-agent": "Mozilla/5.0"}
    try:
        res = requests.get(url, headers=headers)
        posts = res.json()["data"]["children"]    
        
        urls = [p['data'] for p in posts if es_imagen(p['data'])]
        if(not urls):
            print("No se encontraron momos hoy ... ")
            return None, None
            
        imagen_url = random.choice(urls)
        title = imagen_url['title']
        
        print(f"\n MOMOS RESPALDO \n Url: {imagen_url['url']} Title: {title}")
        return title , imagen_url['url']
    
    except requests.exceptions.RequestException as req_err:
        notify.Me(f"MOMOS RESPALDO Error de red o HTTP: {req_err}")
    except ValueError:
        notify.Me(f"MOMOS RESPALDO Error al decodificar JSON.")
    except Exception as e:
        notify.Me(f"MOMOS RESPALDO Error inesperado: {e}")