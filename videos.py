import requests
import random
import subprocess

subreddit = "KasaneTeto"
url = f"https://www.reddit.com/r/{subreddit}/top/.json?t=week&limit=80"
headers = {"User-agent": "Mozilla/5.0"}

res = requests.get(url, headers=headers)
posts = res.json()["data"]["children"]

cont=0
for post in posts:
    if(post['data']['is_video']):
        cont+=1

print(f"Cantidad de datos: {cont}")
# Filtrar los que tienen video
videos = [p['data'] for p in posts if p['data']['is_video']]
random_video = random.choice(videos)
video_url = random_video['secure_media']['reddit_video']['fallback_url']
print("Título:", random_video["title"])
print("Video directo:", video_url)
subprocess.run(["start","brave",f"{video_url}"],shell=True)