"""Tests hors-ligne des collecteurs officiels/agrégateurs (pytest, ou `python -m tests.test_sources_official`)."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sources import adzuna, eures, france_travail, jooble  # noqa: E402

ENV_KEYS = ["FT_CLIENT_ID", "FT_CLIENT_SECRET", "ADZUNA_APP_ID", "ADZUNA_APP_KEY", "JOOBLE_KEY"]


class FakeResp:
    def __init__(self, status, payload=None, headers=None):
        self.status_code, self._payload, self.headers = status, payload, headers or {}

    def json(self):
        return self._payload


FT_SAMPLE = {"resultats": [
    {"id": "198ABCD", "intitule": "Conseiller clientèle turcophone (H/F)",
     "description": "Vous répondez aux clients en turc et en français. Anglais apprécié.",
     "dateCreation": "2026-10-20T09:12:00.000Z", "dateActualisation": "2026-10-21T08:00:00.000Z",
     "lieuTravail": {"libelle": "69 - Lyon 3e Arrondissement", "codePostal": "69003", "commune": "69383"},
     "entreprise": {"nom": "ACME CALL"}, "typeContrat": "CDI", "typeContratLibelle": "Contrat à durée indéterminée",
     "salaire": {"libelle": "Mensuel de 1900.0 Euros sur 12 mois"},
     "langues": [{"libelle": "Turc", "exigence": "E"}, {"libelle": "Français", "exigence": "S"}],
     "origineOffre": {"origine": "1", "urlOrigine": "https://candidat.francetravail.fr/offres/recherche/detail/198ABCD"}},
    {"id": "198ZZZ", "intitule": "Chauffeur international", "description": "Poste en Allemagne",
     "dateCreation": "2026-10-19T09:12:00.000Z", "lieuTravail": {"libelle": "Allemagne"}},
]}

ADZUNA_SAMPLE = {"count": 1, "results": [
    {"id": "4567", "title": "Assistant commercial <strong>turcophone</strong>",
     "description": "Société d'import-export recherche un profil parlant <strong>turc</strong>…",
     "created": "2026-10-25T10:00:00Z", "redirect_url": "https://www.adzuna.fr/details/4567",
     "company": {"display_name": "Import SARL"},
     "location": {"display_name": "Paris, Ile-de-France", "area": ["France", "Ile-de-France", "Paris"]},
     "salary_min": 24000, "salary_max": 28000, "contract_type": "permanent", "contract_time": "full_time",
     "category": {"label": "Emplois Commercial"}}]}

JOOBLE_SAMPLE = {"totalCount": 1, "jobs": [
    {"id": -123456789, "title": "Agent d'accueil bilingue turc", "location": "Strasbourg, Grand Est",
     "snippet": "&nbsp;...maîtrise du <b>turc</b> indispensable...", "salary": "12 € par heure",
     "source": "hellowork.com", "type": "CDD", "link": "https://jooble.org/desc/-123456789",
     "company": "Hôtel Rhin", "updated": "2026-10-24T00:00:00.0000000"}]}


def _clear_env():
    saved = {k: os.environ.pop(k, None) for k in ENV_KEYS}
    return saved


def _restore_env(saved):
    for k, v in saved.items():
        if v is not None:
            os.environ[k] = v


def test_no_keys_returns_empty():
    saved = _clear_env()
    try:
        for mod in (france_travail, eures, adzuna, jooble):
            assert mod.fetch({}) == [], mod.__name__
    finally:
        _restore_env(saved)


def test_france_travail_mapping():
    jobs = [j for j in (france_travail.map_offer(o) for o in FT_SAMPLE["resultats"]) if j]
    assert len(jobs) == 1  # l'offre en Allemagne est écartée
    j = jobs[0]
    assert j.title == j.title_fr == "Conseiller clientèle turcophone (H/F)"
    assert j.company == "ACME CALL" and j.city == "Lyon 3e Arrondissement" and j.country == "FR"
    assert j.posted_at == "2026-10-20" and j.source_type == "official_api" and j.kind == "offer"
    assert j.language_requirements == ["tr:required", "fr:preferred"]
    assert j.url.endswith("/198ABCD") and "turc" in j.description and len(j.snippet) <= 301
    assert "Contrat à durée indéterminée" in j.snippet and j.discovered_at


def test_france_travail_fetch_paginates(monkeypatch=None):
    calls = []

    def fake_post(url, **kw):
        return FakeResp(200, {"access_token": "tok"})

    def fake_get(url, params=None, headers=None, **kw):
        calls.append(params)
        if params["motsCles"] == "turc":
            return FakeResp(206, FT_SAMPLE, {"Content-Range": "offres 0-149/2"})
        return FakeResp(204)

    orig = france_travail.http_post, france_travail.http_get
    france_travail.http_post, france_travail.http_get = fake_post, fake_get
    os.environ["FT_CLIENT_ID"], os.environ["FT_CLIENT_SECRET"] = "id", "secret"
    try:
        jobs = france_travail.fetch({})
    finally:
        france_travail.http_post, france_travail.http_get = orig
        os.environ.pop("FT_CLIENT_ID"), os.environ.pop("FT_CLIENT_SECRET")
    assert len(jobs) == 1
    assert [c["motsCles"] for c in calls] == ["turc", "turcophone", "turque"]
    assert all(c["publieeDepuis"] == 31 and c["range"] == "0-149" for c in calls)


def test_adzuna_mapping():
    j = adzuna.map_result(ADZUNA_SAMPLE["results"][0])
    assert j.title == "Assistant commercial turcophone" and j.company == "Import SARL"
    assert j.city == "Paris" and j.country == "FR" and j.posted_at == "2026-10-25"
    assert j.source_type == "board" and j.url == "https://www.adzuna.fr/details/4567"
    assert "24000–28000" in j.snippet and "<strong>" not in j.description


def test_jooble_mapping():
    j = jooble.map_job(JOOBLE_SAMPLE["jobs"][0])
    assert j.title == "Agent d'accueil bilingue turc" and j.company == "Hôtel Rhin"
    assert j.city == "Strasbourg" and j.posted_at == "2026-10-24" and j.source_type == "board"
    assert "<b>" not in j.description and "turc" in j.description and j.country == "FR"


if __name__ == "__main__":
    failed = 0
    for name, fn in list(globals().items()):
        if name.startswith("test_") and callable(fn):
            try:
                fn()
                print(f"OK   {name}")
            except AssertionError as e:
                failed += 1
                print(f"FAIL {name} : {e!r}")
    sys.exit(1 if failed else 0)
