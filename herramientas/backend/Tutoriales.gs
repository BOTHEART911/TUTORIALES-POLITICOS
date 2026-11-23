/**
 * Tutoriales.gs — TUTORIALES EN VIDEO DE PRIV (23/11/2026)
 * ============================================================================
 * La lista de tutoriales es UNA SOLA para todas las PRIV (marca blanca): vive
 * en el repo BOTHEART911/TUTORIALES-POLITICOS (priv/tutoriales.json) y cada
 * PRIV la lee DIRECTO de GitHub Pages, sin pasar por aquí. Este archivo solo:
 *   1. anota quién vio qué (hoja TUTORIALES_VISTOS) para que el avance siga a
 *      la persona en otro equipo y Avanzado muestre «quién vio qué»;
 *   2. guarda los cambios que el DESARROLLADOR hace en Configuración →
 *      Avanzado → Tutoriales, escribiendo en el repo con la API de GitHub.
 *      La llave vive en las Propiedades del script (TUT_GITHUB_TOKEN) y NUNCA
 *      baja al navegador. Se pega una vez desde Avanzado (priv.tutLlave).
 *      Token recomendado: fine-grained, solo el repo TUTORIALES-POLITICOS,
 *      permiso Contents: Read and write.
 *
 * RUTAS
 *  · priv.tutVistos  { caller }               (lectura, cualquier usuario activo)
 *      → { ok, vistos:[ids] }
 *  · priv.tutVisto   { caller, id }           (cualquier usuario activo)
 *      → { ok }  una fila por persona y tutorial (no repite)
 *  · priv.tutResumen { caller }               (lectura, solo DESARROLLADOR)
 *      → { ok, usuarios, vieron, porId:{id:n}, llave:bool }
 *  · priv.tutLlave   { caller, llave }        (solo DESARROLLADOR)
 *      → { ok }  guarda el token en las propiedades (vacío lo borra)
 *  · priv.tutGuardar { caller, base, lista, img? }   (solo DESARROLLADOR)
 *      lista = JSON completo; base = la versión que el navegador editó.
 *      Si en GitHub ya hay otra versión → { ok:false, conflicto:true } (nadie
 *      pisa a nadie). Si no: version+1, actualizado = hoy y PUT al repo.
 *      img = JSON { id, base64 } → priv/img/<id>v.jpg en el mismo guardado.
 *      → { ok, lista (texto), version }
 * ============================================================================
 */
var TUT_REPO = 'BOTHEART911/TUTORIALES-POLITICOS';
var TUT_RUTA = 'priv/tutoriales.json';
var TUT_PROP = 'TUT_GITHUB_TOKEN';
var TUT_HOJA = 'TUTORIALES_VISTOS';
var TUT_CAB = ['FECHA', 'DOCUMENTO', 'NOMBRE', 'ID'];

function tutQuien_(p) {
  var caller = nucleoQuien_(p.caller);
  var u = findRowByDoc_('USUARIOS', caller);
  if (!u || String(u['ESTADO']).toUpperCase() !== 'ACTIVO') throw new Error('No autorizado');
  return { doc: String(caller), nombre: String(u['NOMBRE'] || ''), rol: String(u['ROL'] || '').toUpperCase() };
}
function tutHoja_() {
  var sh = shOpt_(TUT_HOJA);
  if (!sh) {
    sh = ss_().insertSheet(TUT_HOJA);
    sh.getRange(1, 1, 1, TUT_CAB.length).setValues([TUT_CAB]);
    sh.setFrozenRows(1);
    _shMemo[TUT_HOJA] = sh;
  }
  return sh;
}
/** Todas las filas (una lectura por ejecución). */
function tutFilas_() {
  var sh = shOpt_(TUT_HOJA);
  if (!sh || sh.getLastRow() < 2) return [];
  return sh.getRange(2, 1, sh.getLastRow() - 1, TUT_CAB.length).getValues();
}
function tutCacheK_(doc) { return 'tutv:' + doc; }

