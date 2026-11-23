"""T10 · Mide la campaña — grabación (h | v)."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from rec import Grab
FMT = sys.argv[1]
g = Grab(FMT, f'/home/claude/tut/rec/T10_{FMT}')
g.entrar(ruta='#/bd'); g.espera(2200)
g.grabar()

g.marca('s1')
g.espera(400)
g.tap('#bd-dashboard', despues=2200)
g.mover('.dash-kpis', 800); g.espera(1500)
g.mover('.dbar >> nth=0', 700); g.espera(1500)
g.mover('.dbar >> nth=2', 700); g.espera(1500)

g.marca('s2')
g.tap('#dash-group .seg-b[data-g="puesto"]', despues=1500)
g.tap('#dash-int .bd-chip-int >> nth=0', despues=1800)
g.mover('#dash-xls', 600); g.espera(600)
g.mover('#dash-pdf', 600); g.espera(1200)

g.marca('s3')
g.tap('#backbtn', despues=1400)
g.tap('#bd-simulador', despues=2400)
g.mover('#sim-crono', 700); g.espera(1500)
g.mover('.sbar >> nth=0', 700); g.espera(1200)
g.tap('.sbar-toggle >> nth=0', despues=2200)
g.mover('#sim-pdf', 700); g.espera(1800)

g.marca('s4')
g.tap('#backbtn', despues=1100)
g.tap('#bd-votacion', despues=2000)
g.mover('#voto-crono', 600); g.espera(1000)
g.mover('#voto-total', 600); g.espera(1800)
g.tap('#voto-tabs .seg-b[data-t="porMesa"]', despues=1200)
g.tap('#voto-tabs .seg-b[data-t="porLider"]', despues=1600)

g.marca('s5')
g.js("() => go('home')"); g.espera(1500)
g.tap('.tile[data-id="analisis"]', despues=2400)
g.mover('.an-areas', 700); g.espera(1500)
g.mover('.an-act', 700); g.espera(1500)
g.mover('.an-alertas', 700); g.espera(1500)

g.marca('s6')
g.tap('.an-alerta >> nth=0', despues=2200)
g.mover('#an-body .an-card >> nth=0', 700); g.espera(1300)
g.js("() => document.querySelector('#an-s-limpiar').click()"); g.espera(900)
g.tap('#an-body .seg-b[data-eje="profesional"]', despues=2000)

g.marca('s7')
g.espera(2500)
g.fin()
