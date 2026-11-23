"""L01 · Mis referidos — grabación (h | v). Zona de líderes, datos de ejemplo (mock_lz)."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import lz
from rec import Grab
import mock_lz as M
FMT = sys.argv[1]
g = Grab(FMT, f'/home/claude/tut/rec/L01_{FMT}')
R = M.REFS
A, B, C = R[0], R[1], R[2]
CED = R[6]
card = lambda r: f'.rcard[data-doc="{r["documento"]}"]'

lz.entrar(g)
g.js("() => window.scrollTo(0, 0)"); g.espera(800)
g.grabar()

# s1 · introducción
g.marca('s1')
g.espera(600); g.mover('#lr-bar', 900); g.espera(1200)
g.mover(card(A), 1000); g.espera(1500); g.mover(card(B), 900); g.espera(1500); g.mover('#lr-bar', 900); g.espera(1200)

# s2 · leer la vista: fidelización + franja + ampliar
g.marca('s2')
g.mover('#lr-bar', 700); g.espera(2200)
g.mover('#lrt-open', 800); g.espera(1500)
g.tap('#lrt-open', despues=2600)
g.page.mouse.wheel(0, 300); g.espera(1500)
g.js("() => closeLayer()"); g.espera(700)

# s3 · pastillas de municipio y actividad
g.marca('s3')
g.tap('.lr-mun[data-mun="SIN CONSULTAR"]', despues=1500)
g.tap('.lr-mun[data-mun=""]', despues=900)
g.tap('#lr-act [data-act="s"]', despues=1300)
g.tap('#lr-act2 [data-i="0"]', despues=1500)
g.tap('#lr-act [data-act="s"]', despues=900)

# s4 · trazabilidad
g.marca('s4')
g.tap(card(A) + ' [data-act="traza"]', despues=2600)
g.page.mouse.wheel(0, 350); g.espera(1800)
g.tap('.sheet [data-close]', despues=800)

# s5 · llamar y marcar la intención
g.marca('s5')
g.tap(card(A) + ' [data-act="tel"]', despues=200)
lz.llamada(g, A['nombre'], '300 555 ' + A['contacto'][-4:])
g.tap(card(A) + ' [data-act="inten"]', despues=1100)
g.tap('.sheet .opt-row[data-val="Firme con el voto"]', despues=1300)
g.mover('#lr-bar', 700); g.espera(1500)

# s6 · confirmar asistencia
g.marca('s6')
g.tap(card(B) + ' [data-act="tel"]', despues=200)
lz.llamada(g, B['nombre'], '300 555 ' + B['contacto'][-4:], 2000)
g.tap(card(B) + ' [data-act="asis"]', despues=1100)
g.tap('.sheet .opt-row[data-val="Confirmada"]', despues=1400)

# s7 · el ritmo: 4 llamadas al día + buscador
g.marca('s7')
g.page.mouse.wheel(0, 700); g.espera(2200); g.page.mouse.wheel(0, 700); g.espera(1800)
g.js("() => window.scrollTo({top: 0, behavior: 'smooth'})"); g.espera(1000)
g.escribir('#lr-q', CED['nombre'].split()[0].title(), 120); g.espera(1500)

# s8 · ceder
g.marca('s8')
g.tap(card(CED) + ' [data-act="ceder"]', despues=1400)
g.escribir('#cd-lid', 'Paola', 140); g.espera(700)
g.tap('#cd-lid-list .combo-opt >> nth=0', despues=600)
g.tap('#cd-save', despues=1300)
g.tap('.sheet [data-yes]', despues=1800)
g.mover('#lr-q', 400); g.page.fill('#lr-q', ''); g.page.dispatch_event('#lr-q', 'input'); g.espera(600)

# s9 · agregar: ya es de otro líder
g.marca('s9')
g.js("() => window.scrollTo({top: 0, behavior: 'smooth'})"); g.espera(600)
g.tap('#lr-nuevo', despues=1200)
g.escribir('#nr-doc', '1000777001', 90)
g.tap('#nr-check', despues=1700)
g.mover('.nr-found', 700); g.espera(3500)

# s10 · agregar: persona nueva
g.marca('s10')
g.mover('#nr-doc', 400); g.page.fill('#nr-doc', ''); g.espera(200)
g.escribir('#nr-doc', '1000888002', 80)
g.tap('#nr-check', despues=1500)
g.escribir('#nr-nombre', 'Nubia Esperanza Rincón', 40)
g.escribir('#nr-tel', '3015550777', 50)
g.escribir('#nr-resi', 'Las Pal', 110); g.espera(800)
g.tap('#nr-resi-list .combo-opt[data-v="Las Palmas"]', despues=400)
g.tap('#nr-save', despues=1300)
g.tap('.sheet [data-yes]', despues=2500)

# s11 · validar los por confirmar
g.marca('s11')
g.js("() => window.scrollTo({top: 0, behavior: 'smooth'})"); g.espera(700)
g.tap('#lr-val [data-v="toggle"]', despues=1800)
g.mover('#lrv-lista .lrv-btns', 700); g.espera(1500)
g.tap('#lrv-lista [data-a="visto"] >> nth=0', despues=1300)
g.tap('#lrv-chk', despues=600)
g.tap('#lrv-si', despues=2200)

# s12 · cierre
g.marca('s12')
g.js("() => window.scrollTo({top: 0, behavior: 'smooth'})"); g.espera(800)
g.tap('#lr-val [data-v="toggle"]', despues=900)
g.mover('#lr-bar', 800); g.espera(2500)
g.fin()
print(open(f'/home/claude/tut/rec/L01_{FMT}/log.json').read()[:1500])
