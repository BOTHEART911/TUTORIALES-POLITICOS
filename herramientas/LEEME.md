# Herramientas de grabación de los tutoriales

Graban la app REAL (repo PRIV clonado) con un CORE simulado y datos de ejemplo (campaña ficticia «Candidato Ejemplo»). Nunca usan datos reales.

Copiar a `/home/claude/tut` (tools/, build/, assets/) y además:
- `pip install edge-tts brotli` · fuente Sora: `npm pack @fontsource/sora` en `fuente/npm`, y pasar los woff2 600/700/800 a `fuente/ttf/Sora-<peso>.ttf` (fontTools).
- Clonar la PRIV en `/home/claude/jhonny-priv` (o `PRIV_REPO`).

Orden por tutorial N: `python3 tools/vNN.py h` y `v` → `python3 tools/voz.py tools/gNN.json` → `python3 build/tut.py tools/gNN.json h|v` → `python3 build/miniatura.py tools/gNN.json`.
Salida en `out/TNN/`.
