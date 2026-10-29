"""Tests hors-ligne des sources turques (pytest, ou `python -m tests.test_sources_turkish`)."""
import datetime
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sources import company_ats, gurbetilan, iskur, kariyer_net, tr_consulates, yenibiris  # noqa: E402

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


# ------------------------------------------------------------------ Yenibiriş ------------------
def yb_card(url, title, company, location):
    return (f'<div class="row listViewRows "><div class="titleWorks"><div class="jobTitleLnk jobHoover">'
            f'<a href="{url}" class="line-clamp-1 gtmTitle" title="{title}">{title}</a></div>'
            f'<div class="jobCompanyLnk gtmCompanyName" title="{company}">{company}</div>'
            f'<div class="fs16 gtmLocation" title="{location}">{location}</div></div>'
            '<div class="orderDateTxt gtmDate"><div title="Dün">Dün</div></div></div>')


def yb_detail(locality="Paris", region="Fransa", posted="2026-10-20", valid="2026-12-20"):
    ld = ('{"@context":"http://schema.org","datePosted":"' + posted + '","description":"Garson aranıyor",'
          '"jobLocation":{"@type":"Place","address":{"@type":"PostalAddress","addressLocality":"' + locality + '",'
          '"addressRegion":"' + region + '"}},"@type":"JobPosting","title":"Garson","hiringOrganization":"Anadolu '
          'Restoran","validThrough":"' + valid + '"}')
    return (f'<html><head><script type="application/ld+json">{ld}</script></head><body><div id="adTemplateDiv">'
            '<div class="well mb0 mainInfos"><div class="mb20"><p>Paris restoranımız için garson aranıyor.</p>'
            '<p>Türkçe bilen, Fransızca şart değil.</p><p>Vize desteği sağlanır.</p></div></div></div></body></html>')


def test_yenibiris_list():
    assert yenibiris.parse_list('<div class="resultCountTxt"><span>Fransa iş ilanı bulunamamıştır.</span></div>') == []
    html = yb_card("https://www.yenibiris.com/is-ilani/garson/1", "Garson", "Anadolu Restoran", "Fransa - Paris") + \
        yb_card("/is-ilani/asci/2", "Aşçı", "X", "Fransa")
    cards = yenibiris.parse_list(html)
    assert [c["url"] for c in cards] == ["https://www.yenibiris.com/is-ilani/garson/1",
                                         "https://www.yenibiris.com/is-ilani/asci/2"]
    assert cards[0]["location"] == "Fransa - Paris" and cards[0]["company"] == "Anadolu Restoran"


def test_yenibiris_detail():
    card = {"title": "Garson", "company": "Anadolu Restoran", "location": "Fransa - Paris"}
    j, why = yenibiris.parse_detail(yb_detail(), "https://www.yenibiris.com/is-ilani/garson/1", card, today=TODAY)
    assert j is not None, why
    assert j.city == "Paris" and j.country == "FR" and j.posted_at == "2026-10-20" and j.source_type == "board"
    assert j.company == "Anadolu Restoran" and j.language_requirements == ["tr:required", "fr:none"]
    assert j.visa_evidence == "Vize desteği sağlanır."
    j, why = yenibiris.parse_detail(yb_detail(locality="İstanbul", region="Turkey"), "u", {"location": "İstanbul"},
                                    today=TODAY)
    assert j is None and why.startswith("hors France")
    j, why = yenibiris.parse_detail(yb_detail(posted="2026-06-01"), "u", card, today=TODAY)
    assert j is None and why.startswith("trop ancienne")
    j, why = yenibiris.parse_detail(yb_detail(valid="2026-10-01"), "u", card, today=TODAY)
    assert j is None and why.startswith("expirée")


# ------------------------------------------------------------------ İŞKUR ----------------------
ISKUR_FORM = """<form><input type="hidden" name="__VIEWSTATE" value="vs"/><input type="text" name="ctl04$ctlArananMetin2"/>
<select name="ctl04$ctlIl" id="ctl04_ctlIl"><option value="">--Tüm İller--</option><option value="34">İSTANBUL</option>
<option value="61">TRABZON</option></select>
<select name="ctl04$ctlCalismaYeri" id="ctl04_ctlCalismaYeri"><option value=""></option><option value="1">Yurtiçi</option>
<option value="0">Yurtdışı</option></select>
<select name="ctl04$ctlUlke" id="ctl04_ctlUlke"><option value=""></option><option value="2">ALMANYA</option>
<option value="14">FRANSA</option></select></form>"""


