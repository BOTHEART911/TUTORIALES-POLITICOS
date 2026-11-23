"""Grabadora de PRIV: app REAL (repo clonado) + CORE simulado (mock.py) + screencast CDP.

g = Grab('h'|'v', salida)   ->  g.page (Playwright)
g.marca('s1') marca el inicio de una escena; g.fin() cierra y guarda frames + marcas.
Acciones con cursor visible: g.tap(sel), g.escribir(sel, txt), g.espera(ms)
"""
import json, os, re, sys, time, threading, base64, functools, http.server, socketserver, urllib.parse
sys.path.insert(0, os.path.dirname(__file__))
import mock
from playwright.sync_api import sync_playwright

REPO = os.environ.get('PRIV_REPO', '/home/claude/jhonny-priv')
TUT = '/home/claude/tut'
FONTS = TUT + '/fuente/npm/package/files'
PORT = 8765

FONT_CSS = ''.join(
    f"@font-face{{font-family:'Sora';font-style:normal;font-weight:{w};font-display:block;src:url(/__fonts/sora-latin-{w}-normal.woff2) format('woff2');}}"
    for w in (500, 600, 700, 800))

CURSOR_JS = r"""
(() => {
  const st = document.createElement('style');
  st.textContent = `#__cur{position:fixed;left:0;top:0;z-index:2147483647;pointer-events:none;transition:transform var(--d,600ms) cubic-bezier(.4,0,.2,1);will-change:transform}
  #__cur.flecha svg{filter:drop-shadow(0 2px 3px rgba(0,0,0,.35))}
  #__cur.dedo i{display:block;width:46px;height:46px;margin:-23px 0 0 -23px;border-radius:50%;background:rgba(10,37,64,.28);border:3px solid rgba(255,255,255,.95);box-shadow:0 2px 8px rgba(0,0,0,.3);transition:transform .18s}
  #__cur.dedo.on i{transform:scale(.78);background:rgba(0,99,216,.45)}
  .__onda{position:fixed;z-index:2147483646;pointer-events:none;width:20px;height:20px;margin:-10px 0 0 -10px;border-radius:50%;border:3px solid #0063D8;animation:__o .55s ease-out forwards}
  @keyframes __o{to{transform:scale(3.4);opacity:0}}`;
  const pon = () => {
    if (document.getElementById('__cur')) return;
    document.head.appendChild(st);
    const c = document.createElement('div'); c.id = '__cur';
    c.className = window.__TOUCH ? 'dedo' : 'flecha';
    c.innerHTML = window.__TOUCH ? '<i></i>' : '<svg width="30" height="30" viewBox="0 0 24 24"><path d="M4 2l15 9.2-6.6 1.3 3.9 7.3-2.6 1.4-3.9-7.3L4 18.6z" fill="#fff" stroke="#0A2540" stroke-width="1.4" stroke-linejoin="round"/></svg>';
    const p = window.__CURP || [innerWidth * .6, innerHeight * .55];
    c.style.transform = `translate(${p[0]}px,${p[1]}px)`;
    document.body.appendChild(c);
  };
  window.__curMove = (x, y, ms) => { pon(); const c = document.getElementById('__cur'); c.style.setProperty('--d', (ms || 600) + 'ms'); c.style.transform = `translate(${x}px,${y}px)`; window.__CURP = [x, y]; try { sessionStorage.setItem('__curp', JSON.stringify([x, y])); } catch (e) {} };
  window.__curTap = (x, y) => { const c = document.getElementById('__cur'); if (c) { c.classList.add('on'); setTimeout(() => c.classList.remove('on'), 220); }
    const o = document.createElement('div'); o.className = '__onda'; o.style.left = x + 'px'; o.style.top = y + 'px'; document.body.appendChild(o); setTimeout(() => o.remove(), 700); };
  try { window.__CURP = JSON.parse(sessionStorage.getItem('__curp') || 'null'); } catch (e) {}
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', pon); else pon();
})();
"""

FORMATOS = {
    # horizontal: PC 1280x720 css a 2x ; vertical: teléfono 390x844 a 3x
    'h': dict(viewport={'width': 1280, 'height': 720}, device_scale_factor=2, is_mobile=False, has_touch=False),
    'v': dict(viewport={'width': 390, 'height': 844}, device_scale_factor=3, is_mobile=True, has_touch=True,
              user_agent='Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1'),
}


