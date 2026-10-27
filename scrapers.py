"""
Scrapers et collecteurs d'opportunités d'emploi franco-turques avec support bilingue complet.
Intègre les multinationales turques, les plateformes de la diaspora, et les institutions européennes/internationales.
"""
import time
import datetime
import requests
from bs4 import BeautifulSoup
from typing import List
from ddgs import DDGS

from models import JobOpportunity
from scorer import analyze_job
from config import SEARCH_DORKS
from companies_data import (
    TURKISH_COMPANIES_IN_FRANCE,
    SPECIALIZED_TURKISH_CHANNELS,
    INTERNATIONAL_AND_ACADEMIC_INSTITUTIONS_IN_FRANCE,
    TECH_SCALEUPS_ENGLISH_IN_FRANCE
)

class BilateralJobScanner:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        }

    def scan_gurbet_ilan(self, max_pages: int = 4) -> List[JobOpportunity]:
        """
        Scrape les annonces de la communauté turque et des PME turques en France (GurbetIlan).
        """
        jobs = []
        now_str = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")

        for page in range(1, max_pages + 1):
            url = f"https://www.gurbetilan.com/is-ilanlari/fransa/page/{page}/" if page > 1 else "https://www.gurbetilan.com/is-ilanlari/fransa/"
            try:
                r = requests.get(url, headers=self.headers, timeout=10)
                if r.status_code != 200:
                    break

                soup = BeautifulSoup(r.text, "html.parser")
                articles = soup.find_all("article")
                if not articles:
                    break

                for art in articles:
                    title_elem = art.find(["h2", "h3"])
                    link_elem = art.find("a")
                    snippet_elem = (
                        art.find("div", class_=lambda c: c and any(k in c for k in ["entry-content", "excerpt", "summary"]))
                        or art.find("p")
                    )

                    title = title_elem.get_text(strip=True) if title_elem else "Fransa İş İlanı"
                    link = link_elem["href"] if link_elem and "href" in link_elem.attrs else url
                    snippet = snippet_elem.get_text(strip=True) if snippet_elem else ""

                    score, tags_tr, tags_fr, location, company, french_req, working_lang = analyze_job(title, snippet, link)

                    if any(t in title.lower() for t in ["büro", "transport", "hostes", "yönetici", "muhasebe", "ofis"]):
                        cat_tr = "Lojistik & Büro"
                        cat_fr = "Tertiaire & Logistique"
                    else:
                        cat_tr = "KOBİ & Saha İşleri"
                        cat_fr = "PME & Métiers de Terrain"

                    jobs.append(JobOpportunity(
                        title=title,
                        title_fr=title,
                        company=company if company != "Kurum / Şirket" else "Fransa'daki Türk İşletmesi",
                        location=location,
                        url=link,
                        source="Gurbetİlan France",
                        snippet=snippet,
                        snippet_fr=f"Annonce parue sur la plateforme franco-turque : {snippet[:180]}...",
                        category=cat_tr,
                        category_fr=cat_fr,
                        tags=tags_tr,
                        tags_fr=tags_fr,
                        relevance_score=score,
                        discovered_at=now_str,
                        french_required=french_req,
                        working_language=working_lang,
                        visa_sponsorship="İşverenle Görüşülmeli"
                    ))

                time.sleep(0.5)
            except Exception as e:
                print(f"[-] GurbetIlan tarama hatası (sayfa {page}): {e}")

        return jobs

    def scan_web_dorks(self, max_queries: int = 8, results_per_query: int = 4) -> List[JobOpportunity]:
        """
        Exécute des requêtes ciblées sur Kariyer.net, LinkedIn, Indeed et le web turc via DDGS.
        """
        jobs = []
        now_str = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
        seen_urls = set()

        dorks_to_run = SEARCH_DORKS[:max_queries]

        for dork in dorks_to_run:
            try:
                res = list(DDGS().text(dork, max_results=results_per_query))
                for item in res:
                    url = item.get("href", "")
                    if not url or url in seen_urls:
                        continue
                    seen_urls.add(url)

                    title = item.get("title", "")
                    snippet = item.get("body", "")

                    source = "Web Arama"
                    if "kariyer.net" in url:
                        source = "Kariyer.net"
                    elif "linkedin.com" in url:
                        source = "LinkedIn"
                    elif "indeed.com" in url:
                        source = "Indeed France"
                    elif "eleman.net" in url:
                        source = "Eleman.net"
                    elif "jooble" in url:
                        source = "Jooble"
                    elif "yenibiris" in url:
                        source = "Yenibiriş"
                    elif "secretcv" in url:
                        source = "SecretCV"

                    score, tags_tr, tags_fr, location, company, french_req, working_lang = analyze_job(title, snippet, url)

                    if any(x in url for x in ["kariyer.net", "linkedin.com", "indeed.com", "eleman.net", "jooble", "secretcv", "yenibiris"]):
                        cat_tr = "Kariyer / LinkedIn İlanı"
                        cat_fr = "Job Board Professionnel"
                    else:
                        cat_tr = "İkili Web İlanı"
                        cat_fr = "Offre Spécifique Bilatérale"

                    jobs.append(JobOpportunity(
                        title=title,
                        title_fr=title,
                        company=company,
                        location=location,
                        url=url,
                        source=source,
                        snippet=snippet,
                        snippet_fr=f"Extrait de l'offre indexée : {snippet[:180]}...",
                        category=cat_tr,
                        category_fr=cat_fr,
                        tags=tags_tr,
                        tags_fr=tags_fr,
                        relevance_score=score,
                        discovered_at=now_str,
                        french_required=french_req,
                        working_language=working_lang,
                        visa_sponsorship="İş İlanında Belirtilen Şartlar"
                    ))

                time.sleep(1)
            except Exception as e:
                print(f"[-] Arama sorgusu hatası ({dork}): {e}")

        return jobs

    def get_major_companies_leads(self) -> List[JobOpportunity]:
        """
        Génère les fiches d'opportunités prioritaires pour chaque grande multinationale
        turque implantée en France avec leurs liens ATS directs, filiales et emails RH.
        """
        jobs = []
        now_str = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")

        for comp in TURKISH_COMPANIES_IN_FRANCE:
            title_tr = f"Fransa / Avrupa İşe Alım & Kariyer - {comp['name']}"
            title_fr = f"Postes & Recrutements France / Europe - {comp['name']}"

            snippet_tr = f"Fransa Şubesi: {comp['subsidiary_france']}. Aranan Profiller: {comp['recruitment_focus_tr']}"
            snippet_fr = f"Filiale en France: {comp['subsidiary_france']}. Profils recherchés: {comp['recruitment_focus_fr']}"

            tags_tr = ["🏢 Büyük Türk Grubu", f"📍 {comp['hq_france'][:20]}"]
            tags_fr = ["🏢 Groupe Turc Majeur", f"📍 {comp['hq_france'][:20]}"]

            if comp.get("visa_relocation_friendly"):
                tags_tr.append("✈️ Vize / Relokasyon Destekli")
                tags_fr.append("✈️ Visa / Relocalisation Prise en Charge")

            is_ccift = comp.get("is_ccift_deik", False)
            if is_ccift:
                tags_tr.append("🤝 CCIFT & DEİK Üyesi")
                tags_fr.append("🤝 Membre CCIFT & DEİK")

            # La plupart des postes centraux Koç, Vestel, Trendyol, Barsan opèrent en Turc et Anglais
            french_req = False
            working_lang = "İngilizce veya Türkçe (Merkez İle İletişim)"

            jobs.append(JobOpportunity(
                title=title_tr,
                title_fr=title_fr,
                company=comp["name"],
                location=comp["hq_france"],
                url=comp.get("ats_direct_url") or comp["linkedin_jobs"] or comp["career_portal"],
                source="Resmi ATS / İK Portalı",
                snippet=snippet_tr,
                snippet_fr=snippet_fr,
                category="Büyük Türk Holdingi (Doğrudan Başvuru)",
                category_fr="Multinationale Turque (Candidature Directe)",
                tags=tags_tr,
                tags_fr=tags_fr,
                relevance_score=98 if is_ccift else (95 if comp.get("visa_relocation_friendly") else 85),
                contact_info=comp.get("hr_email") or comp["career_portal"],
                discovered_at=now_str,
                french_required=french_req,
                working_language=working_lang,
                visa_sponsorship="Şirket İçi Transfer (ICT) / Relokasyon Vizesi",
                is_ccift_deik=is_ccift
            ))

        return jobs

    def get_specialized_channels_leads(self) -> List[JobOpportunity]:
        """
        Intègre les opportunités sectorielles ciblées identifiées par les sous-agents
        (Groupe BBL, amo tech, ISM/AFTCom, Retail Luxe, etc.).
        """
        jobs = []
        now_str = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")

        for ch in SPECIALIZED_TURKISH_CHANNELS:
            is_ccift = "BBL" in ch["name"] or "Azkan" in ch["name"]
            tags_tr = list(ch["tags_tr"])
            tags_fr = list(ch["tags_fr"])
            if is_ccift:
                tags_tr.append("🤝 CCIFT Partner")
                tags_fr.append("🤝 Partenaire CCIFT")

            jobs.append(JobOpportunity(
                title=ch["title_tr"],
                title_fr=ch["title_fr"],
                company=ch["name"],
                location=ch["location"],
                url=ch["url"],
                source=ch["source"],
                snippet=ch["snippet_tr"],
                snippet_fr=ch["snippet_fr"],
                category=ch["category_tr"],
                category_fr=ch["category_fr"],
                tags=tags_tr,
                tags_fr=tags_fr,
                relevance_score=ch["score"],
                contact_info=ch.get("contact_info", ""),
                discovered_at=now_str,
                french_required="Fransızca / Çift Dil" in str(ch["tags_tr"]),
                working_language="Türkçe & Fransızca" if "Çift Dil" in str(ch["tags_tr"]) else "Türkçe / İngilizce",
                visa_sponsorship="İkili Sektörel Sözleşme / Passeport Talent",
                is_ccift_deik=is_ccift
            ))

        return jobs

    def get_international_institutions_leads(self) -> List[JobOpportunity]:
        """
        Intègre les institutions européennes et internationales situées en France
        où la Turquie est État membre et qui recrutent directement en Turquie sans visa préalable.
        """
        jobs = []
        now_str = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")

        for inst in INTERNATIONAL_AND_ACADEMIC_INSTITUTIONS_IN_FRANCE:
            jobs.append(JobOpportunity(
                title=f"{inst['name_tr']} - Uluslararası Kadrolar",
                title_fr=f"{inst['name']} - Postes Internationaux",
                company=inst["name_tr"],
                location=inst["city_france"],
                url=inst.get("ats_direct_url") or inst["career_portal"],
                source="Resmi Uluslararası ATS",
                snippet=f"Türkiye Durumu: {inst['turkey_status_tr']} Aranan Alanlar: {inst['recruitment_focus_tr']}",
                snippet_fr=f"Statut Turquie : {inst['turkey_status_fr']} Profils recherchés : {inst['recruitment_focus_fr']}",
                category=inst["category_tr"],
                category_fr=inst["category_fr"],
                tags=inst["tags_tr"],
                tags_fr=inst["tags_fr"],
                relevance_score=inst["score"],
                contact_info=inst.get("career_portal", ""),
                discovered_at=now_str,
                french_required=inst.get("french_required", False),
                working_language=inst.get("working_language", "İngilizce veya Türkçe"),
                visa_sponsorship=inst.get("legal_status_visa_tr", "Özel Statü / Relokasyon %100")
            ))

        return jobs

    def get_tech_scaleups_leads(self) -> List[JobOpportunity]:
        """
        Intègre les scale-ups tech internationales à Paris qui sponsorisent le Passeport Talent
        et où l'anglais est la langue de travail exclusive (0% de français requis).
        """
        jobs = []
        now_str = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")

        for tech in TECH_SCALEUPS_ENGLISH_IN_FRANCE:
            jobs.append(JobOpportunity(
                title=f"{tech['name_tr']} - Yazılım, AI & Veri Pozisyonları",
                title_fr=f"{tech['name']} - Postes Tech / AI / Data (100% Anglais)",
                company=tech["name_tr"],
                location=tech["city_france"],
                url=tech.get("ats_direct_url") or tech["career_portal"],
                source="Resmi Tech ATS",
                snippet=f"Çalışma Dili: {tech['working_language']}. Aranan Alanlar: {tech['recruitment_focus_tr']}",
                snippet_fr=f"Langue de travail : {tech['working_language']}. Profils : {tech['recruitment_focus_fr']}",
                category=tech["category_tr"],
                category_fr=tech["category_fr"],
                tags=tech["tags_tr"],
                tags_fr=tech["tags_fr"],
                relevance_score=tech["score"],
                contact_info=tech.get("career_portal", ""),
                discovered_at=now_str,
                french_required=tech.get("french_required", False),
                working_language=tech.get("working_language", "100% İngilizce"),
                visa_sponsorship=tech.get("legal_status_visa_tr", "Passeport Talent Sponsorluğu")
            ))

        return jobs