def iskur_row(no, title, workplace, deadline="26.11.2026"):
    p = "ctl04_ctlGridAcikIslerListeDetail_ctl02_"
    return (f'<tr><td><a id="{p}flag_{no}" href="#">{title}</a><span id="{p}ctlIsverenTurDL">Özel</span>'
            f'<span id="{p}Label9">2</span></td><td><span id="{p}ctlCalismaYeriDL">İlçe Geneli Başvuru <br> '
            f'(Çalışma Yeri: {workplace}) </span></td><td><span id="{p}ctlSonBasvuruTarihi">{deadline}</span></td></tr>')


ISKUR_DETAIL = ('<span id="ctl01_ctlIsIlanBilgileri_ctlGenelSartlar"><p>Paris\'teki restoranımızda çalışacak aşçı. '
                'Türkçe bilen. Konaklama ve vize desteği verilir.</p></span>'
                '<span id="ctl01_ctlIsIlanBilgileri_ctlGenelSartlar2"><p>En az 2 yıl deneyim.</p></span>'
                '<span id="ctl01_ctlIsIlanBilgileri_repeaterMeslek_ctl01_ctlMeslekLabel">Aşçı</span>')


def test_iskur_form_and_results():
    from bs4 import BeautifulSoup
    form = BeautifulSoup(ISKUR_FORM, "html.parser")
    assert iskur.turkish_provinces(form) == ["istanbul", "trabzon"]
    data = iskur.search_payload(form)
    assert data["ctl04$ctlCalismaYeri"] == "0" and data["ctl04$ctlUlke"] == "14"
    assert data["__EVENTTARGET"] == iskur.SEARCH_TARGET and data["__VIEWSTATE"] == "vs"
    grid = ('<table id="ctl04_ctlGridAcikIslerListeDetail"><tr><th>x</th></tr>'
            + iskur_row("00001", "Aşçı", "FRANSA / PARİS") + iskur_row("00002", "Garson", "TRABZON / ORTAHİSAR") + "</table>")
    rows = iskur.parse_results(grid)
    assert [r["ilan_no"] for r in rows] == ["00001", "00002"]
    assert rows[0]["workplace"] == "FRANSA / PARİS" and rows[0]["deadline"] == "2026-11-26" and rows[0]["positions"] == "2"


def test_iskur_detail():
    prov = ["istanbul", "trabzon"]
    row = {"ilan_no": "00001", "title": "Aşçı", "workplace": "FRANSA / PARİS", "deadline": "2026-11-26", "positions": "2"}
    j, why = iskur.parse_detail(ISKUR_DETAIL, row, prov, today=TODAY)
    assert j is not None, why
    assert j.city == "Paris" and j.country == "FR" and j.source_type == "official_api" and j.posted_at == ""
    assert j.url == "https://esube.iskur.gov.tr/Istihdam/AcikIsIlanDetay.aspx?uiID=00001"
    assert j.language_requirements == ["tr:required"] and "vize desteği" in j.visa_evidence
    assert "Son başvuru tarihi : 2026-11-26" in j.description
    j, why = iskur.parse_detail(ISKUR_DETAIL, dict(row, workplace="TRABZON / ORTAHİSAR"), prov, today=TODAY)
    assert j is None and why.startswith("hors France")
    j, why = iskur.parse_detail(ISKUR_DETAIL, dict(row, deadline="2026-10-01"), prov, today=TODAY)
    assert j is None and why.startswith("expirée")
    j, why = iskur.parse_detail(ISKUR_DETAIL, dict(row, workplace="FRANSA"), prov, today=TODAY)
    assert j.city == "France" and j.location == "France"
    assert iskur.city_title("SAINT-DENİS") == "Saint-Denis" and iskur.city_title("NICE") == "Nice"


