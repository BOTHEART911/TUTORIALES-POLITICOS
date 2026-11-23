"""CORE simulado para grabar la ZONA DE LÍDERES (JHONNY-PERDOMO / RONALD-SUAREZ).

DATOS DE EJEMPLO: campaña ficticia «Candidato Ejemplo · Villa Ejemplo», líder Laura Gómez
(N° 12) con 99 referidos inventados. Nunca datos reales.
responder(accion, params, cuerpo) -> lo que va en 'data' de la respuesta del CORE.
"""
import random, datetime as dt

random.seed(23)
HOY = dt.date.today()
FALTAN = []

MARCA = {
    'candidato': 'Candidato Ejemplo', 'pnCandidato': 'Candidato', 'municipio': 'Villa Ejemplo',
    'departamento': 'Departamento Ejemplo', 'lugar': 'Villa Ejemplo', 'lema': 'Tu campaña',
    'equipo': 'Equipo de ejemplo', 'color': '#0063D8', 'color700': '#004FAD',
    'icono': '/__assets/logo.png', 'banner': '/__assets/logo.png', 'imgBase': '/__assets/',
}
YO = {'documento': '1000000001', 'nombre': 'LAURA GÓMEZ RUIZ', 'pin': '2580'}
LIDER = {'codigo': '12', 'nombre': 'Laura Gómez Ruiz', 'documento': YO['documento'], 'correo': 'laura@ejemplo.co'}

NOMBRES = ['ANA', 'CARLOS', 'MARÍA', 'JORGE', 'PAOLA', 'ANDRÉS', 'LUISA', 'FELIPE', 'DIANA', 'JULIÁN',
           'CAMILA', 'SERGIO', 'NATALIA', 'ÓSCAR', 'VALENTINA', 'MAURICIO', 'SANDRA', 'RICARDO', 'LINA', 'HÉCTOR',
           'GLORIA', 'IVÁN', 'PATRICIA', 'FABIÁN', 'ROSA', 'NELSON', 'CLAUDIA', 'EDWIN', 'MARTA', 'WILSON']
APELL = ['ROJAS', 'CASTRO', 'MORENO', 'VARGAS', 'PARDO', 'ORTIZ', 'SUÁREZ', 'RAMÍREZ', 'LEÓN', 'TORRES',
         'CRUZ', 'PEÑA', 'DUARTE', 'SALAZAR', 'MEJÍA', 'RÍOS', 'CANO', 'ARIAS', 'SILVA', 'HERRERA']
BARRIOS = ['Centro', 'La Esperanza', 'El Prado', 'San José', 'Villa del Río', 'Los Almendros',
           'Las Palmas', 'El Recreo', 'Primero de Mayo', 'Vereda El Llano']
OPC = {'asistencia': ['Confirmada', 'No puede', 'Fuera de Villa Ejemplo', 'No contactado'],
       'intencion': ['Firme con el voto', 'No vota con nosotros', 'No está seguro(a)', 'No sabe votar', 'No contactado']}
LIDERES = [{'codigo': str(k + 1), 'nombre': n} for k, n in enumerate(['Ana Rojas Peña', 'Jorge Castro León', 'Paola Vargas Cruz', 'Felipe Ortiz Ríos',
    'Camila Peña Torres', 'Rosa León Duarte', 'Mario Silva Cano', 'Luz Marina Arias', 'Germán Duarte Ruiz', 'Yaneth Cruz Mejía', 'Óscar Iván Pardo'])]


def _f(d): return d.strftime('%d/%m/%Y')


def _refs(n=99):
    out, usados = [], set()
    # crecimiento: más registros en los meses recientes
    pesos = [(8, 2), (7, 8), (6, 9), (5, 11), (4, 13), (3, 15), (2, 14), (1, 13), (0, 14)]
    fechas = []
    for meses, k in pesos:
        for _ in range(k):
            ini = (HOY.replace(day=1) - dt.timedelta(days=30 * meses)).replace(day=1)
            fin = HOY if meses == 0 else (ini + dt.timedelta(days=27))
            fechas.append(ini + dt.timedelta(days=random.randint(0, max(0, (fin - ini).days))))
    for i in range(n):
        while True:
            nom = f"{random.choice(NOMBRES)} {random.choice(APELL)} {random.choice(APELL)}"
            if nom not in usados: usados.add(nom); break
        mun = 'VILLA EJEMPLO'
        if i % 13 == 5: mun = 'SIN CONSULTAR'
        if i % 17 == 9: mun = 'OTRO MUNICIPIO'
        inten = random.choice(['Firme con el voto'] * 4 + ['No está seguro(a)', 'No vota con nosotros', 'No contactado']) if random.random() < .41 else ''
        asis = random.choice(['Confirmada', 'No puede']) if (inten and random.random() < .3) else ''
        out.append({'documento': str(1000100000 + i * 731), 'nombre': nom, 'contacto': '300555' + str(1000 + i),
                    'residencia': random.choice(BARRIOS), 'municipio': mun, 'asistencia': asis, 'intencion': inten,
                    'fr': _f(fechas[i % len(fechas)]), 'foto': ''})
    # dos por confirmar (validación)
    out[20]['municipio'] = 'POR CONFIRMAR'; out[47]['municipio'] = 'POR CONFIRMAR'
    out.sort(key=lambda x: x['nombre'])
    return out


