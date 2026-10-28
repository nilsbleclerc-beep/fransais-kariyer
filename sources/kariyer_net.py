"""
Kariyer.net — offres dont le LIEU DE TRAVAIL est la France (filtre « Yurt Dışı », pays = Fransa).

Accès (vérifié le 28/10/2026) :
- robots.txt autorise /is-ilanlari/* et /is-ilani/* (interdit /filtre, *?ckw*, comptes, etc.).
- /is-ilanlari/yurtdisi est la page « Yurtdışı İş İlanları » : TOUTES les offres hors Turquie/KKTC
  (≈ 40-50 annonces, une seule page). Chaque carte porte des attributs structurés
  countryName="…" / cityName="…" ; on ne garde que countryName == "Fransa". Le simple mot-clé
  « Fransa » / « Fransızca » renvoie des postes à Istanbul (« Fransızca bilen ») : jamais utilisé.
- Détail /is-ilani/<slug>-<id> : état Nuxt (window.__NUXT__) -> jobGeneralInformation
  (title, qualifications, postingDate, closingDate, locations[].countryName/cityName, isActive),
  jobCandidateCriteria.languageText, jobCompanyInformation.companyName. Le pays est revérifié ici.
Le site embarque PerimeterX : en cas de 403/défi, on renvoie [] (pas de contournement).

Fiabilité : postingDate = dernière (re)publication affichée par le site ; pays structuré (fiable) ;
ville souvent vide pour l'étranger -> on cherche une ville française dans le titre/texte, sinon "France".
"""
import datetime
import json
import re
from typing import Dict, List, Optional, Tuple

from models import JobOpportunity
from .common import http_get, now_str
from .gurbetilan import detect_language_requirements, extract_visa_evidence, lines_text, snippet_of, utc_now_iso

SOURCE = "Kariyer.net (Yurt Dışı › Fransa)"
BASE = "https://www.kariyer.net"
ABROAD_URL = BASE + "/is-ilanlari/yurtdisi"
FRANCE_NAMES = {"fransa", "france"}
DELAY = 2.0

_FR_CITIES = ["Paris", "Lyon", "Marseille", "Marsilya", "Toulouse", "Nice", "Nantes", "Strasbourg", "Montpellier",
              "Bordeaux", "Lille", "Rennes", "Reims", "Le Havre", "Saint-Étienne", "Toulon", "Grenoble", "Dijon",
              "Angers", "Nîmes", "Villeurbanne", "Clermont-Ferrand", "Le Mans", "Aix-en-Provence", "Brest", "Tours",
              "Amiens", "Limoges", "Annecy", "Perpignan", "Metz", "Besançon", "Orléans", "Rouen", "Mulhouse", "Caen",
              "Nancy", "Calais", "Dunkerque", "Roissy", "Saint-Denis", "Montbéliard", "Colmar", "Valence", "Avignon"]

_MONTHS_TR = {"ocak": 1, "şubat": 2, "subat": 2, "mart": 3, "nisan": 4, "mayıs": 5, "mayis": 5, "haziran": 6,
              "temmuz": 7, "ağustos": 8, "agustos": 8, "eylül": 9, "eylul": 9, "ekim": 10, "kasım": 11, "kasim": 11,
              "aralık": 12, "aralik": 12}


def parse_tr_date(s: str) -> str:
    """« 09 Kasım 2026 » -> 2026-11-09 ; ISO conservé ; "" sinon."""
    s = (s or "").strip()
    m = re.match(r"(\d{4}-\d{2}-\d{2})", s)
    if m:
        return m.group(1)
    m = re.match(r"(\d{1,2})\s+([A-Za-zÇĞİÖŞÜçğıöşü]+)\s+(\d{4})", s)
    if m and m.group(2).lower() in _MONTHS_TR:
        return f"{m.group(3)}-{_MONTHS_TR[m.group(2).lower()]:02d}-{int(m.group(1)):02d}"
    return ""


