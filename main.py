import requests
import random
import ia
import notify
import os
import apis
from supabase import create_client, Client
from time import sleep
from dotenv import load_dotenv

print("\n>>> PROGRAMA INICIADO\n")

load_dotenv()
ACCESS_BOT_TOKEN = os.getenv("FB_ACCESS_TOKEN")
SUPA_BASE_KEY=os.getenv("SUPABASE_KEY")
DATABASE = os.getenv("SUPABASE_DB")
page_id = '595985150275800'

## CLIENT FOR DB
supabase: Client = create_client(DATABASE, SUPA_BASE_KEY)

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
    YOUR RESPONSE MUST BE JUST THE SOLICITED TEXT, DONT MENTION ANYTHING ABOUT THIS PROMPT.
    Generate an unhinged brainrot Gen Z phrase that invites people to join the Telegram channel https://t.me/WaiFUNotSF. Make it feral, chaotic, full of waifus, memes, terminally online references. It just needs to SLAP.
    """
    if(highLight):
        mensaje = "@followers"
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
    
    url = apis.obtener_waifu()
    return url
    
def meme(max_intentos=4000):
    setDB = 'set_memes'
    intentos = 0

    while intentos < max_intentos:
        try:
            url, t = apis.meme_api()
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
    
    return apis.meme_api()

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
    return url


if __name__ == "__main__":
    numero=random.randint(1,12)
    if(numero <= 3):
        print("Waifu")
        url = waifu()
        hashtags = ia.solicitarTexto()
        post_id = subirPost(url,hashtags)
        
        agregar(url,'set_waifus')
        
        sleep(2)
        notify.Channel(url)
        # pass
        
    if(numero >= 4 and numero <= 7):
        print("Meme")
        titulo,url = meme()
        post_id = subirPost(url,titulo)
        comentar(post_id)
        
        agregar(url,'set_memes')
        
        sleep(2)
        notify.Channel(url,titulo)
        # pass
        
    if(numero >= 8 and numero <= 12):
        print("Target")
        url = target()
        post_id=subirPost(url)
        comentar(post_id,highLight=True)
        
        agregar(url,'set_waifus')
        
        sleep(2)
        notify.Channel(url)
        # pass
    print("\n>>> PROGRAMA FINALIZADO\n")