function apiPrivTutVistos_(p) {
  var q = tutQuien_(p);
  var c = CacheService.getScriptCache(), k = tutCacheK_(q.doc), hit = c.get(k);
  if (hit) return { ok: true, vistos: JSON.parse(hit) };
  var ids = [];
  tutFilas_().forEach(function (r) { if (String(r[1]) === q.doc && ids.indexOf(String(r[3])) < 0) ids.push(String(r[3])); });
  c.put(k, JSON.stringify(ids), 21600);
  return { ok: true, vistos: ids };
}

function apiPrivTutVisto_(p) {
  var q = tutQuien_(p);
  var id = String(p.id || '').replace(/[^A-Za-z0-9_-]/g, '').slice(0, 20);
  if (!id) return { ok: false, msg: 'Falta el tutorial' };
  var c = CacheService.getScriptCache(), k = tutCacheK_(q.doc), hit = c.get(k);
  if (hit && JSON.parse(hit).indexOf(id) >= 0) return { ok: true, ya: true };
  var lock = LockService.getScriptLock();
  lock.waitLock(10000);
  try {
    var ids = [];
    tutFilas_().forEach(function (r) { if (String(r[1]) === q.doc) ids.push(String(r[3])); });
    if (ids.indexOf(id) < 0) {
      tutHoja_().appendRow([new Date(), q.doc, q.nombre, id]);
      ids.push(id);
    }
    c.put(k, JSON.stringify(ids), 21600);
  } finally { lock.releaseLock(); }
  return { ok: true };
}

function apiPrivTutResumen_(p) {
  cfRequire_(p, [ROL_DEV]);
  var sh = shOpt_('USUARIOS'), activos = 0;
  if (sh && sh.getLastRow() > 1) {
    var v = sh.getDataRange().getValues(), cab = v[0].map(function (x) { return String(x).trim().toUpperCase(); });
    var iE = cab.indexOf('ESTADO'), iR = cab.indexOf('ROL');
    for (var i = 1; i < v.length; i++) {
      if (String(v[i][iE]).toUpperCase() !== 'ACTIVO') continue;
      if (iR >= 0 && String(v[i][iR]).toUpperCase() === ROL_DEV) continue;
      activos++;
    }
  }
  var docs = {}, porId = {}, par = {};
  tutFilas_().forEach(function (r) {
    var d = String(r[1]), id = String(r[3]);
    if (par[d + '|' + id]) return;
    par[d + '|' + id] = 1; docs[d] = 1; porId[id] = (porId[id] || 0) + 1;
  });
  return { ok: true, usuarios: activos, vieron: Object.keys(docs).length, porId: porId,
           llave: !!PropertiesService.getScriptProperties().getProperty(TUT_PROP) };
}

function apiPrivTutLlave_(p) {
  cfRequire_(p, [ROL_DEV]);
  var t = String(p.llave || '').trim();
  var pr = PropertiesService.getScriptProperties();
  if (!t) { pr.deleteProperty(TUT_PROP); return { ok: true, borrada: true }; }
  if (!/^(github_pat_|ghp_)[A-Za-z0-9_]{20,}$/.test(t)) return { ok: false, msg: 'Eso no parece un token de GitHub (empieza por github_pat_ o ghp_)' };
  /* se prueba antes de guardarla: debe poder leer el archivo del repo */
  var r = tutGh_('GET', TUT_RUTA, null, t);
  if (r.code !== 200) return { ok: false, msg: 'GitHub no aceptó la llave (' + r.code + '). Revisa que tenga acceso al repo TUTORIALES-POLITICOS.' };
  pr.setProperty(TUT_PROP, t);
  return { ok: true };
}

