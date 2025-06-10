import requests

def obtener_waifu():
    response = requests.get("https://api.waifu.pics/sfw/waifu")
    if response.status_code == 200:
        data = response.json()
        return data["url"]
    return "0"