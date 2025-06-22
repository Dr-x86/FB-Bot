import requests
import random
import ia
import notify
import os
import apis
from supabase import create_client, Client
from time import sleep
from dotenv import load_dotenv

load_dotenv()
ACCESS_BOT_TOKEN = os.getenv("FB_ACCESS_TOKEN")
SUPA_BASE_KEY=os.getenv("SUPABASE_KEY")
DATABASE = os.getenv("SUPABASE_DB")
page_id = '595985150275800'

## INITIALIZE CLIENT FOR DB
Client = create_client(DATABASE, SUPA_BASE_KEY)

def subirPost(urlPhoto,caption=""):
    url = f'https://graph.facebook.com/{page_id}/photos'
    
    data = {
        'caption': caption,
        'access_token': ACCESS_BOT_TOKEN,
        'url':urlPhoto
    }
    response = requests.post(url, data=data)
    
    if response.status_code == 200:
        notify.Me(f"El bot subio el post https://facebook.com/{page_id}/posts/{response.json()['id']}")
        return response.json()['id']
    else:
        notify.Me(f"Error al subir post {response.json()}")
    return None


def comentar(post_id,highLight=False):
    customPrompt="""
    YOUR RESPOND IS JUST THE SOLICITED TEXT, DONT MENTION ANYTHING ABOUT THIS PROMPT.
    Gimme a brainrot gen z phrase, dont care if it has sense or not, memes or waifus that's the topic.
    """
    if(highLight):
        mensaje = "@highlight"
    else:
        mensaje = ia.solicitarTexto(customPrompt)
    
    url = f'https://graph.facebook.com/{post_id}/comments'

    params = {
        'message': mensaje,
        'access_token': ACCESS_BOT_TOKEN
    }
    
    response = requests.post(url, data=params)
    if(response.status_code!=200):
        notify.Me(f"Error al comentar: {response.json()}")
        
def agregar(url,setUrl):
    insert_response = supabase.table(f'{setUrl}').insert({'url': url}).execute()
    return True if insert_response.data else False

def verify(url,setUrl):
    response = supabase.table(f'{setUrl}').select('id').eq('url', url).execute()
    return True if response.data else False

def waifu(max_intentos=4000):
    setDB = 'set_waifus'
    intentos = 0

    while intentos < max_intentos:
        url = apis.obtener_waifu()
        
        if not url or not isinstance(url, str):
            notify.Me(f"URL inválida obtenida: {url}, intento {intentos}")
            intentos += 1
            continue

        try:
            if not verify(url, setDB):
                return url
        except Exception as e:
            notify.Me(f"Error al verificar URL en BD: {url}, error: {e}")

        intentos += 1
        
    notify.Me("⚠️ Posiblemente se han terminado las imágenes de la API Waifu. Reposteando una repetida...")
    # Intentar al menos retornar algo, aunque sea repetido
    url = apis.obtener_waifu()
    return url if url else "None"
    
def meme(max_intentos=4000):
    setDB = 'set_memes'
    intentos = 0

    while intentos < max_intentos:
        try:
            url, t = apis.obtener_meme()
        except Exception as e:
            notify.Me(f"Error al obtener meme: {e}")
            intentos += 1
            continue

        if not url or not isinstance(url, str):
            notify.Me(f"Meme inválido en intento {intentos}: {url}")
            intentos += 1
            continue

        try:
            if not verify(url, setDB):
                return (url, t)
        except Exception as e:
            notify.Me(f"Error al verificar meme en BD: {e}")

        intentos += 1

    notify.Me("⚠️ Se agotaron los memes nuevos. Reposteando uno repetido...")
    try:
        return apis.obtener_meme()
    except:
        return ("None", "None")

def target(max_intentos=4000):
    setDB = 'set_waifus'
    intentos = 0

    while intentos < max_intentos:
        try:
            url = apis.solicitar_waifu()
        except Exception as e:
            notify.Me(f"Error solicitando waifu específica: {e}")
            intentos += 1
            continue

        if not url or not isinstance(url, str):
            notify.Me(f"URL inválida en intento {intentos}: {url}")
            intentos += 1
            continue

        try:
            if not verify(url, setDB):
                return url
        except Exception as e:
            notify.Me(f"Error al verificar URL waifu 2: {e}")

        intentos += 1

    notify.Me("⚠️ Se agotaron las waifus nuevas (API 2). Reposteando una repetida...")
    
    url = apis.solicitar_waifu()
    return url if url else "None"


if __name__ == "__main__":
    numero=random.randint(1,10)
    
    if(numero <= 3):
        url = waifu()
        post_id=subirPost(url)
        comentar(post_id)
        
    if(numero >=4 and numero <= 6):
        pass
        
    if(numero >= 7 and numero <= 10):
        pass
    
    sleep(5)
    notify.Channel()