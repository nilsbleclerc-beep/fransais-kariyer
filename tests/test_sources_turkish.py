"""Tests hors-ligne des sources turques (pytest, ou `python -m tests.test_sources_turkish`)."""
import datetime
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sources import company_ats, gurbetilan, kariyer_net  # noqa: E402

TODAY = datetime.date(2026, 10, 28)


# ------------------------------------------------------------------ détecteurs partagés ---------
def test_language_requirements():
    d = gurbetilan.detect_language_requirements
    assert d("Türkçe ve Fransızca dillerine hakim (Flamanca veya İngilizce bilmek tercih sebebidir).") == \
        ["tr:required", "fr:fluent", "en:preferred"]
    assert d("Türkçe ana dil seviyesinde, akıcı Fransızca.") == ["tr:required", "fr:fluent"]
    assert d("Anglais courant exigé. Maîtrise du turc.") == ["tr:required", "en:fluent"]
    assert d("Fransızca bilmek şart değil. Türkçe konuşan personel aranıyor.") == ["tr:required", "fr:none"]
    assert d("Turkish speaking customer advisor, no French required") == ["tr:required", "fr:none"]
    assert d("Société française basée à Lyon, poste de comptable.") == []


def test_visa_evidence():
    v = gurbetilan.extract_visa_evidence
    assert v("Güzel ekip.\nVize ve konaklama desteği sağlanır.\nMaaş iyi.") == "Vize ve konaklama desteği sağlanır."
    assert v("Uzun süreli çalışmayı hedefleyen,\nÇalışma izni bulunan.") == "Çalışma izni bulunan."
    assert v("Aucun avantage particulier.") == ""


# ------------------------------------------------------------------ GurbetIlan ------------------
LIST_HTML = """
<article class="cpchild-job-card"><a class="cpchild-job-link" href="https://www.gurbetilan.com/ads/nevers-usta/">
<span class="cpchild-job-time">13.10.2026</span><h3 class="cpchild-job-title">Nevers – Dış Cephe Ustası Aranıyor</h3>
<span class="cpchild-job-country">Fransa</span><span class="cpchild-job-city">Paris</span></a></article>
<article class="cpchild-job-card"><a class="cpchild-job-link" href="https://www.gurbetilan.com/ads/eski/">
<span class="cpchild-job-time">24.01.2025</span><h3 class="cpchild-job-title">Lyon – Garson</h3>
<span class="cpchild-job-country">Fransa</span><span class="cpchild-job-city">Lyon</span></a></article>
"""


def detail_html(title, desc, country="FR", locality="Paris", posted="2026-10-13T07:00:00+03:00",
                valid="2026-12-12T07:00:00+00:00"):
    ld = {"@context": "https://schema.org/", "@type": "JobPosting", "title": title, "datePosted": posted,
          "validThrough": valid, "jobLocation": {"@type": "Place", "address": {
              "@type": "PostalAddress", "addressLocality": locality, "addressCountry": country}}}
    return (f'<html><head><script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script></head>'
            f'<body><h1 class="cpchild-single-title">{title}</h1><div class="cpchild-single-description">{desc}</div>'
            '<div class="cpchild-feature-item"><span class="cpchild-feature-label">Sektör</span>'
            '<span class="cpchild-feature-value">Yapı - İnşaat</span></div></body></html>')


def test_gurbetilan_list():
    cards = gurbetilan.parse_list(LIST_HTML)
    assert [c["date"] for c in cards] == ["2026-10-13", "2025-01-24"]
    assert cards[0]["country"] == "Fransa" and cards[0]["url"].endswith("/ads/nevers-usta/")


def test_gurbetilan_detail_ok():
    html = detail_html("Nevers – Dış Cephe İzolasyon Ustası Aranıyor",
                       "<p>Nevers şantiyemiz için usta aranıyor.</p><ul><li>Türkçe bilen</li>"
                       "<li>Çalışma izni bulunan.</li></ul><p>Tel : 06 12 34 56 78</p>")
    j, why = gurbetilan.parse_detail(html, "https://www.gurbetilan.com/ads/x/", today=TODAY)
    assert j is not None, why
    assert j.city == "Nevers" and j.country == "FR" and j.posted_at == "2026-10-13"
    assert j.kind == "offer" and j.source_type == "community" and j.title_fr == j.title
    assert j.language_requirements == ["tr:required"] and j.visa_evidence == "Çalışma izni bulunan."
    assert "06 12 34 56 78" in j.contact_info and len(j.snippet) <= 301 and "Sektör: Yapı" in j.description


