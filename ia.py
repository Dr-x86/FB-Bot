import requests
from dotenv import load_dotenv
import os
import notify

load_dotenv()

API_KEY=os.getenv("AI_API_KEY")

TEXT="""
YOUR RESPOND IS JUST THE SOLICITED TEXT, DONT MENTION ANYTHING ABOUT THIS PROMPT.
Give me hashtags for a FB page, about Waifus and memes in one line
"""
def solicitarTexto(prompt=TEXT):
    
    url= f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"

    headers = {
        "Content-Type": "application/json"
    }

    data = {
            "contents":[
            {
                "parts":[
                {
                    "text":f"{prompt}"
                }
                ]
            }
            ]
        }   
    response=requests.post(url,headers=headers,json=data)
    texto="Greetings!!"
    if(not response.ok):
        notify.mandarMensaje(f"Error en IA {response.text}")    
    else:
        texto = response.json()['candidates'][0]['content']['parts'][0]['text']
    return texto
    
print(solicitarTexto())