REFS = _refs()
# primera persona en pantalla: sin marcar, para el ejemplo de la llamada
for k in (0, 1, 2): REFS[k]['intencion'] = ''; REFS[k]['asistencia'] = ''
# otros registros de la base (de otros líderes)
OTROS = {'1000777001': {'nombre': 'RAÚL ANDRÉS QUINTERO', 'residencia': 'El Prado', 'referencia': '2', 'lider': 'Jorge Castro León'}}

SERV = ['Asesoría jurídica', 'Jornada de salud']
EVEN = [['E1', 'Encuentro con comerciantes', ''], ['E2', 'Caminata por el barrio', '']]
FORM = [['F1', 'Inscripción: Jornada de salud'], ['F2', 'Curso de emprendimiento']]


def _act():
    ds = [r['documento'] for r in REFS]
    s = {ds[i]: [i % 2] for i in range(0, 99, 7)}
    c = {ds[i]: 1 for i in range(3, 99, 9)}
    e = {ds[i]: [i % 2] for i in range(1, 99, 5)}
    f = {ds[i]: [i % 2] for i in range(2, 99, 8)}
    return {'s': {'n': SERV, 'd': s}, 'c': {'d': c}, 'e': {'n': EVEN, 'd': e}, 'f': {'n': FORM, 'd': f}}


MOTIVOS_PC = {}


def _pc():
    items = []
    for r in REFS:
        if r['municipio'] == 'POR CONFIRMAR':
            m = MOTIVOS_PC.setdefault(r['documento'], 'NO APARECE EN CENSO' if not MOTIVOS_PC else 'MUERTE')
            items.append({'d': r['documento'], 'n': r['nombre'], 'm': m, 'g': '12', 't': r['contacto'], 'r': r['residencia']})
    return {'ok': True, 'n': len(items), 'items': items, 'grupos': [{'codigo': '12', 'nombre': LIDER['nombre'], 'propio': True}]}


def _ref(doc): return next((r for r in REFS if r['documento'] == str(doc)), None)


def _traza(d):
    c = _ref(d) or {}
    def iso(dd, h): return dd.strftime('%Y-%m-%d') + 'T' + h + ':00'
    items = [
        {'k': 'formulario', 'tit': 'Inscripción: Jornada de salud', 'det': 'Se inscribió desde la app', 'est': 'CONFIRMADO', 'f': iso(HOY - dt.timedelta(days=4), '09:15')},
        {'k': 'compromiso', 'tit': 'Arreglo del alumbrado de su calle', 'det': 'Gestionado con la junta de acción comunal', 'est': 'PENDIENTE', 'f': iso(HOY - dt.timedelta(days=10), '16:40')},
        {'k': 'servicio', 'tit': 'Solicitud: Asesoría jurídica', 'det': 'Atendida por un profesional de la casa social', 'est': 'ATENDIDO', 'f': iso(HOY - dt.timedelta(days=21), '11:20')},
        {'k': 'evento', 'tit': 'Asistió: Encuentro con comerciantes', 'det': 'Plaza principal', 'est': '', 'f': iso(HOY - dt.timedelta(days=30), '15:05')},
        {'k': 'lider', 'tit': 'Referido por ' + LIDER['nombre'], 'det': '', 'est': '', 'f': ''},
        {'k': 'alta', 'tit': 'Registro en la base de datos', 'det': 'Agregado desde la zona de líderes', 'est': '', 'f': iso(HOY - dt.timedelta(days=70), '10:00')},
    ]
    return {'ok': True, 'persona': {'NOMBRE': c.get('nombre', ''), 'DOCUMENTO': d}, 'items': items, 'total': len(items),
            'resumen': {'servicios': 1, 'serviciosAtendidos': 1, 'compromisos': 1, 'eventos': 1, 'formularios': 1}}


def _lista():
    return {'ok': True, 'referidos': REFS, 'opciones': OPC, 'gestion': {'propio': True, 'nombre': LIDER['nombre'], 'ahijados': []},
            'act': _act(), 'pc': _pc(), 'rv': {}}


CONFIG = {'ok': True, 'conectar': 'Hola *{pn_referido}*\nTe comparto la App de *{pn_candidato}*\nInstala a través de este enlace: {APP_PUBLICA_URL}\nInicia sesión con tu CC: {documento}',
          'pnCandidato': 'Candidato', 'appPublicaUrl': 'https://ejemplo.app/', 'liderPrincipal': {'codigo': '1', 'nombre': 'Ana Rojas Peña'}}


