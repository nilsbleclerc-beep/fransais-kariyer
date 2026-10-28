#!/usr/bin/env python3
"""
Fransaİş — collecte d'offres d'emploi RÉELLES en France pour une candidate vivant en Turquie.

1. Charge le profil (profile.json : langues, ancienneté max des annonces).
2. Appelle chaque collecteur de sources.SOURCE_MODULES (module absent ou en erreur : journalisé, ignoré).
3. Filtre avec quality.filter_offers (France, fraîcheur, URL vivante, langue compatible, doublons).
4. Ajoute les fiches statiques (kind="lead" : groupes turcs, institutions, scale-ups — ce ne sont pas des offres).
5. Écrit offres_france_turquie.json/.csv, rejected_offers.json (audit, non affiché) et dashboard.html.
"""
import argparse
import datetime
import importlib
import json
import os
import sys
import time
from collections import Counter, defaultdict

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

import quality
from scrapers import BilateralJobScanner

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
console = Console()


def load_profile(path: str = os.path.join(BASE_DIR, "profile.json")) -> dict:
    try:
        with open(path, encoding="utf-8") as f:
            return {k: v for k, v in json.load(f).items() if not k.startswith("_")}
    except (OSError, ValueError) as e:
        console.print(f"[yellow]⚠ profile.json illisible ({e}) : profil par défaut[/yellow]")
        return {"languages": {"tr": "native", "en": "A2-B1", "fr": "A1"}, "max_age_days": 45, "target_country": "FR"}


def collect_from_sources(profile: dict):
    """Renvoie (jobs, origin{id(job): module}, stats{module: {...}})."""
    try:
        from sources import SOURCE_MODULES
    except ImportError as e:
        console.print(f"[red]✗ Paquet sources introuvable : {e}[/red]")
        return [], {}, {}
    jobs, origin, stats = [], {}, {}
    for name in SOURCE_MODULES:
        t0 = time.time()
        st = stats[name] = {"status": "ok", "collected": 0, "kept": 0, "rejected": Counter(), "error": ""}
        try:
            mod = importlib.import_module(f"sources.{name}")
        except ModuleNotFoundError as e:
            if e.name in (f"sources.{name}", name):
                st["status"] = "absent"
                console.print(f"  [dim]– {name} : module absent, ignoré[/dim]")
            else:
                st.update(status="error", error=f"dépendance manquante : {e.name}")
                console.print(f"  [red]✗ {name} : dépendance manquante ({e.name})[/red]")
            continue
        except Exception as e:  # noqa: BLE001 — un module cassé ne doit pas arrêter la collecte
            st.update(status="error", error=repr(e)[:200])
            console.print(f"  [red]✗ {name} : import impossible ({e!r})[/red]")
            continue
        fetch = getattr(mod, "fetch", None)
        if not callable(fetch):
            st.update(status="error", error="pas de fonction fetch(profile)")
            console.print(f"  [red]✗ {name} : pas de fetch(profile)[/red]")
            continue
        try:
            found = list(fetch(profile) or [])
        except Exception as e:  # noqa: BLE001
            st.update(status="error", error=repr(e)[:200])
            console.print(f"  [red]✗ {name} : erreur pendant fetch ({e!r})[/red]")
            continue
        for j in found:
            origin[id(j)] = name
        jobs.extend(found)
        st["collected"] = len(found)
        console.print(f"  [green]✓[/green] {name} : {len(found)} annonce(s) collectée(s) en {time.time() - t0:.0f}s")
    return jobs, origin, stats


def print_summary(stats: dict, kept_offers: list, leads: list):
    table = Table(title="Résumé par source / Kaynak özeti", header_style="bold magenta")
    table.add_column("Source")
    table.add_column("État")
    table.add_column("Collectées", justify="right")
    table.add_column("Gardées", justify="right")
    table.add_column("Rejetées (raison : nombre)")
    total_rej = Counter()
    for name, st in stats.items():
        total_rej.update(st["rejected"])
        reasons = ", ".join(f"{r}: {n}" for r, n in st["rejected"].most_common()) or "-"
        state = st["status"] + (f" ({st['error'][:40]})" if st["error"] else "")
        table.add_row(name, state, str(st["collected"]), str(st["kept"]), reasons)
    console.print(table)
    console.print(f"[bold green]Offres réelles gardées : {len(kept_offers)}[/bold green] | "
                  f"fiches entreprises (leads) : {len(leads)} | rejetées : {sum(total_rej.values())} "
                  f"({', '.join(f'{r}: {n}' for r, n in total_rej.most_common()) or '-'})")


