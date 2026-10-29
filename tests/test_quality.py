"""Tests du filtre qualité (pytest, ou `python tests/test_quality.py` sans pytest)."""
import datetime
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import quality  # noqa: E402
import scorer  # noqa: E402
from models import JobOpportunity  # noqa: E402

TODAY = datetime.date(2026, 10, 28)
PROFILE = {"languages": {"tr": "native", "en": "A2-B1", "fr": "A1"}, "max_age_days": 45}


class FakeResp:
    def __init__(self, status=200, text="<html>Annonce</html>", url=None, history=()):
        self.status_code, self.text, self.url, self.history = status, text, url, list(history)


def install_http(pages):
    """pages : {url: FakeResp} ; URL inconnue -> 200 générique."""
    quality._URL_CACHE.clear()
    calls = []

    def fake_get(url, **kw):
        calls.append(url)
        r = pages.get(url) or FakeResp()
        r.url = r.url or url
        return r

    quality.common.http_get = fake_get
    return calls


def job(**kw):
    base = dict(title="Poste", company="ACME", location="Lyon", url="https://ex.fr/offre/1", source="Test",
                snippet="", kind="offer", source_type="board", country="FR", city="Lyon",
                posted_at=(TODAY - datetime.timedelta(days=3)).isoformat(), description="")
    base.update(kw)
    return JobOpportunity(**base)


def run(jobs):
    return quality.filter_offers(jobs, PROFILE, today=TODAY)


def test_istanbul_fransizca_bilen_rejected():
    install_http({})
    j = job(title="Fransızca Bilen Müşteri Temsilcisi", location="İstanbul (Avr.)", city="İstanbul", country="TR",
            description="İstanbul ofisimizde çalışacak Fransızca bilen müşteri temsilcisi aranıyor.")
    kept, rej = run([j])
    assert not kept and rej[0]["reason"] == "in_turkey", rej
    # Même annonce rangée en « Fransa » mais le texte la place à İstanbul
    j2 = job(title="Fransızca Bilen Satış Temsilcisi", location="Fransa", city="", country="",
             url="https://ex.fr/offre/2", source_type="community",
             description="İstanbul ofisimizde çalışacak Fransızca bilen arkadaş arıyoruz.")
    kept, rej = run([j2])
    assert not kept and rej[0]["reason"] == "in_turkey", rej


def test_francais_courant_rejected():
    install_http({})
    j = job(title="Vendeur bilingue", description="Langues : turc et français courant exigés. Poste à Lyon.")
    kept, rej = run([j])
    assert not kept and rej[0]["reason"] == "french_level", rej
    j = job(title="Assistant", description="Required: French C1, Turkish native.", url="https://ex.fr/o/3")
    kept, rej = run([j])
    assert not kept and rej[0]["reason"] == "french_level", rej


def test_fluent_english_rejected():
    install_http({})
    j = job(title="Data Analyst", description="Turkish is a plus. Fluent English required.")
    kept, rej = run([j])
    assert not kept and rej[0]["reason"] == "english_level", rej


def test_permit_or_residence_kept_with_warning():
    """Elle s'installe en IDF : on garde, mais on avertit honnêtement (pas de rejet trop sévère)."""
    install_http({})
    permit_cases = [
        "Paris – Mantolama ustası. Aranan nitelikler: Çalışma izni bulunan.",
        "Fransa’da yasal çalışma ve oturum iznine sahip olmak (Oturum izni olmayan adayların başvurmaması rica olunur).",
        "Vendeur turcophone à Lyon. Titre de séjour valide obligatoire.",
    ]
    for i, desc in enumerate(permit_cases):
        kept, rej = run([job(title="Personel", description=desc, source_type="community", url=f"https://ex.fr/o/permit{i}")])
        assert len(kept) == 1, (desc, rej)
        assert kept[0].warnings_tr and "izni" in kept[0].warnings_tr[0], kept[0].warnings_tr
        assert kept[0].visa_evidence == "", kept[0].visa_evidence
    # Résidence à Paris demandée : simple info, elle habitera en Île-de-France
    kept, rej = run([job(title="Paris – Hostes", city="Paris",
                         description="Aranan Nitelikler: Paris veya yakın çevresinde ikamet eden Türkçe konuşabilen.",
                         url="https://ex.fr/o/resid")])
    assert len(kept) == 1, rej
    assert "Paris'e yerleşince" in kept[0].warnings_tr[0], kept[0].warnings_tr
    assert any("Île-de-France" in r for r in kept[0].match_reasons_tr), kept[0].match_reasons_tr
    # « çalışma izni sağlanır » = l'employeur fournit le permis : aucun avertissement
    kept, rej = run([job(title="Usta", description="Lyon'da şantiye. Türkçe yeterli. Çalışma izni sağlanır.",
                         url="https://ex.fr/o/permit-given")])
    assert len(kept) == 1 and not kept[0].warnings_tr, (rej, kept and kept[0].warnings_tr)


