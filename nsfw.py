import requests

def obtenerNSFW():
    response = requests.get("https://api.waifu.pics/nsfw/waifu")
    if response.status_code == 200:
        data = response.json()
        return data["url"]
    return "0"