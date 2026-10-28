"""
Jooble REST API (https://jooble.org/api/about) — agrégateur d'offres.

Clé gratuite : formulaire sur https://jooble.org/api/about, puis JOOBLE_KEY. Sans clé : log et [].
Requête : POST https://jooble.org/api/{key}, JSON {keywords, location, page, ResultOnPage, datecreatedfrom}.
Réponse : {totalCount, jobs: [{id, title, location, snippet, salary, source, type, link, company, updated}]}.
Limites : seul un extrait (snippet) est fourni ; `updated` = date de mise à jour (pas forcément de
publication) ; `link` est une redirection Jooble vers l'annonce d'origine.
"""
import datetime
import os
from typing import Dict, List, Optional

from models import JobOpportunity
from .common import clean_text, http_post, now_str, to_iso_date

SOURCE = "Jooble"
API_URL = "https://jooble.org/api/{key}"
# Une clé Jooble est rattachée à l'index d'un pays : si l'index par défaut ne renvoie rien pour la France,
# on essaie l'index français
API_URL_CANDIDATES = [API_URL, "https://fr.jooble.org/api/{key}"]
# Expressions précises d'abord : la recherche de Jooble est floue (« turc » seul ramène surtout du bruit)
KEYWORDS = ["langue turque", "parlant turc", "bilingue turc", "turcophone", "turkish speaking", "turc"]
PER_PAGE = 50
MAX_PAGES = 2
MAX_AGE_DAYS = 31


def snippet_of(text: str, limit: int = 300) -> str:
    text = (text or "").strip()
    if len(text) <= limit:
        return text
    return text[:limit].rsplit(" ", 1)[0].rstrip(" ,;:.-") + "…"


def map_job(j: Dict) -> Optional[JobOpportunity]:
    title = clean_text(j.get("title") or "", limit=300)
    url = (j.get("link") or "").strip()
    if not title or not url:
        return None
    location = clean_text(j.get("location") or "", limit=200)
    city = location.split(",")[0].strip() if location and location.lower() != "france" else ""
    description = clean_text(j.get("snippet") or "", limit=8000)
    extras = [x for x in (clean_text(j.get("salary") or ""), j.get("type")) if x]
    head = " | ".join(extras)
    snippet = snippet_of((head + " — " if head else "") + description)
    return JobOpportunity(
        title=title,
        title_fr=title,
        company=(j.get("company") or "").strip() or "Entreprise non communiquée",
        location=location or "France",
        city=city,
        country="FR",
        url=url,
        source=SOURCE,
        source_type="board",
        kind="offer",
        snippet=snippet,
        snippet_fr=snippet,
        description=description,
        posted_at=to_iso_date(j.get("updated")),
        discovered_at=now_str(),
        tags=[t for t in (j.get("source"),) if t],
    )


def _pick_endpoint(key: str) -> str:
    """Premier index qui renvoie des résultats pour une recherche simple en France."""
    for url in API_URL_CANDIDATES:
        resp = http_post(url.format(key=key), json={"keywords": "turc", "location": "France"},
                         headers={"Content-Type": "application/json"})
        total = 0
        if resp is not None and resp.status_code == 200:
            try:
                total = int((resp.json() or {}).get("totalCount") or 0)
            except (ValueError, TypeError):
                total = 0
        print(f"[i] Jooble {url.split('/api/')[0]} : HTTP {getattr(resp, 'status_code', 'réseau')} totalCount={total}")
        if total:
            return url
    return API_URL


def fetch(profile: dict = None) -> List[JobOpportunity]:
    key = os.environ.get("JOOBLE_KEY", "").strip()
    if not key:
        print("[i] Jooble : clé manquante (JOOBLE_KEY) — source ignorée")
        return []
    out: List[JobOpportunity] = []
    seen = set()
    since = (datetime.date.today() - datetime.timedelta(days=MAX_AGE_DAYS)).isoformat()
    api_url = _pick_endpoint(key)
    try:
        for kw in KEYWORDS:
            for page in range(1, MAX_PAGES + 1):
                body = {"keywords": kw, "location": "France", "page": str(page),
                        "ResultOnPage": str(PER_PAGE), "datecreatedfrom": since}
                resp = http_post(api_url.format(key=key), json=body, headers={"Content-Type": "application/json"})
                if resp is None or resp.status_code != 200:
                    print(f"[-] Jooble « {kw} » p{page} : HTTP {getattr(resp, 'status_code', 'réseau')} "
                          f"{(getattr(resp, 'text', '') or '')[:150]}")
                    break
                data = resp.json() or {}
                # « datecreatedfrom » n'est pas garanti par la doc publique : sans résultat, on réessaie sans
                # (la fraîcheur reste contrôlée par quality.py)
                if page == 1 and not data.get("jobs"):
                    body.pop("datecreatedfrom")
                    retry = http_post(api_url.format(key=key), json=body, headers={"Content-Type": "application/json"})
                    if retry is not None and retry.status_code == 200:
                        data = retry.json() or {}
                print(f"[i] Jooble « {kw} » p{page} : totalCount={data.get('totalCount')} "
                      f"jobs={len(data.get('jobs') or [])}")
                jobs = data.get("jobs") or []
                for j in jobs:
                    k = j.get("id") or j.get("link")
                    if k in seen:
                        continue
                    seen.add(k)
                    job = map_job(j)
                    if job:
                        out.append(job)
                if len(jobs) < PER_PAGE:
                    break
        print(f"[+] Jooble : {len(out)} offres")
    except Exception as e:
        print(f"[-] Jooble : erreur {e}")
    return out
