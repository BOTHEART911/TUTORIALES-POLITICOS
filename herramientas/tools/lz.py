"""Ayudas para grabar la zona de líderes (PERDOMO / RONALD-SUAREZ) con el mock_lz."""
import os, json
os.environ.setdefault('MOCK', 'mock_lz')
os.environ.setdefault('PRIV_REPO', '/home/claude/jhonny-perdomo')
import mock_lz as M

# Ningún número de teléfono se ve en cámara (YouTube los marca como datos personales):
# los campos de teléfono se ven con puntos y cualquier celular escrito en pantalla se tapa.
TAPAR = r"""(() => {
  const RX = /(^|[^\d])(3\d{2})[ ]?(\d{3})[ ]?(\d{4})(?!\d)/g;
  const tapar = n => { if (n.nodeValue && RX.test(n.nodeValue)) { RX.lastIndex = 0; n.nodeValue = n.nodeValue.replace(RX, '$1$2 ••• ••••'); } RX.lastIndex = 0; };
  const recorrer = r => { const w = document.createTreeWalker(r, NodeFilter.SHOW_TEXT); let n; while ((n = w.nextNode())) tapar(n); };
  const st = document.createElement('style'); st.textContent = 'input[inputmode=numeric][maxlength="10"]:not(#nr-doc):not(#lrv-doc):not([id$="-doc"]){-webkit-text-security:disc}';
  const on = () => { document.head.appendChild(st); recorrer(document.body);
    new MutationObserver(ms => ms.forEach(m => { if (m.type === 'characterData') tapar(m.target); m.addedNodes.forEach(x => x.nodeType === 3 ? tapar(x) : x.nodeType === 1 && recorrer(x)); }))
      .observe(document.body, { childList: true, subtree: true, characterData: true }); };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', on); else on();
})();"""

def entrar(g, sub='referidos'):
    """Fuera de cámara: sesión pública + pase de líder guardados y se para en la zona."""
    g.ctx.add_init_script(TAPAR)
    g.ir(); g.espera(1200)
    u = {'documento': M.YO['documento'], 'nombre': M.YO['nombre'], 'pin': M.YO['pin'], 'codigo': M.LIDER['codigo']}
    L = dict(M.LIDER, opciones=M.OPC, tkl='demo-pase')
    g.js("""([u, L]) => { const k = s => nsKey(s);
      sessionStorage.setItem(k('continuedWeb'), '1');
      localStorage.setItem(k('jp_sessions'), JSON.stringify([u])); localStorage.setItem(k('jp_active'), u.documento);
      localStorage.setItem(k('jp_lider_ses'), JSON.stringify(L)); localStorage.setItem(k('lrv_bienvenida_v1'), '1'); }""", [u, L])
    g.ir('#/lideres'); g.espera(2500)
    if sub == 'referidos':
        g.js("() => liderReferidos(getActive())"); g.espera(2500)

import rec
# En los dos formatos el teléfono de las tarjetas se ve (el líder trabaja desde el celular)
rec.FORMATOS['h']['user_agent'] = 'Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Mobile Safari/537.36'

def llamada(g, nombre, tel, ms=2600):
    """tel: no hace nada en el navegador de grabación: se muestra una vista neutra de la llamada."""
    g.js("""([n, t]) => { const d = document.createElement('div'); d.id = '__tel';
      d.innerHTML = `<div style="position:fixed;inset:0;z-index:2147483500;background:rgba(10,37,64,.88);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:14px;color:#fff;font:16px Inter,system-ui,sans-serif">
        <div style="width:96px;height:96px;border-radius:50%;background:#0063D8;display:flex;align-items:center;justify-content:center"><svg width="44" height="44" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2"/></svg></div>
        <div style="font:700 22px Sora,sans-serif">${n}</div><div style="opacity:.8">Llamando…</div></div>`;
      document.body.appendChild(d); }""", [nombre, tel])
    g.espera(ms)
    g.js("() => { const d = document.getElementById('__tel'); if (d) d.remove(); }")
