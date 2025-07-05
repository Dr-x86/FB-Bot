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
    return response


def comentar(post_id):
    customPrompt="""
    YOUR RESPONSE MUST BE JUST THE SOLICITED TEXT, DONT MENTION ANYTHING ABOUT THIS PROMPT.
    Generate a brainrot Gen Z phrase that invites people to follow the page. use Waifus, memes and terminally online references.
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
        url,book = apis.books()
        
        if not url or not isinstance(url, str):
            # notify.Me(f"URL inválida obtenida: {url}, intento {intentos}")
            print(f"URL inválida obtenida: {url}, intento {intentos}")
            intentos += 1
            continue

        try:
            if not verify(url, setDB):
                return url,book
        except Exception as e:
            # notify.Me(f"Error al verificar URL en BD: {url}, error: {e}")
            print(f"Error al verificar URL en BD: {url}, error: {e}")

        intentos += 1
        
    notify.Me("Posiblemente se han terminado las imágenes de la API Waifu. Reposteando una repetida...")
    print("Posiblemente se han terminado las imágenes de la API Waifu. Reposteando una repetida...")
    
    url,book = apis.books()
    return url,book
    
def meme(max_intentos=4000):
    setDB = 'set_memes'
    intentos = 0

    while intentos < max_intentos:
        
        url, title = apis.meme_api()

        if not url or not isinstance(url, str):
            # notify.Me(f"Meme inválido en intento {intentos}: {url}")
            print(f"Meme inválido en intento {intentos}: {url}")
            intentos += 1
            continue

        try:
            if not verify(url, setDB):
                return (url, title)
        except Exception as e:
            # notify.Me(f"Error al verificar meme en BD: {e}")
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
            # notify.Me(f"Error solicitando waifu específica: {e}")
            print(f"Error solicitando waifu específica: {e}")
            intentos += 1
            continue

        if not url or not isinstance(url, str):
            # notify.Me(f"URL inválida en intento {intentos}: {url}")
            print(f"URL inválida en intento {intentos}: {url}")
            intentos += 1
            continue

        try:
            if not verify(url, setDB):
                return url
        except Exception as e:
            # notify.Me(f"Error al verificar URL waifu 2: {e}")
            print(f"Error al verificar URL waifu 2: {e}")

        intentos += 1

    notify.Me("Se agotaron las waifus nuevas (API 2). Reposteando una repetida...")
    print("Se agotaron las waifus nuevas (API 2). Reposteando una repetida...")
    
    url = apis.solicitar_waifu()
    return url

if __name__ == "__main__":        
    
    print(" - Waifu")
    url, book = waifu()
    response = subirPost(url,"Programming Book: " + book)
    if(response.status_code==200):
        agregar(url,'set_waifus')
    else:
        notify.Me(f"ERROR - Waifu books - tipo: {response.json()} \nURL: {url}")
    
    # sleep(3)
    # print(" - Target")
    # url = target()
    # response = subirPost(url)
    # if(response.status_code == 200):
        # agregar(url,'set_waifus')
    # else:
        # notify.Me(f"ERROR - Target - tipo: {response.json()} \nURL: {url}")

    sleep(3)
    print(" - Meme")
    url,title = meme()
    if(title == None):
        title = ""
    response = subirPost(url,title)
    if(response.status_code==200):
        agregar(url,'set_memes')
    else:
        notify.Me(f"ERROR - Meme - tipo: {response.json()} \nURL:{url}")
    
    
    print("\n>>> PROGRAMA FINALIZADO\n")
