import requests
from dotenv import load_dotenv
import os
import notify

load_dotenv()

API_KEY=os.getenv("AI_API_KEY")

TEXT="""
YOUR RESPONSE MUST BE ONLY THE TEXT REQUESTED, DO NOT MENTION
ANYTHING FROM THIS PROMPT,DO NOT USE SPECIAL KEYS AND DO NOT LET VARIABLE NAMES LIKE [WAIFU 1] or [YOUR NAME] DO NOT DO THAT.

Write a post for FB appeling waifus. 
Dont forget the hashtags!
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