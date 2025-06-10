import requests
import os
import random
import animemes
import sfw
import ia
import notify

access_token=os.getenv("FB_ACCESS_TOKEN")

def subirPost(urlPhoto,caption):
    page_id = '595985150275800'
    url = f'https://graph.facebook.com/{page_id}/photos'
    
    data = {
        'caption': caption,
        'access_token': access_token,
        'url':f'{urlPhoto}'
    }
    response = requests.post(url, data=data)
    return response

def verify(url):
    with open("setUrls.txt") as f:
        urlSet = f.read()
        if (url in urlSet):
            print(f"Esta url {url} ya estaba")
            return True
    return False
    
def obtenerUrlWaifu():
    url = sfw.obtener_waifu()
    while(verify(url)):
        print("Ya estaba, buscando una url nueva")
        url = sfw.obtener_waifu()
    return url

def obtenerUrlMeme():
    url,t = animemes.obtener_meme()
    while(verify(url)):
        print("Ya estaba, buscando una url nueva\n\n")
        url,t = animemes.obtener_meme()
    return (url,t)

def agregar(url):
    try:
        with open("setUrls.txt",'a') as f:
            f.write(url+'\n')
    except Exception as e:
        print(f"Error detalles: {e}")

if __name__ == "__main__":
    post=random.randint(1,500)
    
    if(post <= -5): # Toca Waifu
        print("Toca Waifu")
        url = obtenerUrlWaifu()
        if(url == '0'):
            notify.mandarMensaje("Error API de imagenes")
            url=""
        response = ia.solicitarTexto()
        if(not response.ok):
            notify.mandarMensaje(f"Error Detalles fayo la IA {response.text}")
        texto=response.json()['candidates'][0]['content']['parts'][0]['text']
        
        
        print(f"URL: {url} \nTexto:{texto}")
        #respuestaFB=subirPost(url,texto)
        #notify.mandarMensaje(f"Post: {respuestaFB}")
        agregar(url)
        
    else:  #Toca Meme
        print("toca meme")
        url,titulo=obtenerUrlMeme()
        print(f"URL: {url} \nTexto:{titulo}")
        
        #respuestaFB=subirPost(url,titulo)
        #notify.mandarMensaje(f"Post: {respuestaFB}")
        agregar(url)