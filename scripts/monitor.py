
import json
import re
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

OUTPUT = Path("discovered.json")

QUERIES = {
    "Szczecin": [
        '"Restaurant Week" Szczecin site:instagram.com/p/',
        '"Restaurant Week" Szczecin site:instagram.com/reel/',
        '"restaurantweekszczecin" site:instagram.com',
    ],
    "Śląsk": [
        '"Restaurant Week" Katowice site:instagram.com/p/',
        '"Restaurant Week" Śląsk site:instagram.com/reel/',
        '"Restaurant Week" Gliwice site:instagram.com/p/',
        '"Restaurant Week" Chorzów site:instagram.com/p/',
    ],
}

def search_bing(query):
    url = "https://www.bing.com/search?q=" + urllib.parse.quote(query)

    request = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0"}
    )

    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            html = response.read().decode("utf-8", errors="ignore")

        links = re.findall(
            r'https?(?:%3A|:)(?:%2F|/){2}'
            r'(?:www\.)?instagram\.com'
            r'(?:/|%2F)(?:p|reel)(?:/|%2F)'
            r'[A-Za-z0-9_-]+',
            html,
            re.IGNORECASE
        )

        return [
            urllib.parse.unquote(link)
            for link in links
        ]

    except Exception as error:
        print("Search error:", error)
        return []


def main():
    existing = []

    if OUTPUT.exists():
        try:
            data = json.loads(OUTPUT.read_text(encoding="utf-8"))
            if isinstance(data, list):
                existing = data
        except (json.JSONDecodeError, OSError):
            pass

    known = {
        item["url"]
        for item in existing
        if isinstance(item, dict) and "url" in item
    }

    for region, queries in QUERIES.items():
        for query in queries:
            print("Searching:", region, query)

            for url in search_bing(query):
                url = url.split("?")[0].rstrip("/") + "/"

                if url not in known:
                    existing.append({
                        "url": url,
                        "region": region,
                        "note": "Restaurant Week – wynik wyszukiwania",
                        "found_at": datetime.now(timezone.utc).isoformat()
                    })
                    known.add(url)

            time.sleep(3)

    OUTPUT.write_text(
        json.dumps(existing, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    print("Total posts:", len(existing))


if __name__ == "__main__":
    main()