def responder(accion, params, cuerpo):
    p = dict(params or {}); p.update(cuerpo or {})
    if accion == 'app.marca':
        return {'ok': True, 'data': MARCA}
    if accion in ('pub.config',):
        return CONFIG
    if accion == 'pub.paquete':
        return {'ok': True, 'config': CONFIG}
    if accion == 'pub.residencias':
        return BARRIOS
    if accion == 'pub.esProfesional':
        return {'ok': True, 'esProfesional': False}
    if accion == 'pub.esLider':
        return {'ok': True, 'esLider': True, 'tieneCorreo': True}
    if accion == 'pub.rev':
        return {'ok': True}
    if accion == 'pub.liderReferidos':
        return _lista()
    if accion == 'pub.liderTrazabilidad':
        return _traza(str(p.get('refDoc', '')))
    if accion == 'pub.liderTrazabilidadLote':
        return {'ok': True, 'mapa': {d: _traza(d) for d in str(p.get('docs', '')).split(',') if d}}
    if accion == 'pub.liderMarcar':
        r = _ref(p.get('refDoc'))
        if r: r['asistencia' if p.get('campo') == 'ASISTENCIA' else 'intencion'] = p.get('valor', '')
        return {'ok': True, 'fila': r}
    if accion == 'pub.lideresLista':
        return {'ok': True, 'lideres': LIDERES}
    if accion == 'pub.liderCeder':
        r = _ref(p.get('refDoc')); lid = next((l for l in LIDERES if l['codigo'] == str(p.get('destino'))), LIDERES[0])
        if r: REFS.remove(r)
        return {'ok': True, 'lider': lid['nombre'], 'quitar': str(p.get('refDoc'))}
    if accion == 'pub.validarDoc':
        d = str(p.get('documento', ''))
        if d in OTROS:
            o = OTROS[d]; return {'ok': True, 'existe': True, 'documento': d, 'nombre': o['nombre'], 'residencia': o['residencia'], 'referencia': o['referencia'], 'lider': o['lider']}
        r = _ref(d)
        if r: return {'ok': True, 'existe': True, 'documento': d, 'nombre': r['nombre'], 'residencia': r['residencia'], 'referencia': '12', 'lider': LIDER['nombre']}
        return {'ok': True, 'existe': False}
    if accion == 'pub.liderNuevoRef':
        f = {'documento': str(p.get('refDoc')), 'nombre': str(p.get('nombre', '')).upper(), 'contacto': p.get('contacto', ''), 'residencia': p.get('residencia', ''),
             'municipio': 'SIN CONSULTAR', 'asistencia': '', 'intencion': '', 'fr': _f(HOY), 'foto': ''}
        REFS.insert(0, f)
        return {'ok': True, 'fila': f}
    if accion == 'pub.liderAsignar':
        return {'ok': True}
    if accion in ('pub.pcVisto', 'pub.pcEditar', 'pub.pcFallecido'):
        r = _ref(p.get('refDoc'))
        if r:
            r['municipio'] = {'pub.pcVisto': 'A LA ESPERA', 'pub.pcEditar': 'SIN CONSULTAR', 'pub.pcFallecido': 'POR CONFIRMAR'}[accion]
        return {'ok': True, 'fila': r}
    if accion == 'pub.pcLista':
        return _pc()
    if accion == 'pub.liderPendRevisar':
        res = []
        for d in [x for x in str(p.get('docs', '')).split(',') if x]:
            if d in OTROS: res.append({'d': d, 'e': True, 'n': OTROS[d]['nombre'], 'r': OTROS[d]['referencia'], 'l': OTROS[d]['lider'], 'mio': False})
            elif _ref(d): res.append({'d': d, 'e': True, 'n': _ref(d)['nombre'], 'r': '12', 'l': LIDER['nombre'], 'mio': True})
            else: res.append({'d': d, 'e': False})
        return {'ok': True, 'res': res}
    if accion == 'pub.liderNuevoLote':
        res, filas = [], []
        for f in p.get('filas', []):
            fila = {'documento': f['d'], 'nombre': str(f.get('n', '')).upper(), 'contacto': f.get('t', ''), 'residencia': f.get('b', ''), 'municipio': 'SIN CONSULTAR',
                    'asistencia': '', 'intencion': '', 'fr': _f(HOY), 'foto': ''}
            REFS.insert(0, fila); filas.append(fila); res.append({'d': f['d'], 'ok': True})
        return {'ok': True, 'res': res, 'filas': filas}
    if accion in ('pub.liderInsights', 'pub.vozEstado', 'pub.comSocial', 'pub.misGestiones', 'pub.noticias', 'pub.inicio'):
        return {'ok': True, 'items': []}
    FALTAN.append(accion)
    return {'ok': True, 'items': []}
