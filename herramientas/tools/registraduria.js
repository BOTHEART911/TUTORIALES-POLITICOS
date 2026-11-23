// Recreación de la consulta de la Registraduría (consultacenso.registraduria.gov.co) con DATOS DE EJEMPLO.
// regiAbrir(doc) monta la capa; regiConsultar(fila) pinta el resultado; regiSeleccionar() marca la fila; regiCerrar().
window.regiAbrir = (doc) => {
  const st = document.createElement('style'); st.id = '__regi-css';
  st.textContent = `#__regi{position:fixed;inset:0;z-index:2147483600;background:#fff;font-family:Inter,Arial,sans-serif;overflow:auto;animation:__rin .35s ease}
  @keyframes __rin{from{opacity:0;transform:translateY(10px)}to{opacity:1}}
  #__regi .url{display:flex;align-items:center;gap:8px;height:34px;padding:0 14px;background:#f1f3f4;border-bottom:1px solid #dadce0;font-size:13px;color:#3c4043}
  #__regi .url b{font-weight:500}#__regi .url i{font-style:normal;color:#1e8e3e}
  #__regi .rot{margin-left:auto;background:#C2410C;color:#fff;font-size:11px;font-weight:700;padding:3px 9px;border-radius:10px;letter-spacing:.03em}
  #__regi header{background:#00305b;color:#fff;display:flex;align-items:center;min-height:118px;padding:0 28px;position:relative}
  #__regi .logo{font-family:Georgia,'Times New Roman',serif;line-height:1.05;text-align:center}
  #__regi .logo b{display:block;font-size:17px;letter-spacing:.02em}#__regi .logo small{font-size:8.5px;font-weight:700;letter-spacing:.04em}
  #__regi .logo .esc{width:46px;height:46px;margin:0 auto 6px;border:2px solid #fff;border-radius:50% 50% 45% 45%;opacity:.9}
  #__regi h1{position:absolute;left:0;right:0;text-align:center;margin:0;font:900 34px/1.1 Inter,Arial;letter-spacing:.01em;pointer-events:none}
  #__regi main{display:grid;grid-template-columns:1fr 1fr;gap:40px;padding:34px 72px 40px}
  #__regi label{display:block;color:#0b3a6e;font-weight:700;font-size:17px;margin:14px 0 10px}
  #__regi .in{border:2.5px solid #0b3a6e;border-radius:40px;height:52px;display:flex;align-items:center;padding:0 24px;font-size:17px;color:#222}
  #__regi .in.ph{color:#888}#__regi .ok{color:#1a9b6b;font-size:14px;margin:8px 8px 0;visibility:hidden}
  #__regi .sel{justify-content:space-between}#__regi .sel:after{content:'';border:6px solid transparent;border-top-color:#0b3a6e;margin-top:6px}
  #__regi .btn{display:inline-flex;align-items:center;justify-content:center;margin-top:30px;background:#0b3a6e;color:#fff;font-weight:800;letter-spacing:.12em;height:50px;width:220px;border-radius:30px;font-size:16px}
  #__regi h2{color:#0b3a6e;text-align:center;font:800 21px/1.2 Inter,Arial;letter-spacing:.03em;margin:6px 0 18px}
  #__regi .ayuda{color:#555;text-align:center;font-size:15px}
  #__regi table{width:100%;border-collapse:collapse;font-size:14px;text-align:center;color:#222}
  #__regi th{background:#e8eef6;color:#0b3a6e;font-size:12px;padding:10px 6px;border:1px solid #dde3ea}
  #__regi td{padding:12px 6px;border:1px solid #dde3ea}
  #__regi .ciud{margin-top:20px;text-align:center;color:#333;font-size:14px}#__regi .ciud b{display:block;color:#0b3a6e;font-size:17px;margin-bottom:10px}
  @media (max-width:700px){#__regi header{min-height:92px;padding:0 14px}#__regi h1{position:static;font-size:18px;text-align:left;margin-left:14px;flex:1}#__regi .url{font-size:11px;gap:4px;padding:0 8px}#__regi .rot{font-size:8.5px;padding:2px 6px;white-space:nowrap}
    #__regi .logo b{font-size:12px}#__regi .logo small{font-size:6px}#__regi .logo .esc{width:30px;height:30px}
    #__regi main{display:block;padding:18px 18px 30px}#__regi .der{margin-top:26px}#__regi label{font-size:15px}
    #__regi .in{height:46px;font-size:15px}#__regi table{font-size:11px}#__regi th{font-size:9px;padding:6px 2px}#__regi td{padding:8px 2px}#__regi h2{font-size:15px}}`;
  document.head.appendChild(st);
  const d = document.createElement('div'); d.id = '__regi';
  d.innerHTML = `<div class="url">🔒 <b>consultacenso.registraduria.gov.co</b><span class="rot">RECREACIÓN · DATOS DE EJEMPLO</span></div>
  <header><div class="logo"><div class="esc"></div><b>REGISTRADURÍA</b><small>NACIONAL DEL ESTADO CIVIL</small></div><h1>CONSULTA LUGAR DE VOTACIÓN</h1></header>
  <main><section><label>No. Identificación:</label><div class="in ph" id="__regi-doc">dígite el número sin puntos ni comas</div>
  <div class="ok" id="__regi-ok">✓ El campo está listo para ser enviado</div>
  <label>Seleccione la elección:</label><div class="in sel">LUGAR DE VOTACION ACTUAL</div>
  <div class="btn" id="__regi-btn">CONSULTAR</div></section>
  <section class="der"><h2>INFORMACIÓN DEL LUGAR DE VOTACIÓN</h2><div id="__regi-res"><p class="ayuda">Por favor digite su número de cédula, seleccione el tipo de elección y dé clic en consultar.</p></div></section></main>`;
  document.body.appendChild(d);
  window.__regiDoc = doc;
};
window.regiPegar = () => { const e = document.getElementById('__regi-doc'); e.classList.remove('ph'); e.textContent = window.__regiDoc; document.getElementById('__regi-ok').style.visibility = 'visible'; };
window.regiConsultar = (f) => {
  document.getElementById('__regi-res').innerHTML = `<table id="__regi-tab"><thead><tr><th>NUIP</th><th>DEPARTAMENTO</th><th>MUNICIPIO</th><th>PUESTO</th><th>DIRECCIÓN</th><th>MESA</th></tr></thead>
  <tbody><tr id="__regi-fila">${f.map(x => `<td>${x}</td>`).join('')}</tr></tbody></table>
  <div class="ciud"><b>Señor Ciudadano:</b>Si tiene dudas o inquietudes acerca de su lugar de votación, contáctese con la Registraduría Nacional del Estado Civil.</div>`;
};
window.regiSeleccionar = () => { const r = document.createRange(); r.selectNodeContents(document.getElementById('__regi-fila')); const s = getSelection(); s.removeAllRanges(); s.addRange(r); };
window.regiCerrar = () => { getSelection().removeAllRanges(); const d = document.getElementById('__regi'); if (d) d.remove(); };
