import requests
from bs4 import BeautifulSoup

# Google araması yap
query = "kocaeli"
url = f"https://www.google.com/search?q={query}"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
page = requests.get(url, headers=headers)
soup = BeautifulSoup(page.content, "html.parser")
results = soup.find_all("div", class_="g")[:10]

# Sonuçları listele
for idx, result in enumerate(results, start=1):
    link = result.find("a")["href"]
    title = result.find("a").find("h3").get_text() if result.find("a").find("h3") else result.find("a").get_text()
    print(f"{idx} - {title} - ({link})")
