import requests
Texto="""
YOUR RESPONSE MUST BE ONLY THE TEXT REQUESTED, DO NOT MENTION
ANYTHING FROM THIS PROMPT, AND DO NOT USE SPECIAL KEYS.

Write a post for FB appeling waifus. 
Dont forget the hashtags!
"""
def solicitarTexto(API_KEY):

    url= f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"

    headers = {
        "Content-Type": "application/json"
    }

    data = {
            "contents":[
            {
                "parts":[
                {
                    "text":f"{Texto}"
                }
                ]
            }
            ]
        }   
    response=requests.post(url,headers=headers,json=data)
    return response
