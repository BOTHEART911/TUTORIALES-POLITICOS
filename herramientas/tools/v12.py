"""T12 · Mi Bot de WhatsApp — grabación (h | v)."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from rec import Grab
FMT = sys.argv[1]
g = Grab(FMT, f'/home/claude/tut/rec/T12_{FMT}')
g.entrar(); g.espera(1500)
g.grabar()

g.marca('s1')
g.espera(400)
g.tap('.tile[data-id="mibot"]', despues=2400)
g.mover('#bot-status', 800); g.espera(1800)
g.mover('#bot-refresh', 600); g.espera(1200)

g.marca('s2')
g.tap('#bot-qr-btn', despues=2400)
g.mover('#bot-qr-img', 700); g.espera(2600)
g.mover('#bot-qr-regen', 600); g.espera(1000)
g.tap('#bot-refresh', despues=2200)
g.mover('#bot-status', 600); g.espera(1000)

g.marca('s3')
g.tap('#bot-reboot', despues=1300)
g.tap('[data-yes]', despues=1500)
g.tap('#bot-mute', despues=1300)
g.tap('[data-yes]', despues=1500)
g.mover('#bot-logout', 700); g.espera(1500)

g.marca('s4')
g.escribir('#bot-num', '573005550177', 70); g.espera(300)
g.tap('#bot-block', despues=1300)
g.tap('[data-yes]', despues=1800)
g.escribir('#bot-num', '573005550123', 50)
g.tap('#bot-clear', despues=1200)
g.tap('[data-yes]', despues=1500)

g.marca('s5')
g.mover('#bot-bl', 700); g.espera(1200)
g.tap('#bot-bl [data-unb] >> nth=0', despues=1300)
g.tap('[data-yes]', despues=1800)

g.marca('s6')
g.espera(2500)
g.fin()