def run_agent(pages: int = 4, html: bool = True, verify_urls: bool = True):
    console.print(Panel("[bold red]🇹🇷 FRANSAİŞ — Fransa'da gerçek ve güncel iş ilanları 🇫🇷[/bold red]\n"
                        "[dim]Yalnızca Fransa'daki, güncel, dil seviyesine uygun ilanlar · Offres réelles, "
                        "récentes, en France, compatibles avec le niveau de langue[/dim]", border_style="red"))
    profile = load_profile()
    profile["max_pages"] = pages  # utilisé par les collecteurs paginés (ex. gurbetilan)

    console.print("[bold]1. Collecte des offres (sources/*)[/bold]")
    raw, origin, stats = collect_from_sources(profile)

    console.print(f"[bold]2. Filtre qualité de {len(raw)} annonce(s) (vérification des URL : "
                  f"{'oui' if verify_urls else 'non'})[/bold]")
    kept, rejected = quality.filter_offers(raw, profile, verify_urls=verify_urls)

    by_url = defaultdict(list)
    for j in raw:
        by_url[(j.url, j.title)].append(origin.get(id(j), "?"))
    for j in kept:
        name = origin.get(id(j))
        if name in stats:
            stats[name]["kept"] += 1
    for r in rejected:
        names = by_url.get((r["url"], r["title"])) or ["?"]
        name = names.pop(0) if len(names) > 1 else names[0]
        r["module"] = name
        if name in stats:
            stats[name]["rejected"][r["reason"]] += 1

    offers = sorted((j for j in kept if j.kind == "offer"), key=lambda j: (j.relevance_score, j.posted_at), reverse=True)
    source_leads = [j for j in kept if j.kind != "offer"]

    console.print("[bold]3. Fiches entreprises / institutions (leads, pas des offres)[/bold]")
    leads = source_leads + BilateralJobScanner().get_all_leads()
    print_summary(stats, offers, leads)

    if offers:
        top = Table(title="Meilleures offres réelles", header_style="bold cyan")
        for col, w in (("Score", 6), ("Entreprise", 22), ("Poste", 36), ("Ville", 14), ("Pourquoi", 40)):
            top.add_column(col, width=w)
        for j in offers[:12]:
            top.add_row(str(j.relevance_score), j.company[:22], j.title[:36], (j.city or j.location)[:14],
                        " · ".join(j.match_reasons_fr[:2])[:80])
        console.print(top)
    else:
        console.print("[yellow]Aucune offre réelle ne passe les filtres aujourd'hui (les fiches restent "
                      "disponibles). C'est voulu : mieux vaut rien qu'une fausse joie.[/yellow]")

    from exporter import export_to_csv, export_to_html_dashboard, export_to_json
    all_items = offers + leads
    export_to_csv(all_items, os.path.join(BASE_DIR, "offres_france_turquie.csv"))
    export_to_json(all_items, os.path.join(BASE_DIR, "offres_france_turquie.json"))
    audit = {
        "generated_at": datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat(),
        "profile": profile,
        "sources": {n: {**{k: v for k, v in st.items() if k != "rejected"}, "rejected": dict(st["rejected"])}
                    for n, st in stats.items()},
        "counts": dict(Counter(r["reason"] for r in rejected)),
        "rejected": rejected,
    }
    with open(os.path.join(BASE_DIR, "rejected_offers.json"), "w", encoding="utf-8") as f:
        json.dump(audit, f, ensure_ascii=False, indent=2)
    console.print(f"[✓] Audit des rejets : rejected_offers.json ({len(rejected)})")
    if html:
        export_to_html_dashboard(all_items, os.path.join(BASE_DIR, "dashboard.html"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fransa'daki gerçek ve güncel iş ilanlarını toplar ve filtreler")
    parser.add_argument("--pages", type=int, default=4, help="Pages max. par collecteur paginé")
    # Ancienne option de la recherche DuckDuckGo (supprimée) : acceptée et ignorée pour compatibilité
    parser.add_argument("--dorks", type=int, default=0, help=argparse.SUPPRESS)
    parser.add_argument("--no-html", action="store_true", help="Ne pas régénérer dashboard.html")
    parser.add_argument("--no-verify", action="store_true",
                        help="Ne pas vérifier les URL (déconseillé : les offres de date inconnue seront écartées)")
    args = parser.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        except (OSError, ValueError):
            pass
    run_agent(pages=args.pages, html=not args.no_html, verify_urls=not args.no_verify)
