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
                    "source": "reddit",
                    "category": sub.capitalize()
                })

# Load existing YouTube videos (if available)
try:
    with open("videos.json", "r") as f:
        existing = json.load(f)
except FileNotFoundError:
    existing = []

# Append original YouTube list (only YouTube entries)
youtube_videos = [v for v in existing if v.get("source") == "youtube"]

# Combine with new Reddit videos
combined = videos[:30] + youtube_videos[:30]

# Deduplicate by video ID
seen = set()
unique = []
for vid in combined:
    if vid["id"] not in seen:
        unique.append(vid)
        seen.add(vid["id"])

# Save final list (max 50)
with open("videos.json", "w") as f:
    json.dump(unique[:50], f, indent=2)

print(f"✅ Wrote {len(unique[:50])} total videos (Reddit + YouTube) to videos.json")