def test_past_event_rejected():
    install_http({})
    j = job(title="Paris – Fuar Organizasyonu İçin Hostes", city="Paris", posted_at="2026-10-15",
            description="Paris'te düzenlenecek fuar organizasyonumuzda 17-21 Ekim tarihleri arasında görev alacak personel.",
            url="https://ex.fr/o/fuar", source_type="community")
    kept, rej = quality.filter_offers([j], PROFILE, today=datetime.date(2026, 10, 28))
    assert not kept and rej[0]["reason"] == "event_passed", rej
    kept, rej = quality.filter_offers([j], PROFILE, today=datetime.date(2026, 10, 16))
    assert len(kept) == 1, rej


def test_turkish_negation_and_mastery():
    """« Fransızca şart değil » n'est PAS une exigence ; « Fransızca dillerine vakıf » en est une."""
    install_http({})
    ok = job(title="Garson", description="Türkçe bilen, Fransızca şart değil. Paris.", url="https://ex.fr/o/neg",
             source_type="community")
    ko = job(title="Sekreter", description="Türkçe ve Fransızca dillerine vakıf olmak.", url="https://ex.fr/o/vakif",
             source_type="community")
    kept, rej = run([ok, ko])
    assert [k.title for k in kept] == ["Garson"], (kept, rej)
    assert rej[0]["reason"] == "french_level", rej


def test_old_ats_posting_kept():
    """Un ATS ne liste que des postes ouverts : une annonce permanente ancienne n'est pas périmée."""
    install_http({})
    j = job(title="Chauffeur turcophone", description="Turc exigé. Poste à Calais.", posted_at="2025-01-10",
            url="https://ex.fr/o/ats-old")
    j.source_type = "ats"
    kept, rej = run([j])
    assert len(kept) == 1, rej


def test_turc_exige_lyon_kept_with_reason():
    install_http({})
    j = job(title="Conseiller clientèle", description="Poste basé à Lyon. Turc exigé, français débutant accepté.")
    kept, rej = run([j])
    assert len(kept) == 1, rej
    k = kept[0]
    assert any("Türkçe isteniyor" in r and "Turc exigé" in r for r in k.match_reasons_tr), k.match_reasons_tr
    assert any("Turc demandé" in r for r in k.match_reasons_fr)
    assert any("3 gün önce" in r for r in k.match_reasons_tr)
    assert k.verified_at.endswith("Z")
    assert k.visa_evidence == "" and k.visa_sponsorship == "İlanda belirtilmemiş"
    assert 0 < k.relevance_score <= 90


def test_too_old_rejected():
    install_http({})
    j = job(title="Turcophone H/F", posted_at=(TODAY - datetime.timedelta(days=60)).isoformat())
    kept, rej = run([j])
    assert not kept and rej[0]["reason"] == "too_old", rej


def test_unknown_date_needs_live_url():
    install_http({"https://ex.fr/dead": FakeResp(404)})
    ok = job(title="Turcophone H/F", posted_at="", url="https://ex.fr/live")
    dead = job(title="Turcophone H/F 2", posted_at="", url="https://ex.fr/dead")
    kept, rej = run([ok, dead])
    assert [k.url for k in kept] == ["https://ex.fr/live"]
    assert "Yayın tarihi bilinmiyor" in kept[0].match_reasons_tr
    assert rej[0]["reason"] == "url_dead"


