import requests
import json

hotdog_subreddits = [
    "hotdogs", "fastfood", "foodporn", "streetfood", "grilling"
]

videos = []

for sub in hotdog_subreddits:
    url = f"https://www.reddit.com/r/{sub}/top.json?t=week&limit=15"
    headers = {"User-agent": "YouGlizzBot/0.1"}
    res = requests.get(url, headers=headers)
    if res.status_code != 200:
        continue

    posts = res.json()["data"]["children"]
    for post in posts:
        data = post["data"]
        if data.get("is_video") and "reddit_video" in data.get("secure_media", {}):
            reddit_video_url = data["secure_media"]["reddit_video"]["fallback_url"]
            videos.append({
                "id": reddit_video_url,
                "category": sub.capitalize()
            })

# Save to videos.json
with open("videos.json", "w") as f:
    json.dump(videos[:20], f, indent=2)
