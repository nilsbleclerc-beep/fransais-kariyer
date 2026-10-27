#!/usr/bin/env python3
"""
Mini-serveur HTTP local autonome & haute performance pour "Fransaİş"
- Sert l'application PWA sur http://localhost:8080 (ou port suivant disponible)
- Fournit l'API /api/refresh pour rescanner les opportunités en 1-clic depuis le web
- Fournit l'API /api/status pour suivre l'avancement et les statistiques
- Boucle d'auto-refresh paramétrable en tâche de fond (défaut : toutes les 12h)
- Ouvre automatiquement le navigateur web par défaut au lancement
- 100% standard library Python (aucune dépendance tierce requise pour le serveur)
"""

import os
import sys
import json
import time
import socket
import threading
import subprocess
import webbrowser
from datetime import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler
import socketserver

# Dossier racine du projet
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE_DIR)

# État global du serveur et du scraping
SERVER_STATE = {
    "status": "idle",           # "idle" ou "running"
    "last_refresh": None,
    "last_duration_seconds": 0,
    "job_count": 0,
    "last_error": None,
    "total_refreshes": 0,
    "auto_refresh_hours": 12,
    "next_refresh_timestamp": 0
}

STATE_LOCK = threading.Lock()

def count_current_jobs():
    """Lit le nombre d'offres actuellement présentes dans le fichier JSON."""
    json_path = os.path.join(BASE_DIR, "offres_france_turquie.json")
    if os.path.exists(json_path):
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return len(data)
        except Exception:
            return 0
    return 0

# Initialisation de l'état
SERVER_STATE["job_count"] = count_current_jobs()
SERVER_STATE["last_refresh"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

def run_scraper_task(pages=4, dorks=8):
    """Exécute main.py dans un processus séparé pour ne jamais bloquer le serveur."""
    global SERVER_STATE
    start_time = time.time()
    
    with STATE_LOCK:
        if SERVER_STATE["status"] == "running":
            print("[Serveur] Un scraping est déjà en cours d'exécution.")
            return
        SERVER_STATE["status"] = "running"
        SERVER_STATE["last_error"] = None

    print(f"\n[🔄 SCRAPER] Début du rafraîchissement des offres (pages={pages}, dorks={dorks})...")
    
    try:
        # Exécution de main.py
        cmd = [sys.executable, os.path.join(BASE_DIR, "main.py"), f"--pages={pages}", f"--dorks={dorks}"]
        process = subprocess.run(cmd, cwd=BASE_DIR, capture_output=True, text=True, encoding="utf-8", errors="replace")
        
        duration = round(time.time() - start_time, 1)
        
        if process.returncode == 0:
            job_count = count_current_jobs()
            with STATE_LOCK:
                SERVER_STATE["status"] = "idle"
                SERVER_STATE["last_refresh"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                SERVER_STATE["last_duration_seconds"] = duration
                SERVER_STATE["job_count"] = job_count
                SERVER_STATE["total_refreshes"] += 1
                SERVER_STATE["next_refresh_timestamp"] = time.time() + (SERVER_STATE["auto_refresh_hours"] * 3600)
            print(f"[✅ SCRAPER] Terminé avec succès en {duration}s ! Total offres : {job_count}")
        else:
            with STATE_LOCK:
                SERVER_STATE["status"] = "idle"
                SERVER_STATE["last_error"] = process.stderr[-300:] if process.stderr else "Erreur d'exécution"
            print(f"[❌ SCRAPER] Échec avec code {process.returncode}")
            if process.stderr:
                print(process.stderr[:500])
                
    except Exception as e:
        with STATE_LOCK:
            SERVER_STATE["status"] = "idle"
            SERVER_STATE["last_error"] = str(e)
        print(f"[❌ SCRAPER] Exception inattendue : {e}")

def auto_refresh_daemon(hours):
    """Boucle d'actualisation automatique périodique en tâche de fond."""
    global SERVER_STATE
    with STATE_LOCK:
        SERVER_STATE["auto_refresh_hours"] = hours
        SERVER_STATE["next_refresh_timestamp"] = time.time() + (hours * 3600)

    print(f"[⏰ AUTO-REFRESH] Planifié toutes les {hours} heures.")
    
    while True:
        time.sleep(30) # Vérification toutes les 30 secondes
        now = time.time()
        with STATE_LOCK:
            should_run = (SERVER_STATE["status"] == "idle") and (now >= SERVER_STATE["next_refresh_timestamp"])
            
        if should_run:
            print(f"\n[⏰ AUTO-REFRESH] Déclenchement automatique programmé ({datetime.now().strftime('%H:%M:%S')})...")
            run_scraper_task()

class BilateralAppRequestHandler(SimpleHTTPRequestHandler):
    """Gestionnaire de requêtes HTTP avec support PWA et endpoints API."""

    def __init__(self, *args, **kwargs):
        # Mappage des types MIME indispensables pour les PWA
        self.extensions_map.update({
            '.json': 'application/json',
            '.webmanifest': 'application/manifest+json',
            '.js': 'application/javascript; charset=utf-8',
            '.svg': 'image/svg+xml',
            '.png': 'image/png',
            '.ico': 'image/x-icon',
            '.css': 'text/css; charset=utf-8',
            '.html': 'text/html; charset=utf-8'
        })
        super().__init__(*args, **kwargs)

    def do_GET(self):
        # Redirection de la racine vers index.html
        if self.path == '/' or self.path == '':
            self.path = '/index.html'

        # Route API : Statut du serveur
        if self.path.startswith('/api/status'):
            self.send_api_response(200, self.get_status_payload())
            return

        # Route API : Rafraîchissement GET
        if self.path.startswith('/api/refresh'):
            self.handle_refresh_request()
            return

        # Fichiers statiques normaux
        return super().do_GET()

    def do_POST(self):
        # Route API : Rafraîchissement POST
        if self.path.startswith('/api/refresh'):
            self.handle_refresh_request()
            return

        self.send_api_response(404, {"error": "Endpoint non trouvé"})

    def handle_refresh_request(self):
        """Lance le scraping si aucun n'est déjà en cours."""
        with STATE_LOCK:
            is_running = (SERVER_STATE["status"] == "running")
            
        if is_running:
            self.send_api_response(409, {
                "success": False,
                "status": "running",
                "message": "Scraping déjà en cours / Tarama devam ediyor..."
            })
            return

        # Lancement dans un thread démon
        thread = threading.Thread(target=run_scraper_task, kwargs={"pages": 4, "dorks": 8}, daemon=True)
        thread.start()

        self.send_api_response(200, {
            "success": True,
            "status": "started",
            "message": "Scraping démarré en arrière-plan / Tarama başlatıldı !"
        })

    def get_status_payload(self):
        with STATE_LOCK:
            now = time.time()
            next_sec = max(0, int(SERVER_STATE["next_refresh_timestamp"] - now))
            return {
                "status": SERVER_STATE["status"],
                "last_refresh": SERVER_STATE["last_refresh"],
                "last_duration_seconds": SERVER_STATE["last_duration_seconds"],
                "job_count": SERVER_STATE["job_count"],
                "last_error": SERVER_STATE["last_error"],
                "total_refreshes": SERVER_STATE["total_refreshes"],
                "auto_refresh_hours": SERVER_STATE["auto_refresh_hours"],
                "next_auto_refresh_in_seconds": next_sec
            }

    def send_api_response(self, status_code, data):
        payload = json.dumps(data, ensure_ascii=False).encode('utf-8')
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(payload)))
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        self.end_headers()
        self.wfile.write(payload)

    def log_message(self, format, *args):
        # Filtre les logs verbeux de requêtes statiques pour garder une console épurée
        if any(args[0].startswith(prefix) for prefix in ["GET /api", "POST /api"]):
            sys.stdout.write(f"[{datetime.now().strftime('%H:%M:%S')}] API -> {args[0]} - {args[1]}\n")
            sys.stdout.flush()