class _H(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
    def end_headers(self):
        self.send_header('Cache-Control', 'no-store'); super().end_headers()


def _servidor():
    h = functools.partial(_H, directory=REPO)
    class S(socketserver.ThreadingTCPServer):
        allow_reuse_address = True
        daemon_threads = True
    global PORT
    s = S(('127.0.0.1', 0), h); PORT = s.server_address[1]
    threading.Thread(target=s.serve_forever, daemon=True).start()
    return s


def _marca_js():
    s = open(REPO + '/js/marca.js', encoding='utf-8').read()
    rep = {'CANDIDATO': 'Candidato Ejemplo', 'PN_CANDIDATO': 'Candidato', 'MUNICIPIO': 'Villa Ejemplo',
           'DEPARTAMENTO': 'Departamento Ejemplo', 'LEMA': 'Tu campaña', 'EQUIPO': 'Equipo de ejemplo',
           'COLOR': '#0063D8', 'COLOR_700': '#004FAD', 'APP_ICON': '/__assets/logo.png',
           'APP_BANNER': '/__assets/logo.png', 'IMG_BASE': '/__assets/', 'STORAGE_NS': 'demo'}
    for k, v in rep.items():
        s = re.sub(r"(\b%s\s*:\s*)'[^']*'" % k, lambda m: m.group(1) + "'" + v + "'", s)
    s = re.sub(r"(API_URL\s*:\s*)'[^']*'", r"\1'https://script.google.com/macros/s/DEMO/exec'", s)
    return s


class Grab:
    def __init__(self, fmt, salida, lento=0):
        self.fmt, self.salida = fmt, salida
        os.makedirs(salida + '/frames', exist_ok=True)
        for f in os.listdir(salida + '/frames'): os.remove(os.path.join(salida, 'frames', f))
        self.frames, self.marcas, self.log, self.cur = [], [], [], []
        self.srv = _servidor()
        self.pw = sync_playwright().start()
        self.br = self.pw.chromium.launch(args=['--force-color-profile=srgb', '--font-render-hinting=none'])
        self.ctx = self.br.new_context(service_workers='block', locale='es-CO', timezone_id='America/Bogota', **FORMATOS[fmt])
        try: self.ctx.grant_permissions(['clipboard-read', 'clipboard-write'], origin=f'http://127.0.0.1:{PORT}')
        except Exception: pass
        self.ctx.add_init_script('window.__TOUCH=%s;' % ('true' if fmt == 'v' else 'false') + CURSOR_JS)
        self.ctx.route('**/*', self._ruta)
        self.page = self.ctx.new_page()
        self.page.on('console', lambda m: self.log.append(f'{m.type}: {m.text}') if m.type in ('error', 'warning') else None)
        self.page.on('pageerror', lambda e: self.log.append(f'PAGEERROR: {e}'))
        self.cdp = None

    # ---------- red ----------
    def _ruta(self, route):
        u = route.request.url
        pu = urllib.parse.urlparse(u)
        try:
            if 'script.google.com' in pu.netloc:
                q = dict(urllib.parse.parse_qsl(pu.query))
                cuerpo = {}
                if route.request.method == 'POST' and route.request.post_data:
                    try: cuerpo = json.loads(route.request.post_data)
                    except Exception: cuerpo = {}
                acc = q.pop('action', '')
                r = mock.responder(acc, q, cuerpo)
                if acc != 'app.marca': r = {'ok': True, 'data': r, 'v': '2026.11.22.demo'}
                time.sleep(0.25)
                return route.fulfill(status=200, content_type='application/json', body=json.dumps(r))
            if pu.path.startswith('/__fonts/'):
                return route.fulfill(path=FONTS + '/' + os.path.basename(pu.path), content_type='font/woff2')
            if 'fonts.googleapis.com' in pu.netloc:
                return route.fulfill(status=200, content_type='text/css', body=FONT_CSS)
            if pu.path.startswith('/__assets/'):
                return route.fulfill(path=TUT + '/assets/' + os.path.basename(pu.path))
            if pu.netloc.startswith('127.0.0.1'):
                if pu.path.endswith('/js/marca.js'):
                    return route.fulfill(status=200, content_type='application/javascript', body=_marca_js())
                if pu.path.endswith('/img/logo.png') or pu.path.endswith('/img/logo-192.png'):
                    return route.fulfill(path=TUT + '/assets/logo.png')
                return route.continue_()
            return route.abort()
        except Exception as e:
            self.log.append(f'RUTA {u}: {e}')
            try: route.abort()
            except Exception: pass

    # ---------- captura ----------
    def _frame(self, ev):
        ts = ev['metadata'].get('timestamp', time.time())
        n = len(self.frames)
        p = f"{self.salida}/frames/{n:06d}.jpg"
        with open(p, 'wb') as f: f.write(base64.b64decode(ev['data']))
        self.frames.append((ts, p))
        try: self.cdp.send('Page.screencastFrameAck', {'sessionId': ev['sessionId']})
        except Exception: pass

    def grabar(self):
        self.cdp = self.ctx.new_cdp_session(self.page)
        self.cdp.on('Page.screencastFrame', self._frame)
        vp = FORMATOS[self.fmt]['viewport']; dpr = FORMATOS[self.fmt]['device_scale_factor']
        self.cdp.send('Page.startScreencast', {'format': 'jpeg', 'quality': 92, 'maxWidth': vp['width'] * dpr, 'maxHeight': vp['height'] * dpr, 'everyNthFrame': 1})
        self.espera(300)

    def marca(self, nombre):
        self.marcas.append((nombre, time.time()))

    def fin(self):
        self.espera(400)
        self.marcas.append(('__fin', time.time()))
        try: self.cdp.send('Page.stopScreencast')
        except Exception: pass
        json.dump({'frames': self.frames, 'marcas': self.marcas, 'fmt': self.fmt, 'cur': self.cur, 'vp': FORMATOS[self.fmt]['viewport']}, open(self.salida + '/rec.json', 'w'))
        json.dump({'log': self.log, 'faltan': sorted(set(mock.FALTAN))}, open(self.salida + '/log.json', 'w'), ensure_ascii=False, indent=1)
        self.br.close(); self.pw.stop(); self.srv.shutdown(); self.srv.server_close()

    # ---------- acciones ----------
    def ir(self, ruta=''):
        self.page.goto(f'http://127.0.0.1:{PORT}/index.html' + ruta)

    def espera(self, ms):
        self.page.wait_for_timeout(ms)

    def caja(self, sel):
        loc = self.page.locator(sel + ' >> visible=true').first
        try: loc.wait_for(state='visible', timeout=15000)
        except Exception:
            self.page.screenshot(path=self.salida + '/fallo.png'); raise
        movio = loc.evaluate('''el => { const r = el.getBoundingClientRect(), H = innerHeight;
            if (r.top >= 96 && r.bottom <= H - 12) return false;
            el.scrollIntoView({ block: 'center', behavior: 'smooth' }); return true; }''')
        if movio: self.espera(700)
        b = loc.bounding_box()
        return loc, b

    def mover(self, sel, ms=650, dx=0.5, dy=0.5):
        loc, b = self.caja(sel)
        x, y = b['x'] + b['width'] * dx, b['y'] + b['height'] * dy
        self.page.evaluate('([x,y,ms]) => window.__curMove && window.__curMove(x,y,ms)', [x, y, ms])
        self.cur.append((time.time(), x, y))
        self.espera(ms + 120)
        return loc, x, y

    def tap(self, sel, ms=650, antes=250, despues=500):
        loc, x, y = self.mover(sel, ms)
        self.espera(antes)
        self.page.evaluate('([x,y]) => window.__curTap && window.__curTap(x,y)', [x, y])
        self.espera(140)
        loc.click(force=True)
        self.espera(despues)

    def escribir(self, sel, txt, ms_letra=70):
        self.tap(sel, despues=200)
        self.page.keyboard.type(txt, delay=ms_letra)

    def js(self, code, arg=None):
        return self.page.evaluate(code, arg)

    def entrar(self, pin='2580', ruta='#/home'):
        """Fuera de cámara: deja la sesión abierta y se para en la ruta."""
        self.ir(); self.espera(1200)
        self.js("() => { sessionStorage.setItem(nsKey('continuedWeb'),'1'); go('login'); }"); self.espera(800)
        for k in pin: self.page.locator(f'.pin-key[data-key="{k}"]').click()
        self.page.wait_for_selector('.appbar', timeout=15000); self.espera(1500)
        if ruta and ruta != '#/home':
            self.js(f"() => go('{ruta[2:]}')"); self.espera(2500)
