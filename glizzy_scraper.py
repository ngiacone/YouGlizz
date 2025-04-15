import requests
import json

subs = ["hotdogs", "fastfood", "foodporn", "streetfood", "grilling"]
headers = {"User-Agent": "Mozilla/5.0 YouGlizz/1.0"}
videos = []

for sub in subs:
    url = f"https://www.reddit.com/r/{sub}/top.json?limit=20&t=week"
    res = requests.get(url, headers=headers)

    if res.status_code != 200:
        print(f"Error fetching /r/{sub}")
        continue

    posts = res.json().get("data", {}).get("children", [])
    for post in posts:
        data = post["data"]
        media = data.get("secure_media")
        if data.get("is_video") and media and media.get("reddit_video"):
            video_url = media["reddit_video"]["fallback_url"]
            if video_url.endswith(".mp4"):
                videos.append({
                    "id": video_url,
                    "category": sub.capitalize()
                })

# ONLY overwrite the file if we found valid videos
if videos:
    with open("videos.json", "w") as f:
        json.dump(videos[:20], f, indent=2)
    print(f"✅ Wrote {len(videos)} Reddit videos to videos.json")
else:
    print("⚠️ No Reddit videos found — videos.json not updated.")