def test_gurbetilan_rejections():
    def why(**kw):
        base = dict(title="Paris – Garson Aranıyor", desc="<p>Restoranımız için garson aranıyor.</p>")
        base.update(kw)
        j, reason = gurbetilan.parse_detail(detail_html(base.pop("title"), base.pop("desc"), **base), "u", today=TODAY)
        assert j is None
        return reason
    assert why(country="DE").startswith("hors France")
    assert why(title="Paris – İş arıyorum, garsonluk yapabilirim").startswith("demande d'emploi")
    assert why(title="Paris – Satılık Daire").startswith("annonce non-emploi")
    assert why(valid="2026-10-01T00:00:00+00:00").startswith("expirée")
    assert why(posted="2026-06-01T00:00:00+03:00").startswith("trop ancienne")
    assert why(desc="<p>Brüksel’de faaliyet gösteren firmamız için büro personeli.</p>").startswith("lieu ambigu")


def test_city_from_title():
    assert gurbetilan.city_from_title("Levallois-Perret – Restaurant Personeli") == "Levallois-Perret"
    assert gurbetilan.city_from_title("Paris ve Çevresi – Mantolama Ustası") == "Paris ve Çevresi"
    assert gurbetilan.city_from_title("Restoran için garson aranıyor") == ""


# ------------------------------------------------------------------ Kariyer.net -----------------
def card(country, city, href, pos="Satış Temsilcisi"):
    return (f'<div data-test="ad-card" positionName="{pos}" countryId="1" countryName="{country}" cityId="2" '
            f'cityName="{city}" class="job-list-card-item"><div data-v-1><a href="{href}" target="_blank">x</a></div></div>')


def test_kariyer_listing_filters_france():
    html = card("Türkiye", "İstanbul(Avr.)", "/is-ilani/a-fransizca-bilen-satis-1", "Fransızca Bilen Satış") + \
        card("Fransa", "Paris", "/is-ilani/b-paris-2") + card("Almanya", "", "/is-ilani/c-3")
    cards = kariyer_net.parse_listing(html)
    assert len(cards) == 3
    fr = [c for c in cards if c["country"].lower() in kariyer_net.FRANCE_NAMES]
    assert [c["url"] for c in fr] == ["https://www.kariyer.net/is-ilani/b-paris-2"]


def nuxt_detail(country="Fransa", city="", closing="09 Kasım 2026"):
    body = ('jobDetail:{jobInfo:{jobGeneralInformation:{id:1,title:"Mağaza Müdürü",jobUrl:c,qualifications:"Lyon mağazamız için. '
            'Akıcı Fransızca. Vize desteği sağlanır.",qualificationsWithHtml:"<p>Lyon mağazamız için.</p><p>Akıcı Fransızca.</p>'
            '<p>Vize desteği sağlanır.</p>",locationText:i,locations:[{countryId:l,countryName:i,cityId:l,cityName:d,'
            'jobTownLocationList:[]}],isActive:b,postingDate:bR,lastModifyDate:"26 Ekim 2026",closingDate:"' + closing + '",'
            'publishDate:bT},jobIstatistics:{totalApplication:3},jobCandidateCriteria:{languageText:["Fransızca(Okuma : İleri, '
            'Yazma : İleri, Konuşma : İleri)"]},jobCompanyInformation:{companyId:1,companyName:z}}}')
    args = f'null,false,true,"{city}","{country}","3","2026-10-26","2026-10-11T14:01","ACME Retail"'
    return f'<script>window.__NUXT__=(function(c,a,b,d,i,l,bR,bT,z){{return {{{body}}}}}({args}));</script>'


