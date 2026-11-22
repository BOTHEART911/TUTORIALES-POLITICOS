"""T01 · Entra a PRIV — grabación (h = PC 16:9, v = teléfono 9:16)."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from rec import Grab

FMT = sys.argv[1]
OUT = f'/home/claude/tut/rec/T01_{FMT}'
g = Grab(FMT, OUT)
V = FMT == 'v'

INSTALAR_JS = r"""
() => {
  const e = new Event('beforeinstallprompt', { cancelable: true });
  e.prompt = () => {
    const d = document.createElement('div'); d.id = '__inst';
    d.innerHTML = `<div style="position:fixed;top:14px;right:18px;z-index:99999;width:340px;background:#fff;border-radius:12px;box-shadow:0 12px 40px rgba(10,37,64,.28);padding:18px 18px 14px;font:14px/1.4 Inter,system-ui,sans-serif;color:#1f2937">
      <div style="display:flex;gap:12px;align-items:center;margin-bottom:12px"><img src="/__assets/logo.png" style="width:40px;height:40px;border-radius:9px">
      <div><b style="font-size:15px">¿Instalar app?</b><div style="color:#5f6368">Panel privado</div></div></div>
      <div style="display:flex;justify-content:flex-end;gap:8px"><button id="__inst-no" style="border:0;background:none;color:#0063D8;font-weight:600;padding:8px 12px">Cancelar</button>
      <button id="__inst-si" style="border:0;background:#0063D8;color:#fff;font-weight:600;padding:8px 16px;border-radius:18px">Instalar</button></div></div>`;
    document.body.appendChild(d);
    d.querySelector('#__inst-si').onclick = () => { d.remove(); window.__instOk && window.__instOk({ outcome: 'accepted' }); };
  };
  e.userChoice = new Promise(r => window.__instOk = r);
  window.dispatchEvent(e);
}
"""

# ---- preparación (fuera de cámara): una segunda cuenta ya usada en este equipo
g.ir(); g.espera(1500)
g.js("""() => { const k = nsKey('continuedWeb'); sessionStorage.removeItem(k);
  saveSession({documento:'1000000002', nombre:'Diego Martínez', rol:'INVITADO', tk:'tk2', foto:'', permisos:null});
  localStorage.removeItem(ACT_KEY); }""")
g.ir('#/instalar'); g.espera(1800)
if not V: g.js(INSTALAR_JS)
g.espera(500)
g.grabar()

g.marca('s1'); g.espera(1500); g.mover('.login-title', 900); g.espera(1200)

g.marca('s2')
if V:
    g.mover('#install-aviso-txt', 800); g.espera(2500)
    g.tap('#btn-cont-web')
else:
    g.tap('#btn-install', despues=1500)
    g.tap('#__inst-si', despues=600)
    g.js("() => { sessionStorage.setItem(nsKey('continuedWeb'),'1'); go('login'); }")
g.espera(1500)

g.marca('s3')
for k in '1111': g.tap(f'.pin-key[data-key="{k}"]', ms=320, antes=60, despues=80)
g.espera(2400)

g.marca('s4')
for k in '2580': g.tap(f'.pin-key[data-key="{k}"]', ms=320, antes=60, despues=80)
g.espera(2200)

g.marca('s5')
g.mover('.appbar .who', 700); g.espera(900)
g.mover('.rol-badge', 600); g.espera(900)
g.mover('.tile[data-id="bd"]', 700); g.espera(500)
g.mover('.tile[data-id="agenda"]', 700); g.espera(500)
g.mover('.tile[data-id="mibot"]', 900); g.espera(800)

g.marca('s6')
g.tap('#avatarBox', despues=900)
g.tap('#mf-pick', despues=300)
g.page.set_input_files('#mf-file', '/home/claude/tut/assets/foto_laura.png'); g.espera(900)
g.tap('#mf-save', despues=1600)

g.marca('s7')
g.tap('.tile[data-id="bd"]', despues=2200)
g.tap('.ia-fab', despues=1200)
g.tap('.ia-send', despues=2600)
g.espera(1500)
g.tap('.ia-x', despues=700)

g.marca('s8')
g.tap('.navr-fab', despues=1200)
g.tap('.navr-it[data-r="agenda"]', despues=2200)

g.marca('s9')
g.tap('#backbtn', despues=1500)
g.tap('#btnSwap', despues=1300)
g.mover('.acc-chip[data-doc="1000000002"]', 700); g.espera(700)
g.mover('.acc-x[data-forget="1000000002"]', 600); g.espera(900)
g.tap('.acc-chip[data-doc="1000000001"] .acc-meta', despues=1300)

g.marca('s10')
g.tap('#btnOut', despues=1800)
g.espera(800)
g.fin()
print(open(OUT + '/log.json').read())
