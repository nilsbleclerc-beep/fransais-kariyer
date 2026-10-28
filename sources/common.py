"""Outils partagés par les collecteurs d'offres (sources/*)."""
import datetime
import re
import time
from typing import Optional

import requests

USER_AGENT = (
    "Mozilla/5.0 (compatible; FransaIsJobBot/1.0; personal job search; "
    "+https://nilsbleclerc-beep.github.io/fransais-kariyer/)"
)
TIMEOUT = 15

_session = requests.Session()
_session.headers.update({"User-Agent": USER_AGENT, "Accept-Language": "fr,tr;q=0.9,en;q=0.8"})


def http_get(url: str, *, params=None, headers=None, delay: float = 1.0, **kwargs) -> Optional[requests.Response]:
    """GET poli (délai entre requêtes, timeout). Renvoie None en cas d'erreur réseau."""
    time.sleep(delay)
    try:
        return _session.get(url, params=params, headers=headers, timeout=TIMEOUT, **kwargs)
    except requests.RequestException as e:
        print(f"[-] GET {url} : {e}")
        return None


def http_post(url: str, *, json=None, data=None, headers=None, delay: float = 1.0, **kwargs) -> Optional[requests.Response]:
    time.sleep(delay)
    try:
        return _session.post(url, json=json, data=data, headers=headers, timeout=TIMEOUT, **kwargs)
    except requests.RequestException as e:
        print(f"[-] POST {url} : {e}")
        return None


def now_str() -> str:
    """Format historique de discovered_at."""
    return datetime.datetime.now().strftime("%d/%m/%Y %H:%M")


def to_iso_date(value) -> str:
    """Normalise une date (ISO, timestamp ms, 'dd.mm.yyyy', 'dd/mm/yyyy') en 'YYYY-MM-DD' ; '' si illisible."""
    if value in (None, ""):
        return ""
    if isinstance(value, (int, float)):
        ts = value / 1000 if value > 1e11 else value
        return datetime.datetime.utcfromtimestamp(ts).strftime("%Y-%m-%d")
    s = str(value).strip()
    m = re.match(r"(\d{4})-(\d{2})-(\d{2})", s)
    if m:
        return f"{m.group(1)}-{m.group(2)}-{m.group(3)}"
    m = re.match(r"(\d{1,2})[./](\d{1,2})[./](\d{4})", s)
    if m:
        return f"{m.group(3)}-{int(m.group(2)):02d}-{int(m.group(1)):02d}"
    return ""


def clean_text(html_or_text: str, limit: int = 4000) -> str:
    """Retire les balises HTML et compacte les espaces."""
    txt = re.sub(r"<[^>]+>", " ", html_or_text or "")
    txt = re.sub(r"&nbsp;|&#160;", " ", txt)
    txt = re.sub(r"\s+", " ", txt).strip()
    return txt[:limit]
