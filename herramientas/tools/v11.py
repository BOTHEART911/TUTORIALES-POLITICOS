"""T11 · Usuarios, invitados y configuración — grabación (h | v)."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from rec import Grab
FMT = sys.argv[1]
g = Grab(FMT, f'/home/claude/tut/rec/T11_{FMT}')
g.entrar(ruta='#/config'); g.espera(2000)
g.grabar()

g.marca('s1')
g.espera(400); g.mover('.cfg-tabs', 900); g.espera(1500)
g.mover('.cfg-acc-h >> nth=3', 600); g.espera(600)
g.tap('.cfg-acc-h >> nth=0', despues=1500)
g.tap('#cf-cp-APP_PUBLICA_URL', despues=300)
g.ver_mensaje(3200)

g.marca('s2')
g.tap('.cfg-tab[data-t="plantillas"]', despues=1100)
g.tap('.cfg-acc-h >> nth=0', despues=1200)
g.mover('#cf-tpl-0', 600); g.espera(800)
g.tap('#cf-body [data-prev="0"]', despues=2600)

g.marca('s3')
g.tap('.cfg-tab[data-t="usuarios"]', despues=1100)
g.tap('.cfg-acc-h >> nth=0', despues=1300)
g.mover('.cfg-row >> nth=1', 600); g.espera(1000)
g.tap('#cf-us-add', despues=1200)
g.escribir('#cf-us-d', '1000000077', 40)
g.escribir('#cf-us-n', 'Natalia Ruiz Peña', 35)
g.escribir('#cf-us-w', '3005550177', 40); g.espera(200)
g.mover('#cf-us-r', 600); g.page.select_option('#cf-us-r', 'INVITADO'); g.espera(1400)
g.escribir('#cf-us-p', '4826', 120); g.espera(400)

g.marca('s4')
g.tap('.perm-vchk[data-v="bd"]', despues=800)
g.tap('#cf-us-perm [data-k="bd.agregar"]', despues=350)
g.tap('#cf-us-perm [data-k="bd.detalles"]', despues=350)
g.tap('#cf-us-perm [data-k="bd.excel"]', despues=500)
g.tap('.perm-vchk[data-v="ag"]', despues=800)
g.tap('#cf-us-perm [data-x="exportar"]', despues=1200)
g.tap('#cf-us-save', despues=1800)

g.marca('s5')
g.tap('#cf-body [data-usbien="1000000077"]', despues=1300)
g.tap('#cf-bien-wa', despues=300)
g.ver_mensaje(3600)

g.marca('s6')
g.js("() => { sessionStorage.setItem(nsKey('continuedWeb'),'1'); go('login'); }"); g.espera(1500)
for k in '4826':
    g.tap(f'.pin-key[data-key="{k}"]', ms=300, antes=100, despues=250)
g.espera(2800)
g.mover('.tile >> nth=0', 700); g.espera(1500)
g.tap('.tile[data-id="bd"]', despues=2500)

g.marca('s7')
g.espera(2500)
g.fin()
