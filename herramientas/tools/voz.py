"""Voz es-CO por escena (edge-tts) -> voz/<ID>/<escena>.mp3 + .vtt + dur.json"""
import json, os, sys, subprocess
G = json.load(open(sys.argv[1])); VOZ = os.environ.get('VOZ', 'es-CO-SalomeNeural')
d = f"/home/claude/tut/voz/{G['id']}"; os.makedirs(d, exist_ok=True)
env = dict(os.environ, SSL_CERT_FILE='/root/.ccr/ca-bundle.crt')
dur = {}
for e in G['escenas']:
    mp3, vtt = f"{d}/{e['id']}.mp3", f"{d}/{e['id']}.vtt"
    if not (os.path.exists(mp3) and os.path.exists(vtt)) or os.environ.get('REHACER'):
        for i in range(3):
            r = subprocess.run(['edge-tts', '--proxy', os.environ['HTTPS_PROXY'], '--voice', VOZ, '--rate', '+4%', '--text', e['voz'], '--write-media', mp3, '--write-subtitles', vtt], env=env, capture_output=True, text=True, timeout=90)
            if r.returncode == 0: break
    p = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', mp3], capture_output=True, text=True)
    dur[e['id']] = float(p.stdout.strip())
json.dump(dur, open(f"{d}/dur.json", 'w'), indent=1); print(dur)
