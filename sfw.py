import requests

def obtener_waifu():
    response = requests.get("https://api.waifu.pics/sfw/waifu")
    if response.status_code == 200:
        data = response.json()
        return data["url"]
    return "None"

def solicitar_waifu():
    url = 'https://api.waifu.im/search'
    params = {
        'included_tags': ['oppai','waifu']
    }
    response = requests.get(url, params=params)
    url='None'
    if response.status_code==200:
        url = response.json()['images'][0]['url']
    return url