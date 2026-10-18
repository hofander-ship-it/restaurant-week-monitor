#!/usr/bin/env python3
"""Discover publicly indexed Instagram post/reel URLs without Instagram login."""
import html
import json
import os
import re
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / 'discovered.json'
MAX_POSTS = 500
SEARCHES = {
    'Szczecin': [
        '"Restaurant Week" Szczecin instagram.com/p/',
        '"Restaurant Week" Szczecin instagram.com/reel/',
        '"restaurantweekszczecin" instagram.com',
        '"Restaurant Week" "Szczecin" restauracja Instagram',
    ],
    'Śląsk': [
        '"Restaurant Week" Katowice instagram.com/p/',
        '"Restaurant Week" Katowice instagram.com/reel/',
        '"Restaurant Week" Gliwice instagram.com',
        '"Restaurant Week" Chorzów instagram.com',
        '"Restaurant Week" Tychy instagram.com',
        '"Restaurant Week" Śląsk Instagram',
    ],
}
POST_RE = re.compile(r'https?://(?:www\.)?instagram\.com/(?:p|reel)/[A-Za-z0-9_-]+/?', re.I)


def search_public(query, engine):
    encoded = urllib.parse.quote_plus(query)
    if engine == 'bing':
        url = 'https://www.bing.com/search?q=' + encoded
    else:
        url = 'https://www.google.com/search?q=' + encoded
    request = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (compatible; RestaurantWeekMonitor/2.0)',
        'Accept-Language': 'pl-PL,pl;q=0.9,en;q=0.7',
    })
    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            page = response.read(1_000_000).decode('utf-8', errors='replace')
    except Exception as exc:
        print(f'{engine}: {type(exc).__name__}: {exc}')
        return []
    # Public search pages often HTML-escape URLs or percent-encode them.
    variants = [html.unescape(page)]
    variants.append(urllib.parse.unquote(variants[0]))
    variants.append(variants[1].replace('\\/', '/').replace('\\u002F', '/'))
    urls = set()
    for variant in variants:
        urls.update(POST_RE.findall(variant))
    return sorted(urls)


def normalize(url):
    parsed = urllib.parse.urlparse(url)
    match = re.fullmatch(r'/(p|reel)/([A-Za-z0-9_-]+)/?', parsed.path, re.I)
    if not match:
        return None
    return f'https://www.instagram.com/{match.group(1).lower()}/{match.group(2)}/'


def main():
    existing = []
    if OUTPUT.exists():
        try:
            value = json.loads(OUTPUT.read_text(encoding='utf-8'))
            if isinstance(value, list):
                existing = [row for row in value if isinstance(row, dict)]
        except (OSError, ValueError) as exc:
            print(f'Cannot read existing results: {exc}')
    seen = {normalize(row.get('url', '')) for row in existing}
    seen.discard(None)
    new_count = 0
    for region, queries in SEARCHES.items():
        for query in queries:
            for engine in ('bing', 'google'):
                found = search_public(query, engine)
                print(f'{region} | {engine} | {len(found)} URL(s) | {query}')
                for raw in found:
                    url = normalize(raw)
                    if url and url not in seen:
                        existing.append({
                            'url': url,
                            'region': region,
                            'note': f'Publiczny wynik wyszukiwania: {query}',
                            'found_at': datetime.now(timezone.utc).isoformat(),
                        })
                        seen.add(url)
                        new_count += 1
                time.sleep(1)
    # Keep a bounded history and preserve the JSON list format used by the PWA.
    existing = existing[-MAX_POSTS:]
    OUTPUT.write_text(json.dumps(existing, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'New: {new_count}; saved: {len(existing)}')
    print('Links are candidates: verify location and Restaurant Week relevance manually.')


if __name__ == '__main__':
    main()