def test_kariyer_detail():
    j, why = kariyer_net.parse_detail(nuxt_detail(), "https://www.kariyer.net/is-ilani/x-1", today=TODAY)
    assert j is not None, why
    assert j.title == "Mağaza Müdürü" and j.company == "ACME Retail" and j.posted_at == "2026-10-26"
    assert j.city == "Lyon" and j.country == "FR" and j.source_type == "board"
    assert j.language_requirements == ["fr:fluent"] and j.visa_evidence == "Vize desteği sağlanır."
    j, why = kariyer_net.parse_detail(nuxt_detail(country="Türkiye"), "u", today=TODAY)
    assert j is None and why.startswith("hors France")
    j, why = kariyer_net.parse_detail(nuxt_detail(closing="01 Ekim 2026"), "u", today=TODAY)
    assert j is None and why.startswith("expirée")
    assert kariyer_net.parse_tr_date("09 Kasım 2026") == "2026-11-09"


# ------------------------------------------------------------------ ATS ------------------------
def test_lever_mapping():
    fr = {"text": "Category Lead", "country": "FR", "hostedUrl": "https://jobs.lever.co/trendyol/1",
          "createdAt": 1791484700563, "categories": {"location": "Paris", "allLocations": ["Paris"], "commitment": "Full-time"},
          "descriptionPlain": "Fluent French and English. Turkish is a plus.", "lists": []}
    j = company_ats.map_lever(fr, "Trendyol")
    assert j.city == "Paris" and j.posted_at == "2026-10-08" and j.source_type == "ats" and j.company == "Trendyol"
    assert j.language_requirements == ["tr:preferred", "fr:fluent", "en:fluent"]
    ist = dict(fr, country="TR", categories={"location": "Istanbul / Maslak"},
               descriptionPlain="Fransızca bilen, İstanbul ofisi")
    assert company_ats.map_lever(ist, "Trendyol") is None


def test_teamtailor_mapping():
    item = {"title": "Agency Supervisor", "url": "https://jobs.dfds.com/jobs/1", "date_published": "2026-10-21T10:00:00+02:00",
            "_jobposting": {"description": "<p>Anglais courant.</p>", "hiringOrganization": {"name": "DFDS France"},
                            "jobLocation": [{"address": {"addressLocality": "Marseille", "addressCountry": "FR"}}]}}
    j = company_ats.map_teamtailor(item, "DFDS France (ex-Ekol Lojistik)")
    assert j.city == "Marseille" and j.posted_at == "2026-10-21" and j.language_requirements == ["en:fluent"]
    item["_jobposting"]["jobLocation"] = [{"address": {"addressLocality": "Rotterdam", "addressCountry": "NL"}}]
    assert company_ats.map_teamtailor(item, "DFDS") is None


def test_workday_mapping():
    info = {"title": "Sales Rep", "jobDescription": "<p>Français courant</p>", "location": "France - Paris",
            "startDate": "2026-10-20", "externalUrl": "https://x/job/1", "endDate": "2099-01-01",
            "country": {"descriptor": "France", "alpha2Code": "FR"}}
    j = company_ats.map_workday(info, "Pladis")
    assert j.city == "Paris" and j.posted_at == "2026-10-20" and j.language_requirements == ["fr:fluent"]
    assert company_ats.map_workday(dict(info, country={"descriptor": "United Kingdom", "alpha2Code": "GB"}), "P") is None


def test_fetch_never_raises():
    saved = (gurbetilan.http_get, kariyer_net.http_get, company_ats.http_get, company_ats.http_post)
    boom = lambda *a, **k: (_ for _ in ()).throw(RuntimeError("réseau coupé"))
    none = lambda *a, **k: None
    try:
        for fake in (none, boom):
            gurbetilan.http_get = kariyer_net.http_get = company_ats.http_get = company_ats.http_post = fake
            assert gurbetilan.fetch({}) == [] and kariyer_net.fetch({}) == [] and company_ats.fetch({}) == []
    finally:
        gurbetilan.http_get, kariyer_net.http_get, company_ats.http_get, company_ats.http_post = saved


if __name__ == "__main__":
    failed = 0
    for name, fn in list(globals().items()):
        if name.startswith("test_") and callable(fn):
            try:
                fn()
                print(f"OK   {name}")
            except Exception as e:  # noqa: BLE001
                failed += 1
                print(f"FAIL {name} : {e!r}")
    sys.exit(1 if failed else 0)
