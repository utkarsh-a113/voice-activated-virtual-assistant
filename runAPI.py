import requests

newsapi = "7a7970bc3fc44fa2a6cac20e54d7d0ae"
url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}"

response = requests.get(url)
if response.status_code == 200:
    data = response.json()
    articles = data.get("articles", [])
    print("Top 5 Headlines:")
    for article in articles[:5]:
        print("-", article["title"])
else:
    print("Error:", response.status_code, response.text)
