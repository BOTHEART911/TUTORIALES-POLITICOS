"""L02 · Trabaja sin señal — grabación (h | v). Zona de líderes, datos de ejemplo. Sin teléfonos en cámara."""
import sys, os, time
sys.path.insert(0, os.path.dirname(__file__))
import lz
from rec import Grab
FMT = sys.argv[1]
g = Grab(FMT, f'/home/claude/tut/rec/L02_{FMT}')
lz.entrar(g, sub='panel')
g.grabar()

g.marca('s1')
g.espera(800); g.mover('.tile[data-id="l-preparar"]', 1000); g.espera(1800); g.mover('.tile[data-id="l-pendientes"]', 900); g.espera(1500)

g.marca('s2')
g.tap('.tile[data-id="l-preparar"]', despues=2600)
g.mover('.sheet', 600); g.espera(2500)
g.tap('.sheet [data-close]', despues=900)

g.marca('s3')
g.ctx.set_offline(True); g.espera(2600)
g.mover('.sr-tira', 700); g.espera(1500)
g.mover('.tile[data-id="l-compromisos"]', 800); g.espera(1500)
g.tap('.tile[data-id="l-referidos"]', despues=2500)

g.marca('s4')
g.tap('#lr-nuevo', despues=1200)
g.escribir('#pa-doc', '1000888011', 50); g.espera(200)
g.escribir('#pa-nom', 'Nubia Esperanza Rincón', 35); g.espera(200)
g.escribir('#pa-tel', '3015550777', 50); g.espera(200)
g.escribir('#pa-resi', 'Las Pal', 120); g.espera(900)
g.tap('#pa-resi-list .combo-opt[data-v="Las Palmas"]', despues=300)
g.tap('#pa-ok', despues=1300)
for sel, v in (('#pa-doc', '1000888012'), ('#pa-nom', 'Raúl Darío Quintana'), ('#pa-tel', '3015550778')):
    g.mover(sel, 300); g.page.fill(sel, v); g.espera(250)
g.mover('#pa-resi', 300); g.page.fill('#pa-resi', 'Centro'); g.page.dispatch_event('#pa-resi', 'input'); g.espera(500)
g.tap('#pa-resi-list .combo-opt[data-v="Centro"]', despues=300)
g.tap('#pa-ok', despues=900)
g.tap('.sheet [data-close]', despues=1500)
g.tap('#backLiderBtn', despues=1500)
if not g.js("() => !!document.querySelector('#lp-grid')"):
    t0 = time.time(); g.js("() => liderPanel(getActive())"); g.espera(1200); g.cortes.append((t0, time.time()))
g.mover('.tile[data-id="l-pendientes"]', 800); g.espera(1500)

g.ctx.set_offline(False); g.js("() => window.dispatchEvent(new Event('online'))")
t0 = time.time(); g.page.wait_for_function('() => window.SINRED && SINRED.enLinea()', timeout=25000); g.espera(800); g.cortes.append((t0, time.time()))

g.marca('s5')
g.tap('.tile[data-id="l-pendientes"]', despues=2200)
g.mover('#pd-body .sr-lista', 700); g.espera(1500)

g.marca('s6')
g.tap('#pd-body [data-a="pegar"]', despues=1200)
g.escribir('#sr-pegado', '1000888101, CARMEN ROSA DÍAZ, Las Palmass\n1000777001, RAÚL ANDRÉS QUINTERO, El Prado', 28); g.espera(1500)
g.mover('#sr-previa', 700); g.espera(1800)
g.tap('#sr-pegar-ok', despues=3000)

g.marca('s7')
g.mover('#pd-body', 600, dy=0.3); g.espera(1500)
g.mover('#pd-body .sr-card--ex', 700); g.espera(1200)
g.tap('#pd-body .sr-card--ex [data-a="descartar"]', despues=1400)
if not g.js("() => !!document.querySelector('#pd-body .sr-card--cor .sr-edit')"):
    g.tap('#pd-body .sr-card--cor [data-a="editar"]', despues=1200)
if not g.js("() => !!document.querySelector('#pd-body .sr-card--cor .sr-edit')"):
    g.log.append('editar: segundo toque'); g.page.click('#pd-body .sr-card--cor [data-a="editar"]'); g.espera(900)
def toque_real(sel, despues=700):
    loc, x, y = g.mover(sel, 600)
    g.js('([x,y]) => window.__curTap && window.__curTap(x,y)', [x, y]); g.espera(120)
    g.page.click(sel); g.espera(despues)
toque_real('#pd-body .sr-card--cor .sr-edit [data-f="t"]', 200)
g.page.keyboard.type('3015550779', delay=60); g.espera(400)
toque_real('#pd-body .sr-card--cor .sr-edit .sr-sug', 700)
toque_real('#pd-body .sr-card--cor [data-a="guardarEd"]', 1500)
g.log.append('subir habilitado: %s' % g.js("() => { const b = document.querySelector('#pd-body [data-a=\"subir\"]'); return b && !b.disabled; }"))
g.marca('s8')
g.tap('#pd-body [data-a="subir"]', despues=3200)
g.tap('#backLiderBtn', despues=1500)
if not g.js("() => !!document.querySelector('#lp-grid')"):
    t0 = time.time(); g.js("() => liderPanel(getActive())"); g.espera(1200); g.cortes.append((t0, time.time()))
g.tap('.tile[data-id="l-referidos"]', despues=2500)

g.marca('s9')
g.espera(3000)
g.fin()
print(open(f'/home/claude/tut/rec/L02_{FMT}/log.json').read()[:800])
