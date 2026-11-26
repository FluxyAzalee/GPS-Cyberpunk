"""Petit serveur local pour le GPS néon.

- sert les fichiers de ce dossier (comme `python -m http.server`)
- relaie les données des bus Sitac (le navigateur les bloque sinon : CORS)

Lancer :   python serveur.py
Ouvrir :   http://localhost:8000
"""
import http.server
import urllib.parse
import urllib.request

ADRESSES = {
    'rt': 'https://zenbus.net/gtfs/rt/poll.proto?dataset=sitac-calais-rt&src=true',
    'gtfs': 'https://zenbus.net/gtfs/static/download.zip?dataset=sitac-calais-rt&src=true',
}


class Gestionnaire(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        chemin = urllib.parse.urlparse(self.path)
        if chemin.path != '/proxy-bus':
            super().do_GET()
            return

        type_demande = urllib.parse.parse_qs(chemin.query).get('type', ['rt'])[0]
        adresse = ADRESSES.get(type_demande, ADRESSES['rt'])
        try:
            requete = urllib.request.Request(adresse, headers={'User-Agent': 'gps-neon'})
            with urllib.request.urlopen(requete, timeout=20) as reponse:
                contenu = reponse.read()
            self.send_response(200)
            self.send_header('Content-Type', 'application/octet-stream')
            self.send_header('Content-Length', str(len(contenu)))
            self.end_headers()
            self.wfile.write(contenu)
        except Exception as erreur:
            self.send_error(502, 'Relais impossible : ' + str(erreur))


if __name__ == '__main__':
    print('GPS néon sur http://localhost:8000  (Ctrl+C pour arrêter)')
    http.server.ThreadingHTTPServer(('localhost', 8000), Gestionnaire).serve_forever()
