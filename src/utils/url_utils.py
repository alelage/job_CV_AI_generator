from urllib.parse import urlparse


def normalise_url(url: str) -> str:
    url = url.strip()
    return url if not url else (url if urlparse(url).scheme else "https://" + url)