/** Llamada a la API de contenidos de GitHub. */
function tutGh_(metodo, ruta, cuerpo, token) {
  var tk = token || PropertiesService.getScriptProperties().getProperty(TUT_PROP);
  if (!tk) return { code: 0, json: null };
  var op = {
    method: metodo, muteHttpExceptions: true, contentType: 'application/json',
    headers: { Authorization: 'Bearer ' + tk, Accept: 'application/vnd.github+json', 'X-GitHub-Api-Version': '2022-11-28' }
  };
  if (cuerpo) op.payload = JSON.stringify(cuerpo);
  var res = UrlFetchApp.fetch('https://api.github.com/repos/' + TUT_REPO + '/contents/' + ruta, op);
  var j = null; try { j = JSON.parse(res.getContentText()); } catch (e) {}
  return { code: res.getResponseCode(), json: j };
}

function apiPrivTutGuardar_(p) {
  var q = cfRequire_(p, [ROL_DEV]);
  if (!PropertiesService.getScriptProperties().getProperty(TUT_PROP))
    return { ok: false, msg: 'Falta la llave de GitHub: pégala en Avanzado → Tutoriales' };
  var lista;
  try { lista = JSON.parse(String(p.lista || '')); } catch (e) { return { ok: false, msg: 'La lista no es válida' }; }
  if (!lista || !(lista.tutoriales instanceof Array)) return { ok: false, msg: 'La lista no es válida' };
  /* 23/11/2026 · cual=lideres → la lista de la zona de líderes (lideres/tutoriales.json) */
  var CUAL = String(p.cual || '') === 'lideres' ? 'lideres' : 'priv';
  var RUTA = CUAL + '/tutoriales.json';

  var lock = LockService.getScriptLock();
  lock.waitLock(20000);
  try {
    var cur = tutGh_('GET', RUTA);
    if (cur.code !== 200 || !cur.json) return { ok: false, msg: 'No se pudo leer la lista en GitHub (' + cur.code + ')' };
    var remota = JSON.parse(Utilities.newBlob(Utilities.base64Decode(String(cur.json.content).replace(/\s/g, ''))).getDataAsString('UTF-8'));
    if (String(remota.version) !== String(p.base)) return { ok: false, conflicto: true, msg: 'La lista cambió mientras editabas' };

    lista.version = (parseInt(remota.version, 10) || 0) + 1;
    lista.actualizado = Utilities.formatDate(new Date(), 'America/Bogota', 'yyyy-MM-dd');
    var quien = (q && q.nombre) || 'Desarrollador';

    /* imagen vertical del Short, si vino */
    if (p.img) {
      var im = JSON.parse(String(p.img));
      var iid = String(im.id || '').replace(/[^A-Za-z0-9_-]/g, '');
      if (iid && im.base64) {
        var ruta = CUAL + '/img/' + iid + 'v.jpg';
        var ya = tutGh_('GET', ruta);
        var cpo = { message: 'Imagen del Short ' + iid + ' (desde PRIV · ' + quien + ')', content: String(im.base64) };
        if (ya.code === 200 && ya.json && ya.json.sha) cpo.sha = ya.json.sha;
        var ri = tutGh_('PUT', ruta, cpo);
        if (ri.code !== 200 && ri.code !== 201) return { ok: false, msg: 'GitHub no guardó la imagen (' + ri.code + ')' };
      }
    }

    var texto = JSON.stringify(lista, null, 1);
    var r = tutGh_('PUT', RUTA, {
      message: (CUAL === 'lideres' ? 'Tutoriales zona de líderes v' : 'Tutoriales v') + lista.version + ' (desde PRIV · ' + quien + ')',
      content: Utilities.base64Encode(texto, Utilities.Charset.UTF_8),
      sha: cur.json.sha
    });
    if (r.code === 409) return { ok: false, conflicto: true, msg: 'La lista cambió mientras editabas' };
    if (r.code !== 200 && r.code !== 201) return { ok: false, msg: 'GitHub no guardó la lista (' + r.code + ')' };
    return { ok: true, lista: texto, version: lista.version };
  } finally { lock.releaseLock(); }
}
