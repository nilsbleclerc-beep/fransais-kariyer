#!/usr/bin/env python3
"""
Scanner d'Opportunités d'Emploi Bilatérales (Turquie -> France)
Conçu pour identifier les entreprises et institutions recrutant directement des candidats en Turquie.
Interface bilingue (TURC par défaut / FRANÇAIS en bascule).
"""
import sys
import argparse
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn

from scrapers import BilateralJobScanner
from exporter import export_to_csv, export_to_json, export_to_html_dashboard
from companies_data import TURKISH_COMPANIES_IN_FRANCE

console = Console()

def print_banner():
    banner_text = """[bold red]🇹🇷 TÜRKİYE - FRANSA İŞ VE KARİYER AJANI 🇫🇷[/bold red]
[cyan]Türkiye'den Fransa'ya Vize/Relokasyon Destekli İş Fırsatları Tarayıcısı[/cyan]
[dim]Varsayılan Dil: Türkçe 🇹🇷 | Bascule instantanée vers le Français 🇫🇷[/dim]
[dim]Avrupa Konseyi, OECD, UNESCO, Türk Holdingleri (Beko, THY, Ekol, Trendyol) & KOBİ'ler[/dim]"""
    console.print(Panel(banner_text, border_style="red"))

def run_agent(pages: int = 4, dorks_count: int = 8):
    print_banner()

    scanner = BilateralJobScanner()
    all_jobs = []

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        # Étape 1 : Institutions Internationales & Européennes où la Turquie est membre
        t1 = progress.add_task("[bold blue]1. Uluslararası ve Avrupa Kurumları haritalanıyor (OECD, UNESCO, AİHM, vb.)...", total=None)
        inst_leads = scanner.get_international_institutions_leads()
        all_jobs.extend(inst_leads)
        progress.update(t1, completed=True)
        console.print(f"  [green]✓[/green] {len(inst_leads)} uluslararası/Avrupa kurumu eklendi (Özel MEAE statüsü / Vizesiz doğrudan alım)")

        # Étape 2 : Grandes Multinationales Turques en France (ATS & Sièges)
        t2 = progress.add_task("[bold cyan]2. Fransa'daki Büyük Türk Holdingleri & Şirketleri (ATS & Portallar)...", total=None)
        corp_leads = scanner.get_major_companies_leads()
        all_jobs.extend(corp_leads)
        progress.update(t2, completed=True)
        console.print(f"  [green]✓[/green] {len(corp_leads)} büyük Türk grubu haritalandı (Beko, THY, Ekol, Barsan, Şişecam, Çimsa, Kordsa, Trendyol, vb.)")

        # Étape 3 : Opportunités bilatérales spécialisées (BBL, amo, ISM/AFTCom, Retail Luxe)
        t3 = progress.add_task("[bold green]3. Sektörel ve çift dilli istihdam kanalları entegre ediliyor...", total=None)
        spec_leads = scanner.get_specialized_channels_leads()
        all_jobs.extend(spec_leads)
        progress.update(t3, completed=True)
        console.print(f"  [green]✓[/green] {len(spec_leads)} özel ikili sektör fırsatı eklendi (Euronews, BBL, amo, AFTCom)")

        # Étape 4 : Scale-ups Tech Internationales à Paris (%100 İngilizce & Vize Sponsorluğu)
        t4 = progress.add_task("[bold red]4. %100 İngilizce Paris Tech & AI Girişimleri ekleniyor (Mistral, Qonto, Datadog)...", total=None)
        tech_leads = scanner.get_tech_scaleups_leads()
        all_jobs.extend(tech_leads)
        progress.update(t4, completed=True)
        console.print(f"  [green]✓[/green] {len(tech_leads)} uluslararası Paris Tech girişimi eklendi (%100 İngilizce / 0% Fransızca / Passeport Talent)")

        # Étape 5 : Scraping des annonces récentes de la communauté et PME en France (GurbetIlan)
        t5 = progress.add_task(f"[bold yellow]5. Fransa'daki KOBİ ve saha ilanları taranıyor ({pages} sayfa)...", total=None)
        gurbet_jobs = scanner.scan_gurbet_ilan(max_pages=pages)
        all_jobs.extend(gurbet_jobs)
        progress.update(t5, completed=True)
        console.print(f"  [green]✓[/green] {len(gurbet_jobs)} güncel saha/işletme ilanı çıkarıldı")

        # Étape 6 : Scan web ciblé (Kariyer.net, LinkedIn, SecretCV, Indeed, Eleman.net)
        t6 = progress.add_task(f"[bold magenta]6. Job Board'lar & Web (Kariyer.net, LinkedIn, Indeed, Eleman.net - {dorks_count} sorgu)...", total=None)
        web_jobs = scanner.scan_web_dorks(max_queries=dorks_count, results_per_query=4)
        all_jobs.extend(web_jobs)
        progress.update(t6, completed=True)
        console.print(f"  [green]✓[/green] {len(web_jobs)} profesyonel iş ilanı tespit edildi")

    # Déduplication par URL
    unique_jobs = []
    seen = set()
    for j in all_jobs:
        if j.url not in seen:
            seen.add(j.url)
            unique_jobs.append(j)

    # Tri par score de pertinence décroissant
    unique_jobs.sort(key=lambda x: x.relevance_score, reverse=True)

    console.print(f"\n[bold green]TOPLAM : {len(unique_jobs)} ikili kariyer fırsatı konsolide edildi ![/bold green]\n")

    # Affichage du Top 12 en console
    table = Table(title="Öncelikli Fırsatlar (Örnek Liste)", show_header=True, header_style="bold magenta")
    table.add_column("Uygunluk", style="cyan", width=10)
    table.add_column("Kurum / Şirket", style="bold green", width=24)
    table.add_column("Pozisyon / Başlık", style="white", width=36)
    table.add_column("Konum", style="yellow", width=14)
    table.add_column("Fransızca?", style="magenta", width=16)

    for job in unique_jobs[:12]:
        lang_status = "Gerekmiyor ✅" if not job.french_required else "Gerekli B2+"
        table.add_row(
            f"%{job.relevance_score}",
            job.company[:22],
            job.title[:34],
            job.location[:12],
            lang_status
        )

    console.print(table)

    # Export des résultats
    console.print("\n[bold]Dosyalar oluşturuluyor / Exportation des fichiers...[/bold]")
    export_to_csv(unique_jobs, "offres_france_turquie.csv")
    export_to_json(unique_jobs, "offres_france_turquie.json")
    export_to_html_dashboard(unique_jobs, "dashboard.html")

    console.print("\n[bold cyan]💡 İnteraktif Web Paneli / Tableau de bord :[/bold cyan]")
    console.print("Tarayıcınızda açın: [bold underline]dashboard.html[/bold underline]")
    console.print("[dim]Varsayılan dil Türkçe'dir. Sağ üstteki buton ile Fransızca'ya anında geçiş yapabilirsiniz.[/dim]")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fransa'da personel arayan Türk şirketleri ve kurumlar tarayıcısı")
    parser.add_argument("--pages", type=int, default=4, help="Taranacak sayfa sayısı")
    parser.add_argument("--dorks", type=int, default=8, help="Çalıştırılacak arama sorgusu sayısı")
    args = parser.parse_args()

    run_agent(pages=args.pages, dorks_count=args.dorks)