# ------------------------------------------------------------------ Nuxt (window.__NUXT__) --------
def _split_top(s: str) -> List[str]:
    """Découpe une liste d'arguments JS au niveau 0 (chaînes, crochets, accolades respectés)."""
    out, depth, cur, i, n = [], 0, [], 0, len(s)
    while i < n:
        c = s[i]
        if c == '"':
            j = i + 1
            while j < n and s[j] != '"':
                j += 2 if s[j] == "\\" else 1
            cur.append(s[i:j + 1]); i = j + 1; continue
        if c in "[{(":
            depth += 1
        elif c in "]})":
            depth -= 1
        if c == "," and depth == 0:
            out.append("".join(cur)); cur = []
        else:
            cur.append(c)
        i += 1
    if cur:
        out.append("".join(cur))
    return out


def _js_value(tok: str):
    tok = tok.strip()
    if tok.startswith('"'):
        try:
            return json.loads(tok)
        except ValueError:
            return tok.strip('"')
    if tok in ("true", "!0"):
        return True
    if tok in ("false", "!1"):
        return False
    if tok in ("null", "void 0", ""):
        return None
    try:
        return float(tok) if "." in tok else int(tok)
    except ValueError:
        return tok


def nuxt_state(html: str) -> Tuple[str, Dict[str, object]]:
    """(corps de la fonction __NUXT__, {nom de paramètre: valeur})."""
    i = html.find("window.__NUXT__=(function(")
    if i < 0:
        return "", {}
    p0 = i + len("window.__NUXT__=(function(")
    p1 = html.find(")", p0)
    params = html[p0:p1].split(",")
    end = html.find("</script>", p1)
    body = html[p1:end]
    k = body.rfind("}(")
    args_src = body[k + 2:].rstrip().rstrip(";").rstrip(")").rstrip(")")
    args = [_js_value(t) for t in _split_top(args_src)]
    return body[:k], dict(zip(params, args))


def _val(raw: str, env: Dict[str, object]):
    raw = raw.strip()
    if raw.startswith('"') or re.match(r"^-?[\d.]+$", raw) or raw in ("true", "false", "null", "!0", "!1", "void 0"):
        return _js_value(raw)
    return env.get(raw, None)


def _field(block: str, key: str, env: Dict[str, object]):
    m = re.search(r"[{,]" + re.escape(key) + r':("(?:[^"\\]|\\.)*"|[\w$.!-]+)', block)
    return _val(m.group(1), env) if m else None


def parse_listing(html: str) -> List[Dict]:
    """Cartes de /is-ilanlari/yurtdisi : url, country, city, title (attributs structurés)."""
    out = []
    for m in re.finditer(r'<div data-test="ad-card"([^>]*)>\s*<div[^>]*>\s*<a href="(/is-ilani/[^"]+)"', html):
        attrs = dict(re.findall(r'(\w+)="([^"]*)"', m.group(1)))
        out.append({"url": BASE + m.group(2), "country": attrs.get("countryName", ""),
                    "city": attrs.get("cityName", ""), "title": attrs.get("positionName", "")})
    return out


def _french_city(text: str) -> str:
    for c in _FR_CITIES:
        if re.search(r"(?<!\w)" + re.escape(c) + r"(?!\w)", text or "", re.I):
            return "Marseille" if c == "Marsilya" else c
    return ""