def test_duplicates():
    install_http({})
    a = job(title="Turcophone H/F", url="https://ex.fr/offre/9?utm_source=x")
    b = job(title="Turcophone H/F", url="https://www.ex.fr/offre/9/")
    c = job(title="TURCOPHONE (H/F)", url="https://other.fr/offre/9")
    kept, rej = run([a, b, c])
    assert len(kept) == 1 and [r["reason"] for r in rej] == ["duplicate", "duplicate"], rej


def test_expired_page_rejected():
    install_http({
        "https://ex.fr/exp": FakeResp(200, "<h1>Cette offre n'est plus disponible</h1>"),
        "https://ex.fr/kald": FakeResp(200, "<p>Bu ilan yayından kaldırıldı.</p>"),
        "https://ex.fr/redir": FakeResp(200, "liste", url="https://ex.fr/", history=[object()]),
    })
    jobs = [job(title=f"Turcophone {i}", url=u) for i, u in
            enumerate(["https://ex.fr/exp", "https://ex.fr/kald", "https://ex.fr/redir"])]
    kept, rej = run(jobs)
    assert not kept and [r["reason"] for r in rej] == ["expired", "expired", "url_redirect"], rej


def test_generic_french_offer_rejected_field_job_kept():
    install_http({})
    generic = job(title="Comptable H/F", description="Cabinet à Lyon recherche un comptable.")
    # Métier de terrain : accepté sans mention du turc seulement s'il vient de la communauté turque
    field = job(title="Manutentionnaire H/F", description="Entrepôt à Lyon.", url="https://ex.fr/o/7",
                source_type="community")
    # … mais pas depuis un agrégateur : c'est alors une offre française classique (français implicite)
    field_board = job(title="Cariste H/F", description="Entrepôt à Lyon.", url="https://ex.fr/o/8")
    kept, rej = run([generic, field, field_board])
    assert [k.title for k in kept] == ["Manutentionnaire H/F"], [k.title for k in kept]
    assert [r["reason"] for r in rej] == ["no_language_fit", "no_language_fit"], rej


def test_visa_only_if_explicit():
    install_http({})
    j1 = job(title="Turcophone", description="Paris ofisimizde çalışacak Türkçe bilen eleman.")
    j2 = job(title="Turcophone 2", description="Türkçe bilen. Vize işlemleri firma tarafından karşılanır.",
             url="https://ex.fr/o/v")
    j3 = job(title="Turcophone 3", description="Turc exigé. Titre de séjour valide obligatoire.",
             url="https://ex.fr/o/w")
    kept, rej = run([j1, j2, j3])
    assert kept[0].visa_evidence == ""
    assert "Vize işlemleri" in kept[1].visa_evidence
    # Titre de séjour déjà exigé : gardée, sans fausse preuve de visa, avec un avertissement
    assert len(kept) == 3 and kept[2].visa_evidence == "" and kept[2].warnings_tr, (rej, kept[2].warnings_tr)


def test_scorer_no_substring_false_positives():
    s, tags_tr, _, _, _, fr_req, _ = scorer.analyze_job(
        "Technicien amoureux", "Fransa ofisimizde yurtdışı şubemizde coerce a1b2c3")
    assert not any("Vize" in t for t in tags_tr)
    assert not any("A1" in t for t in tags_tr)
    _, tags_tr, _, _, _, _, _ = scorer.analyze_job("Satış", "Vize desteği sağlanır, Paris")
    assert any("Vize" in t for t in tags_tr)


if __name__ == "__main__":
    tests = [(n, f) for n, f in sorted(globals().items()) if n.startswith("test_") and callable(f)]
    failed = 0
    for name, fn in tests:
        try:
            fn()
            print(f"PASS {name}")
        except Exception as e:  # noqa: BLE001
            failed += 1
            print(f"FAIL {name}: {e!r}")
    print(f"\n{len(tests) - failed}/{len(tests)} passed")
    sys.exit(1 if failed else 0)