# ------------------------------------------------------------------ Missions turques -------------
def mfa_item(id_, title, date):
    return (f'<li><a href="/Mission/ShowAnnouncement/{id_}"><span class="ks-announcement-header">{title} '
            '<!-- Başlık --></span><span class="ks-announcement-from">Paris Büyükelçiliği</span>'
            f'<span class="ks-announcement-date"><i class="fa fa-clock-o"></i> {date}</span></a></li>')


MFA_LIST = "<ul>" + mfa_item(1, "Türk Uyruklu Sözleşmeli Sekreter Sınavı Duyurusu", "20.10.2026") + \
    mfa_item(2, "Türk Uyruklu Sözleşmeli Sekreter Sınavı Sonuçları", "25.10.2026") + \
    mfa_item(3, "No: 164, 27 Ağustos 2026, İslam İşbirliği Teşkilatı Genel Sekreteri Seçimi Hk.", "27.08.2026") + \
    mfa_item(4, "Ticaret Ataşeliği Mahalli Sekreter Alım İlanı", "13.06.2025") + "</ul>"


def mfa_detail(title, date="20.10.2026"):
    return (f'<p class="lead ks-announcement-head" id="applicationHeader">{title}</p>'
            f'<span class="ks-announcement-date">{date}</span><div class="ks-announcement-content">'
            '<p>Büyükelçiliğimizde bir adet sözleşmeli sekreter istihdam edilecektir.</p>'
            '<p>Türkçe ve Fransızca dillerine hakim\nolmak, Fransa\'da oturma ya da çalışma iznine sahip olmak.</p></div>')


def test_consulates_list():
    items = tr_consulates.parse_list(MFA_LIST, "paris-be.mfa.gov.tr")
    assert len(items) == 4 and items[0]["url"] == "https://paris-be.mfa.gov.tr/Mission/ShowAnnouncement/1"
    assert items[0]["date"] == "2026-10-20" and items[0]["title"] == "Türk Uyruklu Sözleşmeli Sekreter Sınavı Duyurusu"
    assert [tr_consulates.is_recruitment_title(i["title"]) for i in items] == [True, False, False, True]
    assert not tr_consulates.is_recruitment_title("No: 301, 20 Eylül 2014, Musul Başkonsolosluğumuz Personeli Hk.")


def test_consulates_detail():
    item = {"url": "https://paris-be.mfa.gov.tr/Mission/ShowAnnouncement/1", "title": "t", "date": "2026-10-20"}
    j, why = tr_consulates.parse_detail(mfa_detail("Türk Uyruklu Sözleşmeli Sekreter Sınavı Duyurusu"), item,
                                        "T.C. Paris Büyükelçiliği", "Paris", today=TODAY)
    assert j is not None, why
    assert j.city == "Paris" and j.country == "FR" and j.posted_at == "2026-10-20" and j.source_type == "official_api"
    assert j.company == "T.C. Paris Büyükelçiliği" and j.language_requirements == ["tr:required", "fr:fluent"]
    assert "dillerine hakim olmak" in j.description  # lignes coupées recollées
    j, why = tr_consulates.parse_detail(mfa_detail("Sekreter Sınavı Sonuçları"), item, "M", "Paris", today=TODAY)
    assert j is None and why == "pas une annonce de recrutement"
    j, why = tr_consulates.parse_detail(mfa_detail("Mahalli Sekreter Alım İlanı", "13.06.2025"), item, "M", "Paris",
                                        today=TODAY)
    assert j is None and why.startswith("trop ancienne")


def test_watch_sources_never_raise():
    mods = (yenibiris, iskur, tr_consulates)
    saved = [(m.http_get, getattr(m, "http_post", None)) for m in mods]
    boom = lambda *a, **k: (_ for _ in ()).throw(RuntimeError("réseau coupé"))
    none = lambda *a, **k: None
    try:
        for fake in (none, boom):
            for m in mods:
                m.http_get = fake
                if hasattr(m, "http_post"):
                    m.http_post = fake
            assert yenibiris.fetch({}) == [] and iskur.fetch({}) == [] and tr_consulates.fetch({}) == []
    finally:
        for m, (g, p) in zip(mods, saved):
            m.http_get = g
            if p is not None:
                m.http_post = p


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
