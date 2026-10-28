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


def test_requires_local_status_rejected():
    install_http({})
    cases = [
        "Paris – Mantolama ustası. Aranan nitelikler: Çalışma izni bulunan.",
        "Fransa’da yasal çalışma ve oturum iznine sahip olmak (Oturum izni olmayan adayların başvurmaması rica olunur).",
        "Aranan Nitelikler: Paris veya yakın çevresinde ikamet eden Türkçe konuşabilen.",
        "Vendeur turcophone à Lyon. Titre de séjour valide obligatoire.",
    ]
    for i, desc in enumerate(cases):
        kept, rej = run([job(title="Personel", description=desc, url=f"https://ex.fr/o/local{i}")])
        assert not kept and rej[0]["reason"] == "requires_local_status", (desc, rej)
    # « çalışma izni sağlanır » = l'employeur fournit le permis : ne doit PAS être rejeté
    kept, rej = run([job(title="Usta", description="Lyon'da şantiye. Türkçe yeterli. Çalışma izni sağlanır.",
                         url="https://ex.fr/o/permit-given")])
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
    field = job(title="Manutentionnaire H/F", description="Entrepôt à Lyon.", url="https://ex.fr/o/7")
    kept, rej = run([generic, field])
    assert [k.title for k in kept] == ["Manutentionnaire H/F"]
    assert rej[0]["reason"] == "no_language_fit"


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
    # Titre de séjour déjà exigé : inaccessible depuis la Turquie → rejetée, pas seulement signalée
    assert len(kept) == 2 and rej[0]["reason"] == "requires_local_status", rej


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
