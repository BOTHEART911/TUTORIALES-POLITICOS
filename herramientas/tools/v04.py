"""T04 · En bloque y sin señal — grabación (h | v)."""
import sys, os, openpyxl, html
sys.path.insert(0, os.path.dirname(__file__))
from rec import Grab
FMT = sys.argv[1]
g = Grab(FMT, f'/home/claude/tut/rec/T04_{FMT}')
XLSX = '/home/claude/tut/assets/puestos_diligenciado.xlsx'
filas = [[('' if v is None else str(v)) for v in r] for r in openpyxl.load_workbook(XLSX).active.iter_rows(values_only=True)]
tabla = ''.join('<tr><th>%d</th>%s</tr>' % (i + 1, ''.join(('<td class=h>%s</td>' if i == 0 else '<td>%s</td>') % html.escape(c) for c in r)) for i, r in enumerate(filas))
HOJA_JS = """(t) => { const d = document.createElement('div'); d.id = '__hoja';
  d.innerHTML = `<style>#__hoja{position:fixed;inset:0;z-index:2147483500;background:rgba(10,37,64,.55);display:flex;align-items:center;justify-content:center;padding:14px}
  #__hoja .w{background:#fff;border-radius:12px;box-shadow:0 20px 60px rgba(0,0,0,.35);overflow:auto;max-width:96vw;max-height:92vh;font:12px Inter,system-ui}
  #__hoja .b{background:#0A2540;color:#fff;padding:9px 14px;font-weight:700;font-size:13px}
  #__hoja table{border-collapse:collapse}#__hoja td,#__hoja th{border:1px solid #d9dee6;padding:5px 8px;white-space:nowrap}
  #__hoja th{background:#f1f3f6;color:#6b7280;font-weight:600}#__hoja td.h{background:#e8f0fe;font-weight:700;color:#0A2540}
  #__hoja .c th{background:#f1f3f6}</style>
  <div class="w"><div class="b">PLANTILLA_CARGA_PUESTOS.xlsx · diligenciada</div><table><tr class="c"><th></th>${['A','B','C','D','E','F','G'].map(x=>'<th>'+x+'</th>').join('')}</tr>${t}</table></div>`;
  document.body.appendChild(d); }"""

g.entrar(ruta='#/bd'); g.espera(1500)
g.grabar()

g.marca('s1')
g.espera(800); g.mover('#bd-subir', 900); g.espera(600); g.mover('#bd-pend', 800); g.espera(1200)

g.marca('s2')
g.tap('#bd-subir', despues=1000)
with g.page.expect_download():
    g.tap('#lote-tpl', despues=900)
g.js(HOJA_JS, tabla); g.espera(7000)
g.js("() => document.getElementById('__hoja').remove()"); g.espera(400)

g.marca('s3')
g.tap('#lote-open', despues=1000)
g.tap('#lote-pick', despues=300)
g.page.set_input_files('#lote-file', XLSX); g.espera(1800)
g.mover('.lote-kpis', 700); g.espera(1500)
g.mover('.lote-tabla', 700); g.espera(1500)

g.marca('s4')
g.tap('#lote-go', despues=2500)
g.mover('#lote-bk', 700); g.espera(1500)
g.tap('[data-close]', despues=1000)

g.marca('s5')
D1 = g.js("() => document.querySelectorAll('#bd-body .bd-card')[1].dataset.doc")
D2 = g.js("() => document.querySelectorAll('#bd-body .bd-card')[4].dataset.doc")
g.tap(f'.bd-card[data-doc="{D1}"] .bd-btn[data-a="reasignar"]', despues=1000)
g.escribir('#reasg-lid', 'Cami', 150); g.espera(600)
g.tap('#reasg-lid-list .combo-opt >> nth=0', despues=500)
g.tap('#reasg-save', despues=1600)
g.tap(f'.bd-card[data-doc="{D2}"] .bd-btn[data-a="reasignar"]', despues=1100)
g.tap('#reasg-ult', despues=1700)

g.marca('s6')
g.page.evaluate('() => window.scrollTo({top: 0, behavior: "smooth"})'); g.espera(600)
g.js('() => PEND.barrios()'); g.espera(300)
g.ctx.set_offline(True); g.espera(2500)
g.tap('[data-sr="tira"]', despues=1500)
g.mover('.sr-ayuda', 700); g.espera(2500)
g.tap('.sheet button:has-text("Entendido")', despues=800)

g.marca('s7')
g.tap('#bd-add', despues=1000)
g.escribir('#pa-doc', '1000008811', 40); g.espera(200)
g.escribir('#pa-nom', 'Nubia Esperanza Rincón', 30); g.espera(200)
g.escribir('#pa-tel', '3015550777', 40); g.espera(200)
g.escribir('#pa-resi', 'Las Pal', 120); g.espera(900)
g.tap('#pa-resi-list .combo-opt[data-v="Las Palmas"]', despues=300)
g.tap('#pa-ok', despues=1200)
for sel, v in (('#pa-doc', '1000008812'), ('#pa-nom', 'Raúl Andrés Quintero'), ('#pa-tel', '3015550778')):
    g.mover(sel, 300); g.page.fill(sel, v); g.espera(250)
g.mover('#pa-resi', 300); g.page.fill('#pa-resi', 'Centro'); g.page.dispatch_event('#pa-resi', 'input'); g.espera(500)
g.tap('#pa-resi-list .combo-opt[data-v="Centro"]', despues=300)
g.tap('#pa-ok', despues=600)
g.pausa(2000)
g.tap('.sheet button:has-text("Terminar")', despues=900)
g.mover('#bd-pend', 700); g.espera(800)

g.ctx.set_offline(False); g.js("() => window.dispatchEvent(new Event('online'))"); g.espera(2500)

g.marca('s8')
g.mover('.sr-tira', 600); g.espera(900)
g.pausa(6000)
t0 = __import__('time').time(); g.page.wait_for_function('() => window.SINRED && SINRED.enLinea()', timeout=20000); g.cortes.append((t0, __import__('time').time()))
g.tap('#bd-pend', despues=1500)
if not g.js("() => !!document.getElementById('pd-body')"):
    t0 = __import__('time').time(); g.js("() => { closeLayer(); PEND.bdPendientes(getActive()); }"); g.espera(1500); g.cortes.append((t0, __import__('time').time()))
g.log.append('pd-body: %s' % g.js("() => !!document.getElementById('pd-body')"))
g.tap('#pd-body [data-a="revisar"]', despues=2200)
g.page.select_option('#pd-lider', '2'); g.mover('#pd-lider', 600); g.espera(800)
g.tap('#pd-body [data-a="subir"]', despues=2200)
g.tap('#backbtn', despues=1800)

g.marca('s9')
g.tap('#bd-pdf', despues=1300)
g.mover('#bd-colpick', 700); g.espera(1200)
with g.page.expect_download() as dl:
    g.tap('#bd-colgo', despues=900)
g.ver_pdf(dl.value, ms=3800)

g.marca('s10')
g.espera(2500)
g.fin()
print(open(f'/home/claude/tut/rec/T04_{FMT}/log.json').read())