class ThreadedHTTPServer(socketserver.ThreadingMixIn, HTTPServer):
    daemon_threads = True

def find_available_port(start_port=8080, max_attempts=10):
    """Trouve un port libre si 8080 est déjà occupé."""
    for port in range(start_port, start_port + max_attempts):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(('localhost', port)) != 0:
                return port
    return start_port

def start_server(port=8080, auto_hours=12, open_browser=True):
    actual_port = find_available_port(port)
    server_address = ('', actual_port)
    httpd = ThreadedHTTPServer(server_address, BilateralAppRequestHandler)

    url = f"http://localhost:{actual_port}/index.html"
    
    print("=" * 68)
    print("🇹🇷 FRANSA İŞ & KARİYER REHBERİ — YEREL UYGULAMA SUNUCUSU 🇫🇷")
    print("=" * 68)
    print(f"  • URL d'accès direct  : {url}")
    print(f"  • Point d'entrée PWA  : http://localhost:{actual_port}/")
    print(f"  • API Statut          : http://localhost:{actual_port}/api/status")
    print(f"  • API Rafraîchissement: http://localhost:{actual_port}/api/refresh")
    print(f"  • Auto-refresh auto   : Toutes les {auto_hours} heures")
    print(f"  • Offres actuelles    : {SERVER_STATE['job_count']} offres disponibles")
    print("-" * 68)
    print("Appuyez sur [Ctrl + C] pour arrêter le serveur à tout moment.")
    print("=" * 68 + "\n")

    # Démarrage de la boucle d'auto-refresh
    if auto_hours > 0:
        auto_thread = threading.Thread(target=auto_refresh_daemon, args=(auto_hours,), daemon=True)
        auto_thread.start()

    # Ouverture automatique du navigateur après un court délai
    if open_browser:
        def open_tab():
            time.sleep(1.0)
            print(f"[🚀 NAVIGATEUR] Ouverture automatique de {url}...")
            webbrowser.open(url)
        threading.Thread(target=open_tab, daemon=True).start()

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[👋 SERVEUR] Arrêt en cours...")
        httpd.shutdown()
        print("[✓] Serveur arrêté proprement.")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Serveur d'application locale PWA & Refresh pour Fransaİş")
    parser.add_argument("--port", type=int, default=8080, help="Port d'écoute HTTP (défaut: 8080)")
    parser.add_argument("--auto-refresh-hours", type=int, default=12, help="Fréquence d'auto-refresh en heures (défaut: 12)")
    parser.add_argument("--no-browser", action="store_true", help="Ne pas ouvrir automatiquement le navigateur")
    args = parser.parse_args()

    start_server(port=args.port, auto_hours=args.auto_refresh_hours, open_browser=not args.no_browser)