def parse_detail(html: str, url: str, today: Optional[datetime.date] = None) -> Tuple[Optional[JobOpportunity], str]:
    today = today or datetime.date.today()
    body, env = nuxt_state(html)
    i = body.find("jobGeneralInformation:{")
    if i < 0:
        return None, "état Nuxt introuvable"
    gen = body[i:i + 60000]
    title = _field(gen, "title", env) or ""
    if not title:
        return None, "sans titre"
    locs = re.findall(r"countryName:([^,}]+),cityId:[^,}]+,cityName:([^,}]+)", gen[:gen.find("jobIstatistics")] if "jobIstatistics" in gen else gen[:5000])
    countries = [str(_val(c, env) or "") for c, _ in locs]
    if not any(c.lower() in FRANCE_NAMES for c in countries):
        return None, f"hors France ({', '.join(countries) or '?'})"
    cities = [str(_val(ci, env) or "") for c, ci in locs if str(_val(c, env) or "").lower() in FRANCE_NAMES]
    if _field(gen, "isActive", env) is False:
        return None, "inactive"
    posted = (str(_field(gen, "postingDate", env) or "")[:10]) or parse_tr_date(str(_field(gen, "publishDate", env) or ""))
    closing = parse_tr_date(str(_field(gen, "closingDate", env) or ""))
    if closing and closing < today.isoformat():
        return None, f"expirée ({closing})"
    qual = _field(gen, "qualificationsWithHtml", env) or _field(gen, "qualifications", env) or ""
    description = lines_text(str(qual))
    langs = re.search(r"languageText:\[([^\]]*)\]", body)
    lang_text = ", ".join(str(_val(t, env) or "") for t in _split_top(langs.group(1))) if langs else ""
    comp = body.find("jobCompanyInformation:{")
    company = (_field(body[comp:comp + 3000], "companyName", env) if comp >= 0 else None) or "Entreprise (Kariyer.net)"
    city = next((c for c in cities if c), "") or _french_city(title + " " + description) or "France"
    full = description + (f"\nDil: {lang_text}" if lang_text else "")
    reqs = detect_language_requirements(full) + _kariyer_lang_levels(lang_text)
    seen, reqs_u = set(), []
    for r in reqs:
        if r.split(":")[0] not in seen:
            seen.add(r.split(":")[0]); reqs_u.append(r)
    snippet = snippet_of(description)
    return JobOpportunity(
        title=title, title_fr=title, company=str(company),
        location=f"{city}, France" if city != "France" else "France",
        city=city, country="FR", url=url, source=SOURCE, source_type="board", kind="offer",
        snippet=snippet, snippet_fr=snippet, description=full,
        posted_at=posted, verified_at=utc_now_iso(), discovered_at=now_str(),
        contact_info="Candidature via Kariyer.net", language_requirements=reqs_u,
        visa_evidence=extract_visa_evidence(full), visa_sponsorship="",
    ), ""


def _kariyer_lang_levels(lang_text: str) -> List[str]:
    """« Fransızca(Okuma : İleri, Yazma : Orta, Konuşma : İleri) » -> ["fr:fluent"] (niveau de Konuşma)."""
    out = []
    names = {"türkçe": "tr", "fransızca": "fr", "ingilizce": "en"}
    for name, code in names.items():
        m = re.search(name + r"\s*\(([^)]*)\)", lang_text or "", re.I)
        if not m:
            continue
        lv = re.search(r"Konuşma\s*:\s*(\w+)", m.group(1), re.I)
        word = (lv.group(1) if lv else m.group(1)).lower()
        level = "fluent" if word.startswith(("ileri", "çok", "anadil")) else "intermediate" if word.startswith(("orta", "iyi")) else "basic"
        out.append(f"{code}:{'required' if code == 'tr' else level}")
    return out


def fetch(profile: dict = None) -> List[JobOpportunity]:
    jobs: List[JobOpportunity] = []
    try:
        r = http_get(ABROAD_URL, delay=DELAY)
        if r is None or r.status_code != 200 or "ad-card" not in r.text:
            print(f"[-] Kariyer.net : liste Yurt Dışı inaccessible ({getattr(r, 'status_code', 'réseau')}) — "
                  "probable défi anti-bot PerimeterX, pas de contournement.")
            return []
        if not r.url.rstrip("/").endswith("/yurtdisi"):
            print(f"[-] Kariyer.net : redirection inattendue vers {r.url} — URL Yurt Dışı à revoir.")
            return []
        cards = parse_listing(r.text)
        fr_cards = [c for c in cards if c["country"].lower() in FRANCE_NAMES]
        print(f"[+] Kariyer.net : {len(cards)} offres à l'étranger, dont {len(fr_cards)} en France")
        for c in fr_cards:
            d = http_get(c["url"], delay=DELAY)
            if d is None or d.status_code != 200:
                continue
            job, why = parse_detail(d.text, c["url"])
            if job:
                jobs.append(job)
            else:
                print(f"    Kariyer.net rejet : {why} — {c['url']}")
    except Exception as e:  # ne jamais lever
        print(f"[-] Kariyer.net : {e}")
    return jobs
