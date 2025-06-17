import requests
import random
import animemes
import ia
import notify
import os
import sfw
from dotenv import load_dotenv
from supabase import create_client, Client
from time import sleep
import group

load_dotenv()
ACCESS_BOT_TOKEN = os.getenv("FB_ACCESS_TOKEN")
SUPA_BASE_KEY=os.getenv("SUPABASE_KEY")
DATABASE = os.getenv("SUPABASE_DB")
page_id = '595985150275800'

## INITIALIZE CLIENT FOR DB
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
        notify.mandarMensaje(f"El bot subio el post https://facebook.com/{page_id}/posts/{response.json()['id']}")
        return response.json()['id']
    else:
        notify.mandarMensaje(f"Error al subir post {response.json()}")
    return None


def comentar(post_id,highLight=False):
    if(highLight):
        mensaje = "@highlight @followers"
    else:
        mensaje = "Join us at Telegram for more NSFW Waifus content, give us a feedback!! " + "https://t.me/+G7bxJxH8Ul8zNGMx"
    
    url = f'https://graph.facebook.com/{post_id}/comments'

    params = {
        'message': mensaje,
        'access_token': ACCESS_BOT_TOKEN
    }
    
    response = requests.post(url, data=params)
    if(response.status_code!=200):
        notify.mandarMensaje(f"Error al comentar: {response.json()}")


def agregar(url,setUrl):
    insert_response = supabase.table(f'{setUrl}').insert({'url': url}).execute()
    return True if insert_response.data else False

def verify(url,setUrl):
    response = supabase.table(f'{setUrl}').select('id').eq('url', url).execute()
    return True if response.data else False

def obtenerUrlWaifu(max_intentos=4000):
    setDB='set_waifus'
    intentos = 0
    
    while intentos < max_intentos:
        url = sfw.obtener_waifu()
        if not verify(url,setDB):
            return url
        intentos+=1
    
    ### EL EXPLOTADOR MUAJAJAJA
    notify.mandarMensaje("Posiblemente se han terminado las imagenes de la API Waifu, reposteando ...")    
    url = sfw.obtener_waifu()
    return url
    
def obtenerUrlMeme(max_intentos=4000):
    setDB = 'set_memes'
    intentos = 0
    while intentos < max_intentos:
        url, t = animemes.obtener_meme()
        if not verify(url, setDB):
            return (url, t)        
        intentos += 1
    
    # No hay memes nuevos disponibles toca repostear lol
    notify.mandarMensaje("Posiblemente se han terminado las imagenes de la API Momazos, reposteando ...")
    url, t = animemes.obtener_meme()
    return (url, t)

#Specific set of urls for followers
def target(max_intentos=4000):
    setDB='set_waifus'
    intentos = 0
    
    while intentos < max_intentos:
        url = sfw.solicitar_waifu()
        if not verify(url,setDB):
            return url
        intentos+=1
    ### EL EXPLOTADOR MUAJAJAJA
    notify.mandarMensaje("Posiblemente se han terminado las imagenes de la API Waifu 2, reposteando ...")    
    url = sfw.solicitar_waifu()
    return url

if __name__ == "__main__":
    post=random.randint(1,10)
    
    if(post <= 3): # Toca Waifu
        print("Waifus selected")
        url = obtenerUrlWaifu()
        texto=ia.solicitarTexto()
        post_id=subirPost(url,texto)
        
        if(post_id!=None):
            comentar(post_id)
        
        agregar(url,'set_waifus')
            
    if(post >=4 and post <= 6):
        print("Memes selected")
        url,titulo=obtenerUrlMeme()
        # Just in case no Title at the moment
        post_id=subirPost(url)
        if(post_id!=None):
            comentar(post_id)
        
        agregar(url,'set_memes')
    
    if(post >= 7 and post <= 10):
        print("Target selected")
        url = target()
        post_id = subirPost(url)
        if(post_id!=None):
            comentar(post_id,highLight=True)
            
        agregar(url,'set_waifus')
        comentar(post_id)
    
    sleep(7)
    group.notifyGroup()