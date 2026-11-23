"""T03 · Ficha, por confirmar y validación — grabación (h | v)."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from rec import Grab
import mock
FMT = sys.argv[1]
g = Grab(FMT, f'/home/claude/tut/rec/T03_{FMT}')
VILLA = [x for x in sorted(mock.PERSONAS, key=lambda x: x['fechaRegistro'][6:] + x['fechaRegistro'][3:5] + x['fechaRegistro'][:2], reverse=True)
         if x['municipio'] == 'Villa Ejemplo' and x['estado'] == 'ACTIVO']
SINC = [x for x in mock.PERSONAS if x['municipio'] == 'SIN CONSULTAR'][0]['documento']
g.entrar(ruta='#/bd'); g.espera(1500)
DOC = g.js("() => document.querySelector('#bd-body .bd-card').dataset.doc")
DOC2 = g.js("() => document.querySelectorAll('#bd-body .bd-card')[1].dataset.doc")
g.grabar()

g.marca('s1')
g.espera(600); g.mover(f'.bd-card[data-doc="{DOC}"] .bd-nombre', 700); g.espera(500)
g.tap(f'.bd-card[data-doc="{DOC}"] .bd-btn[data-a="detalles"]', despues=1800)

g.marca('s2')
g.mover('.tz-kpis', 800); g.espera(1600)
g.mover('.tz-line .tz-item >> nth=0', 700); g.espera(900)
g.mover('.tz-line .tz-item >> nth=2', 700); g.espera(900)
g.tap('.tz-chips .bd-chip[data-k="compromiso"]', despues=1500)
g.tap('.tz-chips .bd-chip[data-k="todos"]', despues=900)

g.marca('s3')
g.tap('.tz-tab[data-tab="datos"]', despues=1200)
g.mover('.det-list .det-row >> nth=2', 700); g.espera(700)
g.mover('.det-list .det-row >> nth=8', 900); g.espera(1400)

g.marca('s4')
g.tap('#tz-const', despues=2200)
with g.page.expect_download() as dl:
    g.tap('#tzc-dl', despues=600)
g.ver_pdf(dl.value, ms=4200)

g.marca('s5')
g.tap('#det-edit', despues=1600)
g.page.fill('#e-contacto', ''); g.escribir('#e-contacto', '3015550123', 70); g.espera(400)
g.page.fill('#e-resi', ''); g.escribir('#e-resi', 'Alme', 150); g.espera(500)
g.tap('#e-resi-list .combo-opt[data-v="Los Almendros"]', despues=500)
g.tap('#e-save', despues=2000)

g.marca('s6')
g.tap('#bd-chips .bd-chip[data-f="Sin consultar"]', despues=1000)
DOC2 = g.js("() => document.querySelector('#bd-body .bd-card').dataset.doc")
g.tap(f'.bd-card[data-doc="{DOC2}"] .bd-btn[data-a="consultar"]', despues=1000)
g.tap('#cons-marks .cons-mark[data-m="POR CONFIRMAR"]', despues=900)
g.tap('#cons-motivo .cons-mot[data-v="NO APARECE EN CENSO"]', despues=700)
g.tap('#cons-mk-save', despues=1800)
g.mover(f'.bd-card[data-doc="{DOC2}"] .bd-sello', 700); g.espera(1200)

g.marca('s7')
g.tap('#bd-chips .bd-chip[data-f="Todos"]', despues=700)
g.mover('#bd-validacion [data-val-n]', 800); g.espera(900)
g.tap('#bd-validacion', despues=300)
g.ver_mensaje(4800)

g.marca('s8')
g.tap('#bd-chips .bd-chip[data-f="Por eliminar"]', despues=1300)
g.mover('#bd-body .bd-card .bd-sello', 800); g.espera(1200)
g.tap('#bd-body .bd-card .bd-btn[data-a="eliminar"]', despues=1000)
g.escribir('#elim-clave', '246810', 120); g.espera(400)
g.tap('#elim-go', despues=1800)

g.marca('s9')
g.tap('#bd-chips .bd-chip[data-f="Todos"]', despues=900)
g.tap('#bd-body .bd-card >> nth=1 >> .bd-btn[data-a="inactivar"]', despues=1200)
g.tap('[data-yes]', despues=1600)
g.tap('#bd-chips .bd-chip[data-f="Inactivos"]', despues=1800)
g.tap('#bd-chips .bd-chip[data-f="Todos"]', despues=800)

g.marca('s10')
g.espera(2500)
g.fin()
print(open(f'/home/claude/tut/rec/T03_{FMT}/log.json').read())
