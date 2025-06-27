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
        return response.json()['id']
    else:
        notify.Me(f"Error al subir post {response.json()}")
    return None


def comentar(post_id):
    customPrompt="""
    YOUR RESPONSE MUST BE JUST THE SOLICITED TEXT, DONT MENTION ANYTHING ABOUT THIS PROMPT.
    Generate an unhinged brainrot Gen Z phrase that invites people to follow the page. Make it feral, chaotic, full of waifus, memes, terminally online references. It just needs to SLAP and short.
    """
    mensaje = ia.solicitarTexto(customPrompt)
    
    url = f'https://graph.facebook.com/{post_id}/comments'

    params = {
        'message': mensaje,
        'access_token': ACCESS_BOT_TOKEN
    }
    
    response = requests.post(url, data=params)
    if(response.status_code!=200):
        notify.Me(f"Error al comentar: {response.json()}")
        print(f"Error al comentar: {response.json()}")
        
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
            # notify.Me(f"URL inválida obtenida: {url}, intento {intentos}")
            print(f"URL inválida obtenida: {url}, intento {intentos}")
            intentos += 1
            continue

        try:
            if not verify(url, setDB):
                return url
        except Exception as e:
            notify.Me(f"Error al verificar URL en BD: {url}, error: {e}")
            print(f"Error al verificar URL en BD: {url}, error: {e}")

        intentos += 1
        
    notify.Me("Posiblemente se han terminado las imágenes de la API Waifu. Reposteando una repetida...")
    print("Posiblemente se han terminado las imágenes de la API Waifu. Reposteando una repetida...")
    
    url = apis.obtener_waifu()
    return url
    
def meme(max_intentos=4000):
    setDB = 'set_memes'
    intentos = 0

    while intentos < max_intentos:
        
        url, title = apis.meme_api()

        if not url or not isinstance(url, str):
            notify.Me(f"Meme inválido en intento {intentos}: {url}")
            print(f"Meme inválido en intento {intentos}: {url}")
            intentos += 1
            continue

        try:
            if not verify(url, setDB):
                return (url, title)
        except Exception as e:
            notify.Me(f"Error al verificar meme en BD: {e}")
            print(f"Error al verificar meme en BD: {e}")

        intentos += 1

    notify.Me("Se agotaron los memes nuevos. Reposteando uno repetido...")
    print("Se agotaron los memes nuevos. Reposteando uno repetido...")
    
    u,t = apis.meme_respaldo()
    return u,t

def target(max_intentos=4000):
    setDB = 'set_waifus'
    intentos = 0

    while intentos < max_intentos:
        try:
            url = apis.solicitar_waifu()
        except Exception as e:
            notify.Me(f"Error solicitando waifu específica: {e}")
            print(f"Error solicitando waifu específica: {e}")
            intentos += 1
            continue

        if not url or not isinstance(url, str):
            notify.Me(f"URL inválida en intento {intentos}: {url}")
            print(f"URL inválida en intento {intentos}: {url}")
            intentos += 1
            continue

        try:
            if not verify(url, setDB):
                return url
        except Exception as e:
            notify.Me(f"Error al verificar URL waifu 2: {e}")
            print(f"Error al verificar URL waifu 2: {e}")

        intentos += 1

    notify.Me("Se agotaron las waifus nuevas (API 2). Reposteando una repetida...")
    print("Se agotaron las waifus nuevas (API 2). Reposteando una repetida...")
    
    url = apis.solicitar_waifu()
    return url


if __name__ == "__main__":
    numero=random.randint(1,4)
    if(numero == 1):
        print(" - Waifu")
        url = waifu()
        hashtags = ia.solicitarTexto()
        post_id = subirPost(url,hashtags)
        if(post_id == None):
            notify.Me("ADIVINA, NONE EN POST-ID :(")
            exit()        
        agregar(url,'set_waifus')
        
    if(numero == 2):
        print(" - Target")
        url = target()
        post_id = subirPost(url)
        if(post_id == None):
            notify.Me("ADIVINA, NONE EN POST-ID :(")
            exit()
        comentar(post_id)
        agregar(url,'set_waifus')
    
    if(numero >= 3):
        print(" - Meme")
        url,title= meme()
        print(f"\n TITULO: {title} URL: {url} \n")
        post_id = subirPost(url,titulo)
        if(post_id == None):
            notify.Me("ADIVINA, NONE EN POST-ID :(")
            exit()
        comentar(post_id)
        agregar(url,'set_memes')
        
    print("\n>>> PROGRAMA FINALIZADO\n")
