"""
Adzuna API (https://developer.adzuna.com) — agrégateur d'offres (France : /v1/api/jobs/fr/search/{page}).

Clés gratuites : inscription sur https://developer.adzuna.com/signup, puis ADZUNA_APP_ID / ADZUNA_APP_KEY.
Sans clés : log « clé manquante » et [].
La description renvoyée par l'API est un extrait (~500 car.), pas le texte complet ; redirect_url
mène à l'annonce. `created` = date de première indexation par Adzuna.
"""
import os
from typing import Dict, List, Optional

from models import JobOpportunity
from .common import clean_text, http_get, now_str, to_iso_date

SOURCE = "Adzuna"
SEARCH_URL = "https://api.adzuna.com/v1/api/jobs/fr/search/{page}"
WHAT_OR = "turc turcophone turque turkish"
PER_PAGE = 50
MAX_PAGES = 4


def snippet_of(text: str, limit: int = 300) -> str:
    text = (text or "").strip()
    if len(text) <= limit:
        return text
    return text[:limit].rsplit(" ", 1)[0].rstrip(" ,;:.-") + "…"


def map_result(r: Dict) -> Optional[JobOpportunity]:
    title = clean_text(r.get("title") or "", limit=300)
    url = (r.get("redirect_url") or "").strip()
    if not title or not url:
        return None
    loc = r.get("location") or {}
    area = loc.get("area") or []
    if area and str(area[0]).lower() != "france":
        return None
    city = area[-1] if len(area) >= 3 else ""
    description = clean_text(r.get("description") or "", limit=8000)
    extras = []
    if r.get("salary_min") or r.get("salary_max"):
        lo, hi = r.get("salary_min"), r.get("salary_max")
        extras.append(f"Salaire : {int(lo)}–{int(hi)} €" if lo and hi and lo != hi else f"Salaire : {int(lo or hi)} €")
    extras += [x for x in (r.get("contract_type"), r.get("contract_time")) if x]
    head = " | ".join(extras)
    snippet = snippet_of((head + " — " if head else "") + description)
    return JobOpportunity(
        title=title,
        title_fr=title,
        company=((r.get("company") or {}).get("display_name") or "").strip() or "Entreprise non communiquée",
        location=loc.get("display_name") or city or "France",
        city=city,
        country="FR",
        url=url,
        source=SOURCE,
        source_type="board",
        kind="offer",
        snippet=snippet,
        snippet_fr=snippet,
        description=description,
        posted_at=to_iso_date(r.get("created")),
        discovered_at=now_str(),
        tags=[t for t in ((r.get("category") or {}).get("label"),) if t],
    )


def fetch(profile: dict = None) -> List[JobOpportunity]:
    app_id = os.environ.get("ADZUNA_APP_ID", "").strip()
    app_key = os.environ.get("ADZUNA_APP_KEY", "").strip()
    if not app_id or not app_key:
        print("[i] Adzuna : clé manquante (ADZUNA_APP_ID / ADZUNA_APP_KEY) — source ignorée")
        return []
    out: List[JobOpportunity] = []
    seen = set()
    try:
        for page in range(1, MAX_PAGES + 1):
            resp = http_get(
                SEARCH_URL.format(page=page),
                params={"app_id": app_id, "app_key": app_key, "results_per_page": PER_PAGE,
                        "what_or": WHAT_OR, "max_days_old": 31, "sort_by": "date"},
                headers={"Accept": "application/json"},
            )
            if resp is None or resp.status_code != 200:
                print(f"[-] Adzuna page {page} : HTTP {getattr(resp, 'status_code', 'réseau')}")
                break
            results = (resp.json() or {}).get("results") or []
            for r in results:
                key = r.get("id") or r.get("redirect_url")
                if key in seen:
                    continue
                seen.add(key)
                job = map_result(r)
                if job:
                    out.append(job)
            if len(results) < PER_PAGE:
                break
        print(f"[+] Adzuna : {len(out)} offres")
    except Exception as e:
        print(f"[-] Adzuna : erreur {e}")
    return out
