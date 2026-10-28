"""
France Travail — API « Offres d'emploi v2 » (https://francetravail.io/data/api/offres-emploi).

Accès : OAuth2 client_credentials. Créer une application sur https://francetravail.io (espace
partenaire), y souscrire à l'API « Offres d'emploi v2 », puis définir FT_CLIENT_ID / FT_CLIENT_SECRET.
Sans clés : log « clé manquante » et [].

Recherche : motsCles = turc / turcophone / turque (une requête par mot, motsCles combine en ET),
publieeDepuis = 31 jours (valeurs admises : 1, 3, 7, 14, 31), pagination range=p-d (150 max / appel).
Réponses : 200 (tout), 206 (partiel, header Content-Range « offres p-d/total »), 204 (aucune offre).
"""
import os
import re
from typing import Dict, List, Optional

from models import JobOpportunity
from .common import clean_text, http_get, http_post, now_str, to_iso_date

SOURCE = "France Travail"
TOKEN_URL = "https://entreprise.francetravail.fr/connexion/oauth2/access_token"
SEARCH_URL = "https://api.francetravail.io/partenaire/offresdemploi/v2/offres/search"
SCOPE = "api_offresdemploiv2 o2dsoffre"
KEYWORDS = ["turc", "turcophone", "turque"]
PAGE_SIZE = 150
MAX_PER_KEYWORD = 600
DETAIL_URL = "https://candidat.francetravail.fr/offres/recherche/detail/{id}"

# Libellés de langue France Travail -> code ISO
LANG_CODES = {"turc": "tr", "français": "fr", "francais": "fr", "anglais": "en", "allemand": "de",
              "espagnol": "es", "italien": "it", "arabe": "ar", "russe": "ru", "portugais": "pt"}
# exigence : "E" = exigée, "S" = souhaitée
EXIGENCE = {"E": "required", "S": "preferred"}

# Libellé de lieu français : « 75 - Paris 15e », « 2A - Ajaccio », « 971 - Pointe-à-Pitre »
_FR_LIBELLE = re.compile(r"^\s*(\d{2}|2A|2B|97\d)\s*-\s*(.*)$", re.I)


def snippet_of(text: str, limit: int = 300) -> str:
    text = (text or "").strip()
    if len(text) <= limit:
        return text
    cut = text[:limit].rsplit(" ", 1)[0]
    return cut.rstrip(" ,;:.-") + "…"


def get_token(client_id: str, client_secret: str) -> Optional[str]:
    resp = http_post(
        TOKEN_URL,
        params={"realm": "/partenaire"},
        data={"grant_type": "client_credentials", "client_id": client_id,
              "client_secret": client_secret, "scope": SCOPE},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        delay=0,
    )
    if resp is None or resp.status_code != 200:
        detail = ""
        if resp is not None:
            try:
                err = resp.json()
                detail = f" {err.get('error', '')} : {err.get('error_description', '')}"
            except ValueError:
                detail = f" {resp.text[:200]}"
        print(f"[-] France Travail : échec token ({getattr(resp, 'status_code', 'réseau')}){detail}")
        return None
    try:
        return resp.json().get("access_token")
    except ValueError:
        return None


def map_languages(langues) -> List[str]:
    out = []
    for lg in langues or []:
        lib = (lg.get("libelle") or "").strip().lower()
        code = next((c for name, c in LANG_CODES.items() if lib.startswith(name)), None)
        if not code:
            continue
        out.append(f"{code}:{EXIGENCE.get((lg.get('exigence') or '').upper(), 'preferred')}")
    return out


def parse_location(lieu: Dict):
    """Renvoie (location, city, is_france)."""
    lieu = lieu or {}
    libelle = (lieu.get("libelle") or "").strip()
    m = _FR_LIBELLE.match(libelle)
    if m:
        return libelle, m.group(2).strip(), True
    if lieu.get("commune") or lieu.get("codePostal"):
        return libelle, libelle, True
    if libelle.lower() == "france":
        return libelle, "", True
    return libelle, "", False  # offre à l'étranger (ex. « Allemagne »)


def map_offer(o: Dict) -> Optional[JobOpportunity]:
    oid = o.get("id")
    title = (o.get("intitule") or "").strip()
    if not oid or not title:
        return None
    location, city, is_fr = parse_location(o.get("lieuTravail"))
    if not is_fr:
        return None
    url = ((o.get("origineOffre") or {}).get("urlOrigine") or "").strip() or DETAIL_URL.format(id=oid)
    description = clean_text(o.get("description") or "", limit=8000)
    extras = [x for x in (o.get("typeContratLibelle") or o.get("typeContrat"),
                          (o.get("salaire") or {}).get("libelle"),
                          o.get("dureeTravailLibelle")) if x]
    head = " | ".join(extras)
    snippet = snippet_of((head + " — " if head else "") + description)
    return JobOpportunity(
        title=title,
        title_fr=title,
        company=((o.get("entreprise") or {}).get("nom") or "").strip() or "Entreprise non communiquée",
        location=location or city,
        city=city,
        country="FR",
        url=url,
        source=SOURCE,
        source_type="official_api",
        kind="offer",
        snippet=snippet,
        snippet_fr=snippet,
        description=description or snippet,
        posted_at=to_iso_date(o.get("dateCreation")),
        language_requirements=map_languages(o.get("langues")),
        discovered_at=now_str(),
        tags=[t for t in (o.get("typeContrat"), o.get("romeLibelle")) if t],
    )


def _search(token: str, keyword: str) -> List[Dict]:
    results, start = [], 0
    while start < MAX_PER_KEYWORD:
        resp = http_get(
            SEARCH_URL,
            params={"motsCles": keyword, "publieeDepuis": 31, "range": f"{start}-{start + PAGE_SIZE - 1}"},
            headers={"Authorization": f"Bearer {token}", "Accept": "application/json"},
            delay=0.5,
        )
        if resp is None:
            break
        if resp.status_code == 204:
            break
        if resp.status_code not in (200, 206):
            print(f"[-] France Travail « {keyword} » : HTTP {resp.status_code}")
            break
        batch = (resp.json() or {}).get("resultats") or []
        results.extend(batch)
        total = None
        m = re.search(r"/(\d+)", resp.headers.get("Content-Range", ""))
        if m:
            total = int(m.group(1))
        start += PAGE_SIZE
        if resp.status_code == 200 or not batch or (total is not None and start >= total):
            break
    return results


def fetch(profile: dict = None) -> List[JobOpportunity]:
    client_id = os.environ.get("FT_CLIENT_ID", "").strip()
    client_secret = os.environ.get("FT_CLIENT_SECRET", "").strip()
    if not client_id or not client_secret:
        print("[i] France Travail : clé manquante (FT_CLIENT_ID / FT_CLIENT_SECRET) — source ignorée")
        return []
    out: List[JobOpportunity] = []
    try:
        token = get_token(client_id, client_secret)
        if not token:
            return []
        seen = set()
        for kw in KEYWORDS:
            for raw in _search(token, kw):
                if raw.get("id") in seen:
                    continue
                seen.add(raw.get("id"))
                job = map_offer(raw)
                if job:
                    out.append(job)
        print(f"[+] France Travail : {len(out)} offres en France")
    except Exception as e:  # le contrat : ne jamais lever
        print(f"[-] France Travail : erreur {e}")
    return out
