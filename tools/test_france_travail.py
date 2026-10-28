"""
Test local des identifiants France Travail (API Offres d'emploi v2).

Demande l'identifiant client et la clé secrète sans les afficher, tente d'obtenir un jeton,
puis fait une recherche « turc ». N'affiche jamais les identifiants.

    python tools/test_france_travail.py
"""
import getpass
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sources import france_travail  # noqa: E402


def main():
    client_id = getpass.getpass("Identifiant client France Travail (masqué) : ").strip()
    client_secret = getpass.getpass("Clé secrète France Travail (masquée) : ").strip()
    print(f"Longueurs saisies : identifiant {len(client_id)} caractères, clé {len(client_secret)} caractères")
    if client_id.startswith("PAR_"):
        print("Format d'identifiant attendu (commence par PAR_) : OK")
    else:
        print("⚠ L'identifiant client France Travail commence normalement par « PAR_ » : vérifie la valeur copiée")

    token = france_travail.get_token(client_id, client_secret)
    if not token:
        print("\n❌ Jeton refusé. Les identifiants ne sont pas acceptés par France Travail "
              "(ou l'application n'est pas encore active / pas abonnée à « Offres d'emploi v2 »).")
        sys.exit(1)
    print("\n✅ Jeton obtenu : les identifiants sont bons.")
    offres = france_travail._search(token, "turc")
    print(f"Recherche « turc » : {len(offres)} offre(s) renvoyée(s) par l'API.")
    print("→ Si ce test passe mais pas le robot GitHub, ressaisis les mêmes valeurs avec "
          "« gh secret set FT_CLIENT_ID » et « gh secret set FT_CLIENT_SECRET ».")


if __name__ == "__main__":
    main()
