import requests
import notify
import random

# print(">>> SCRIPT INICIADO")

def books():
    url =  'https://api.senpy.club/v2/random'
    try:
        response = requests.get(url)
        imagen = response.json()['image']
        book = response.json()['language']
        return imagen, book
    except Exception as e:
        print(f"ERROR API BOOKS: {e}")
        # notify.Me(f"ERROR API BOOKS :{e}")
    return None,None

def obtener_waifu(respaldo=False):
    url = "https://api.waifu.pics/sfw/waifu"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data["url"]
    except Exception as e:
        print(f"Error con API 1 {url}: {e}")
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
        print(f"Error con API Waifu 2 {url}: {e}")
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
        print(f"Error en la API NSFW {url}: {e}")
        return "None"
        
################################################ LADO DE LOS MOMOS ######################################

sources = ["ImaginaryGaming","hatsune","kasaneteto","frieren","AnimeART"]

def meme_api():
    subreddit=random.choice(sources)
    
    print("Subreddit")
    url = f"https://meme-api.com/gimme/{subreddit}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        data = response.json()
        title = data.get('title')
        meme_url = data.get('url')
        
        if(not url):
            return None, None
        
        return meme_url,title
        
    except requests.exceptions.RequestException as req_err:
        print(f"Error de red o HTTP: {req_err}")
    except ValueError:
        print("Error al decodificar JSON.")
    except Exception as e:
        print(f"Error inesperado: {e}")
    
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
    subreddit=random.choice(sources)
    url = f"https://www.reddit.com/r/{subreddit}/new/.json?limit=100"
    headers = {"User-agent": "Mozilla/5.0"}
    try:
        res = requests.get(url, headers=headers)
        posts = res.json()["data"]["children"]    
        
        urls = [p['data'] for p in posts if es_imagen(p['data'])]
        if(not urls):
            print(" >> No se encontraron momos hoy ... ")
            return None, None
            
        choice = random.choice(urls)
        imagen_url = choice['url']
        title = choice['title']
        
        return imagen_url, title
    
    except requests.exceptions.RequestException as req_err:
        # notify.Me(f"MOMOS RESPALDO Error de red o HTTP: {req_err}")
        print(f"MOMOS RESPALDO Error de red o HTTP: {req_err}")
    except ValueError:
        # notify.Me(f"MOMOS RESPALDO Error al decodificar JSON.")
        print(f"MOMOS RESPALDO Error al decodificar JSON.")
    except Exception as e:
        # notify.Me(f"MOMOS RESPALDO Error inesperado: {e}")
        print(f"MOMOS RESPALDO Error inesperado: {e}")
        