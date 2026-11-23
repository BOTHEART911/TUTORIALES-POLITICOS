"""T05 · Registra y administra líderes — grabación (h | v)."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from rec import Grab
import mock
FMT = sys.argv[1]
g = Grab(FMT, f'/home/claude/tut/rec/T05_{FMT}')
NUEVO = [p for p in mock.PERSONAS if p['municipio'] == 'Villa Ejemplo' and not p['esLider']][3]['documento']
g.entrar(ruta='#/lideres'); g.espera(1500)
g.grabar()

g.marca('s1')
g.espera(700)
g.mover('.ld-legend', 800); g.espera(1500)
g.mover('.ld-card[data-cod="1"] .ld-refs', 800); g.espera(1200)
g.mover('.ld-card[data-cod="3"] .ld-refs', 700); g.espera(1000)
g.mover('.ld-card[data-cod="8"] .ld-refs', 700); g.espera(1000)
g.mover('.ld-card[data-cod="1"] .ld-bar-wrap', 800); g.espera(1800)

g.marca('s2')
g.escribir('#ld-q', 'Rosa', 160); g.espera(1500)
g.page.fill('#ld-q', ''); g.page.dispatch_event('#ld-q', 'input'); g.espera(600)
g.tap('#ld-clfil [data-cl="FAMILIAR"]', despues=1500)
g.tap('#ld-clfil [data-cl=""]', despues=1000)

g.marca('s3')
g.tap('.ld-card[data-cod="2"] .bd-btn[data-a="ver"]', despues=1800)
g.mover('#lf-root .lf-k-trab', 800); g.espera(1500)
g.mover('#lf-root .lf-k-nof', 700); g.espera(1500)
g.js("() => closeLayer()"); g.espera(700)

g.marca('s4')
g.tap('#ld-add', despues=1600)
g.mover('#la-cod', 700); g.espera(700)
g.escribir('#la-doc', NUEVO, 80); g.espera(300)
g.tap('#la-buscar', despues=1600)
g.escribir('#la-padrino', 'Ana', 150); g.espera(500)
g.tap('#la-padrino-list .combo-opt >> nth=0', despues=500)
g.tap('#la-clase', despues=300); g.page.select_option('#la-clase', 'SUGERIDO POR LIDER'); g.espera(700)
g.tap('#la-save', despues=2200)

g.marca('s5')
g.tap('.ld-card[data-cod="5"] .bd-btn[data-a="editar"]', despues=1800)
g.tap('#le-clase', despues=300); g.page.select_option('#le-clase', 'PROCESOS INTERNOS'); g.espera(800)
g.tap('#le-save', despues=2000)

g.marca('s6')
g.page.evaluate('() => window.scrollTo({top: 0, behavior: "smooth"})'); g.espera(500)
g.tap('#ld-tablero', despues=2600)
g.mover('#lt-body .lt-row >> nth=0', 800); g.espera(1500)
g.tap('#lt-body .lt-row >> nth=1', despues=2500)
g.js("() => closeLayer()"); g.espera(500)
g.js("() => go('lideres')"); g.espera(1500)

g.marca('s7')
g.tap('#ld-memoria', despues=1600)
g.tap('#layer [data-ver="2026-10"]', despues=2200)
with g.page.expect_download() as dl:
    g.tap('#ld-mes-pdf', despues=900)
g.ver_pdf(dl.value, ms=3500)
g.js("() => closeLayer()"); g.espera(500)

g.marca('s8')
g.tap('.ld-card[data-cod="10"] .bd-btn[data-a="eliminar"]', despues=1800)
g.mover('#le-res', 700); g.espera(1300)
g.escribir('#le-q', 'Jorge', 150); g.espera(600)
g.tap('#le-list .le-op[data-cod="2"]', despues=900)
g.escribir('#le-clave', '246810', 120); g.espera(400)
g.tap('#le-go', despues=2400)

g.marca('s9')
g.espera(2500)
g.fin()
print(open(f'/home/claude/tut/rec/T05_{FMT}/log.json').read())
