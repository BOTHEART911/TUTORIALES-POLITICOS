"""CORE simulado para grabar PRIV con DATOS DE EJEMPLO (nunca datos reales).

responder(accion, params, cuerpo) -> dict JSON como lo manda el CORE.
Lo que no tenga respuesta propia devuelve {ok:true, items:[]} y queda en FALTAN.
"""
import random, datetime as dt

random.seed(7)
HOY = dt.date.today()
FALTAN = []

MARCA = {
    'candidato': 'Candidato Ejemplo', 'pnCandidato': 'Candidato', 'municipio': 'Villa Ejemplo',
    'departamento': 'Departamento Ejemplo', 'lugar': 'Villa Ejemplo', 'lema': 'Tu campaña',
    'equipo': 'Equipo de ejemplo', 'color': '#0063D8', 'color700': '#004FAD',
    'icono': '/__assets/logo.png', 'banner': '/__assets/logo.png', 'imgBase': '/__assets/',
}

USUARIOS = {
    '2580': {'documento': '1000000001', 'nombre': 'Laura Gómez Ruiz', 'rol': 'ADMIN'},
    '1357': {'documento': '1000000002', 'nombre': 'Diego Martínez', 'rol': 'INVITADO'},
}
FOTO = {'v': ''}

NOMBRES = ['Ana', 'Carlos', 'María', 'Jorge', 'Paola', 'Andrés', 'Luisa', 'Felipe', 'Diana', 'Julián',
           'Camila', 'Sergio', 'Natalia', 'Óscar', 'Valentina', 'Mauricio', 'Sandra', 'Ricardo', 'Lina', 'Héctor',
           'Gloria', 'Iván', 'Patricia', 'Fabián', 'Rosa', 'Nelson', 'Claudia', 'Edwin', 'Marta', 'Wilson']
APELL = ['Rojas', 'Castro', 'Moreno', 'Vargas', 'Pardo', 'Ortiz', 'Suárez', 'Ramírez', 'León', 'Torres',
         'Cruz', 'Peña', 'Duarte', 'Salazar', 'Mejía', 'Ríos', 'Cano', 'Arias', 'Silva', 'Herrera']
BARRIOS = ['Centro', 'La Esperanza', 'El Prado', 'San José', 'Villa del Río', 'Los Almendros',
           'Las Palmas', 'El Recreo', 'Primero de Mayo', 'Vereda El Llano']
INTEN = ['Firme con el voto'] * 5 + ['No está seguro(a)', 'No contactado', 'No sabe votar', ''] + [''] * 3
PUESTOS = ['IE CENTRAL', 'COLEGIO LA ESPERANZA', 'ESCUELA EL PRADO', 'IE SAN JOSÉ']


def _fecha(d):
    return d.strftime('%d/%m/%Y')


def _personas(n=64):
    out = []
    for i in range(n):
        nom = f"{random.choice(NOMBRES)} {random.choice(APELL)} {random.choice(APELL)}"
        mun = 'Villa Ejemplo' if i % 7 else random.choice(['Otro municipio', 'POR CONFIRMAR'])
        if i % 9 == 4: mun = 'SIN CONSULTAR'
        reg = HOY - dt.timedelta(days=random.randint(3, 200))
        p = {
            'documento': str(1000000100 + i * 37), 'nombre': nom, 'residencia': random.choice(BARRIOS),
            'municipio': mun, 'intencion': random.choice(INTEN), 'estado': 'ACTIVO',
            'fechaRegistro': _fecha(reg), 'fechaActualizacion': _fecha(reg + dt.timedelta(days=random.randint(0, 3))) if i % 3 == 0 else '',
            'esLider': i % 11 == 0, 'foto': '', 'puestoCrudo': random.choice(PUESTOS) if mun == 'Villa Ejemplo' else '',
            'mesa': str(random.randint(1, 18)) if mun == 'Villa Ejemplo' else '', 'motivo': 'NO APARECE EN EL CENSO' if mun == 'POR CONFIRMAR' else '',
            'telefono': '300' + str(5550000 + i), 'referencia': str(1 + i % 6) if i % 5 else '',
        }
        out.append(p)
    out.sort(key=lambda x: x['nombre'])
    return out


PERSONAS = _personas()
for k, (nom, doc) in enumerate([('Alberto Gómez Silva', '1000007001'), ('Inés Moreno Cano', '1000007002')]):
    PERSONAS.append({'documento': doc, 'nombre': nom, 'residencia': 'Centro', 'municipio': 'POR CONFIRMAR', 'intencion': '', 'estado': 'INACTIVO',
        'fechaRegistro': _fecha(HOY - dt.timedelta(days=90 + k)), 'fechaActualizacion': _fecha(HOY - dt.timedelta(days=2)), 'esLider': False, 'foto': '',
        'puestoCrudo': '', 'mesa': '', 'motivo': 'FALLECIDO · CONFIRMADO POR EL LÍDER', 'telefono': '', 'referencia': '2'})
LIDERES = [{'codigo': str(k + 1), 'nombre': n} for k, n in enumerate(['Ana Rojas Peña', 'Jorge Castro León', 'Paola Vargas Cruz', 'Felipe Ortiz Ríos', 'Camila Peña Torres', 'Rosa León Duarte',
    'Mario Silva Cano', 'Luz Marina Arias', 'Germán Duarte Ruiz', 'Yaneth Cruz Mejía', 'Óscar Iván Pardo', 'Sofía Herrera León'])]
_REF = [64, 52, 38, 27, 19, 12, 9, 7, 5, 3, 2, 0]
_CLA = ['PRINCIPAL', 'PRINCIPAL', 'PRINCIPAL', 'SUGERIDO POR LIDER', 'PRINCIPAL', 'FAMILIAR', 'SUGERIDO POR LIDER', 'PROCESOS INTERNOS', 'FAMILIAR', 'SUGERIDO POR LIDER', 'PRINCIPAL', 'SUGERIDO POR LIDER']
_PAD = ['', '', '', 'Ana Rojas Peña', '', 'Jorge Castro León', 'Ana Rojas Peña', '', 'Paola Vargas Cruz', 'Jorge Castro León', '', 'Ana Rojas Peña']
def _lider(k, l):
    ref = _REF[k]; firme = round(ref * .45); nov = round(ref * .08); dud = round(ref * .1); nos = round(ref * .05); noc = round(ref * .07)
    trab = firme + nov + dud + nos + noc; pct = round(trab * 100 / ref) if ref else 0
    des = [{'label': a, 'n': b, 'pct': round(b * 100 / ref) if ref else 0} for a, b in (('Firme con el voto', firme), ('No vota con nosotros', nov), ('No está seguro(a)', dud), ('No sabe votar', nos), ('No contactado', noc))]
    return dict(l, documento=str(1000003000 + k * 17), contacto='57300555' + str(1200 + k), residencia=BARRIOS[k % len(BARRIOS)], padrino=_PAD[k], referidos=ref,
                trabajadas=trab, pctTrabajo=pct, desglose=des, noFidelizados=ref - trab, pctNoFidelizados=(100 - pct) if ref else 0,
                clasificacion=_CLA[k], activado=k < 8, correo='', foto='', telLocal='300555' + str(1200 + k))
LIDERES_FULL = [_lider(k, l) for k, l in enumerate(LIDERES)]
import os as _os
if _os.environ.get('LIDERES_EN_BD', '1') == '1':
    for _l in LIDERES_FULL:
        PERSONAS.append({'documento': _l['documento'], 'nombre': _l['nombre'], 'residencia': _l['residencia'], 'municipio': 'Villa Ejemplo', 'intencion': 'Firme con el voto', 'estado': 'ACTIVO',
            'fechaRegistro': _fecha(HOY - dt.timedelta(days=150)), 'fechaActualizacion': '', 'esLider': True, 'foto': '', 'puestoCrudo': 'IE CENTRAL', 'mesa': '3', 'motivo': '', 'telefono': _l['telLocal'], 'referencia': '1'})
EXISTE = {'1000000951': 'Jorge Peña Herrera'}
for x in PERSONAS: EXISTE[x['documento']] = x['nombre']



def _agenda():
    base = HOY.replace(day=1)
    titulos = [('Reunión con líderes del Centro', 'Casa social', 'Ana Rojas'),
               ('Visita al barrio La Esperanza', 'Salón comunal', 'Jorge Castro'),
               ('Encuentro con comerciantes', 'Plaza principal', 'Paola Vargas'),
               ('Recorrido vereda El Llano', 'Escuela de la vereda', 'Felipe Ortiz'),
               ('Reunión de jóvenes', 'Biblioteca', 'Camila Peña'),
               ('Desayuno con madres comunitarias', 'Casa social', 'Rosa León'),
               ('Taller de testigos electorales', 'Sede de campaña', 'Sergio Cruz')]
    it = []
    for k, (t, l, c) in enumerate(titulos):
        d = base + dt.timedelta(days=2 + k * 4)
        est = 'REALIZADA' if d < HOY else 'PROGRAMADA'
        if k == 3: est = 'A REPROGRAMAR'
        it.append({'id': f'AG{k+1:03d}', 'fecha': _fecha(d), 'inicia': ['08:00', '10:30', '15:00', '17:30'][k % 4],
                   'termina': ['09:30', '12:00', '16:30', '19:00'][k % 4], 'titulo': t, 'lugar': l, 'contacto': c, 'estado': est})
    return it


AGENDA = _agenda()


def _user(u, tk='tk-ejemplo'):
    return dict(u, tk=tk, foto=FOTO['v'], permisos=None)


def responder(accion, params, cuerpo):
    p = dict(params or {}); p.update(cuerpo or {})
    if accion == 'app.marca':
        return {'ok': True, 'data': MARCA}
    if accion == 'priv.login':
        u = USUARIOS.get(str(p.get('pin', '')))
        if not u:
            return {'ok': False, 'msg': 'PIN incorrecto'}
        return {'ok': True, 'user': _user(u)}
    if accion == 'priv.miPerfil':
        return {'ok': True, 'foto': FOTO['v'], 'permisos': None, 'rol': 'ADMIN'}
    if accion in ('priv.miFoto', 'priv.subirMiFoto', 'priv.fotoPerfil'):
        FOTO['v'] = '/__assets/foto_laura.png'
        return {'ok': True, 'foto': FOTO['v']}
    if accion == 'priv.baseDatos':
        return {'ok': True, 'items': PERSONAS, 'lideres': LIDERES,
                'columnas': [], 'dash': {'puestos': PUESTOS, 'puestoOtro': 'OTRO MUNICIPIO'}, 'rv': {}, 'registraduriaUrl': 'https://consultacenso.registraduria.gov.co/', 'pc': {'candidato': 'Candidato Ejemplo', 'plantilla': 'Buen día estimados líderes:\n\nLa base de datos se actualizó y hay {n} documentos por validar. Por favor revisen si tienen alguno ustedes o sus ahijados en la app: zona de líderes → Mis referidos.\n\nCordialmente,\n{nombre_candidato}'}}
    if accion == 'pub.residencias':
        return BARRIOS
    if accion == 'priv.validarDoc':
        d = str(p.get('documento', ''))
        return {'ok': True, 'existe': d in EXISTE, 'nombre': EXISTE.get(d, '')}
    if accion == 'priv.personaAgregar':
        c = {'documento': str(p.get('documento')), 'nombre': str(p.get('nombre', '')).upper() if False else p.get('nombre', ''), 'residencia': p.get('residencia', ''),
             'municipio': 'SIN CONSULTAR', 'intencion': '', 'estado': 'ACTIVO', 'fechaRegistro': _fecha(dt.date.today()), 'fechaActualizacion': '',
             'esLider': False, 'foto': '', 'puestoCrudo': '', 'mesa': '', 'motivo': '', 'referencia': p.get('referencia', ''), 'telefono': p.get('contacto', '')}
        PERSONAS.append(c); EXISTE[c['documento']] = c['nombre']
        return {'ok': True, 'card': c}
    if accion == 'priv.puestoGuardar':
        c = next((x for x in PERSONAS if x['documento'] == str(p.get('documento'))), None)
        if c and p.get('marca'):
            c.update({'municipio': p['marca'], 'motivo': p.get('motivo', ''), 'fechaActualizacion': _fecha(dt.date.today())})
        elif c:
            mun = str(p.get('municipio', '')).strip()
            c.update({'municipio': 'Villa Ejemplo' if mun.upper() == 'VILLA EJEMPLO' else mun.title(), 'puestoCrudo': p.get('puesto', ''), 'mesa': p.get('mesa', ''), 'fechaActualizacion': _fecha(dt.date.today())})
        return {'ok': True, 'card': c}
    if accion in ('priv.trazabilidad', 'priv.persona'):
        return _traza(str(p.get('documento', '')))
    if accion == 'priv.trazabilidadLote':
        return {'ok': True, 'mapa': {d: _traza(d) for d in str(p.get('docs', '')).split(',') if d}}
    if accion == 'priv.personaEditar':
        c = _fila(p.get('documentoOriginal'))
        if c: c.update({'nombre': p.get('nombre', c['nombre']), 'residencia': p.get('residencia', c['residencia']), 'telefono': p.get('contacto', ''), 'referencia': p.get('referencia', ''), 'fechaActualizacion': _fecha(dt.date.today())})
        return {'ok': True, 'card': c}
    if accion == 'priv.personaInactivar':
        c = _fila(p.get('documento')); c['estado'] = 'INACTIVO'; return {'ok': True, 'card': c}
    if accion == 'priv.personaEliminar':
        c = _fila(p.get('documento'))
        if c: PERSONAS.remove(c)
        return {'ok': True}
    if accion == 'priv.puestoLote':
        n, antes, faltan = 0, [], []
        for f in p.get('filas', []):
            c = _fila(f.get('d'))
            if not c: faltan.append(f.get('d')); continue
            antes.append([c['documento'], '', c['municipio'], c['puestoCrudo'], '', c['mesa'], c.get('motivo', '')])
            mun = f.get('h', '')
            c.update({'municipio': 'Villa Ejemplo' if mun == 'VILLA EJEMPLO' else (mun.title() if mun not in ('POR CONFIRMAR', 'A LA ESPERA') else mun),
                      'puestoCrudo': f.get('i', ''), 'mesa': f.get('k', ''), 'motivo': f.get('m', '') if mun == 'POR CONFIRMAR' else '', 'fechaActualizacion': _fecha(dt.date.today())})
            n += 1
        return {'ok': True, 'n': n, 'antes': antes, 'noEncontrados': faltan, 'puestosNuevos': []}
    if accion == 'priv.personaReasignar':
        c = _fila(p.get('documento')); c['referencia'] = str(p.get('referencia')); c['fechaActualizacion'] = _fecha(dt.date.today())
        return {'ok': True, 'card': c}
    if accion == 'priv.bdPendRevisar':
        docs = [d for d in str(p.get('docs', '')).split(',') if d]
        res = []
        for d in docs:
            c = _fila(d)
            lid = next((l for l in LIDERES if c and l['codigo'] == c.get('referencia')), None)
            res.append({'d': d, 'e': bool(c), 'n': c['nombre'] if c else '', 'r': c.get('referencia', '') if c else '', 'l': lid['nombre'] if lid else '', 'mio': False})
        return {'ok': True, 'res': res}
    if accion == 'priv.bdNuevoLote':
        lid = next((l for l in LIDERES if l['codigo'] == str(p.get('lider'))), LIDERES[0]); res, cards = [], []
        for f in p.get('filas', []):
            c = {'documento': f['d'], 'nombre': f['n'], 'residencia': f['b'], 'municipio': 'SIN CONSULTAR', 'intencion': '', 'estado': 'ACTIVO',
                 'fechaRegistro': _fecha(dt.date.today()), 'fechaActualizacion': '', 'esLider': False, 'foto': '', 'puestoCrudo': '', 'mesa': '', 'motivo': '',
                 'referencia': lid['codigo'], 'telefono': f.get('t', '')}
            PERSONAS.append(c); cards.append(c); res.append({'d': f['d'], 'ok': True})
        return {'ok': True, 'res': res, 'subidos': len(res), 'cards': cards, 'lider': lid}
    if accion in ('priv.balancePdf',):
        import base64
        return {'ok': True, 'base64': base64.b64encode(open('/home/claude/tut/assets/balance_ejemplo.pdf', 'rb').read()).decode(), 'mime': 'application/pdf', 'filename': 'BALANCE_OCTUBRE_2026.pdf'}
    if accion in ('priv.bdPdf', 'priv.bdExcel'):
        import base64
        return {'ok': True, 'base64': base64.b64encode(open('/home/claude/tut/assets/bd_ejemplo.pdf', 'rb').read()).decode(), 'mime': 'application/pdf', 'filename': 'BASE_DE_DATOS_VILLA_EJEMPLO.pdf'}
    if accion == 'priv.agenda':
        return {'ok': True, 'items': AGENDA, 'estricta': False, 'esDev': False}
    if accion == 'priv.agendaMeta':
        return {'ok': True, 'candidato': {'nombre': 'Candidato Ejemplo'}, 'plantillas': {}}
    if accion == 'priv.iaEstado':
        return {'ok': True, 'configurada': True}
    if accion == 'priv.vozEstado':
        return {'ok': True, 'configurada': False}
    if accion == 'priv.iaAnalizar':
        return {'ok': True, 'modelo': 'Análisis', 'generado': 'hace un momento', 'texto': IA_TEXTO.get(p.get('vista'), IA_TEXTO['bd'])}
    if accion == 'priv.lideres':
        return {'ok': True, 'items': LIDERES_FULL, 'columnas': [], 'rv': {}, 'plantillas': None}
    if accion == 'priv.liderNuevoMeta':
        return {'ok': True, 'lideres': [{'codigo': l['codigo'], 'nombre': l['nombre']} for l in LIDERES_FULL], 'sugerido': str(len(LIDERES_FULL) + 1)}
    if accion == 'priv.liderBuscarDoc':
        d = str(p.get('documento', '')); l = next((x for x in LIDERES_FULL if x['documento'] == d), None)
        if l: return {'ok': True, 'yaLider': True, 'codigo': l['codigo'], 'nombre': l['nombre']}
        c = _fila(d)
        if c: return {'ok': True, 'enPrincipal': True, 'nombre': c['nombre'], 'contacto': c.get('telefono', ''), 'residencia': c['residencia']}
        return {'ok': True, 'enPrincipal': False}
    if accion in ('priv.liderAgregar', 'priv.liderEditar'):
        cod = str(p.get('codigo')); l = next((x for x in LIDERES_FULL if x['codigo'] == cod or x['documento'] == str(p.get('documento'))), None)
        if not l:
            l = _lider(11, {'codigo': cod, 'nombre': p.get('nombre', '')}); l.update(referidos=0, trabajadas=0, pctTrabajo=0, desglose=[], noFidelizados=0, activado=False)
            LIDERES_FULL.append(l)
        l.update({k: v for k, v in (('nombre', p.get('nombre')), ('documento', p.get('documento')), ('residencia', p.get('residencia')), ('padrino', p.get('padrino')), ('clasificacion', p.get('clasificacion')), ('contacto', '57' + str(p.get('contacto', '')) if p.get('contacto') else None)) if v})
        return {'ok': True, 'card': l, 'desactivados': []}
    if accion == 'priv.liderVer':
        l = next((x for x in LIDERES_FULL if x['codigo'] == str(p.get('codigo'))), None)
        return {'ok': True, 'lider': dict(l, enPrincipal=True, municipio='Villa Ejemplo', puesto='IE CENTRAL', mesa='3')}
    if accion == 'priv.liderEliminarPrevia':
        l = next((x for x in LIDERES_FULL if x['codigo'] == str(p.get('codigo'))), None)
        return {'ok': True, 'referidos': l['referidos'], 'activos': l['referidos'], 'ahijados': 0, 'delegados': 0, 'bitacoras': 3, 'compromisos': 1, 'compromisosAbiertos': 0, 'solicitudes': 0, 'solicitudesAbiertas': 0, 'inactivos': [], 'hayClave': True}
    if accion == 'priv.liderEliminar':
        o = next((x for x in LIDERES_FULL if x['codigo'] == str(p.get('codigo'))), None); d = next((x for x in LIDERES_FULL if x['codigo'] == str(p.get('destino'))), None)
        LIDERES_FULL.remove(o); d['referidos'] += o['referidos']
        return {'ok': True, 'movidos': o['referidos'], 'activosMovidos': o['referidos'], 'origen': {'codigo': o['codigo'], 'documento': o['documento']}, 'destino': {'codigo': d['codigo'], 'nombre': d['nombre']}, 'docs': [], 'compromisosAbiertos': 0, 'solicitudesAbiertas': 0}
    if accion == 'priv.balances':
        meses = []
        for k, (m, t) in enumerate((('2026-10', 'Octubre 2026'), ('2026-09', 'Septiembre 2026'), ('2026-08', 'Agosto 2026'))):
            meses.append({'mes': m, 'mesTxt': t, 'pct': [61, 54, 47][k], 'lideres': 11, 'ref': [210, 176, 140][k], 'fechaCierre': '01/' + ['11', '10', '09'][k] + '/2026'})
        return {'ok': True, 'meses': meses}
    if accion == 'priv.balanceVer':
        items = []
        for l in LIDERES_FULL[:11]:
            r = max(0, round(l['referidos'] * .85)); f = round(r * .4)
            items.append({'codigo': l['codigo'], 'lider': l['nombre'], 'ref': r, 'firme': f, 'noVota': round(r * .07), 'noSeguro': round(r * .09), 'noSabe': round(r * .04), 'noContactado': round(r * .05), 'noFid': r - f - round(r * .25), 'pct': round((f + round(r * .25)) * 100 / r) if r else 0})
        return {'ok': True, 'items': items, 'mesTxt': 'Octubre 2026', 'total': len(items)}
    if accion == 'priv.lideresTablero':
        M = ['2026-06', '2026-07', '2026-08', '2026-09', '2026-10', '2026-11']; lid = {}; bal = {}
        for k, l in enumerate(LIDERES_FULL):
            ref = l['referidos']; parts = [0.08, 0.12, 0.18, 0.22, 0.24, 0.16]
            n = [round(ref * x) for x in parts]
            t = [ref, round(ref * .45), round(ref * .08), round(ref * .1), round(ref * .05), round(ref * .07), 0]
            lid[l['codigo']] = {'nom': l['nombre'], 'foto': '', 'cl': l['clasificacion'], 'on': l['activado'], 'n': n, 'al': [round(x * .3) for x in n], 'ae': [round(x * .2) for x in n], 'sf': 0, 't': t, 'st': [ref, 0, 0, 0], 'as': 0, 'inac': 0}
            bal[l['codigo']] = {}
            for j, m in enumerate(M[:-1]):
                r = sum(n[:j + 1]); f = round(r * (.25 + j * .04)); trab = round(r * (.4 + j * .06))
                bal[l['codigo']][m] = [r, f, round(r * .05), round(r * .05), round(r * .02), max(0, trab - f - round(r * .12)), r - trab, trab]
        return {'ok': True, 'meses': M, 'hoy': M[-1], 'lid': lid, 'bal': bal, 'val': {}, 'bit': {}, 'generado': 'hace un momento', 'rv': {}}
    if accion in ('priv.compromisos', 'priv.solicitudes'):
        return {'ok': True, 'items': [], 'rv': {}}
    FALTAN.append(accion)
    return {'ok': True, 'items': []}


def _ia_bd():
    n=len(PERSONAS); loc=sum(1 for x in PERSONAS if x['municipio']=='Villa Ejemplo')
    fir=[x for x in PERSONAS if x['intencion']=='Firme con el voto']; sinp=sum(1 for x in PERSONAS if not x['intencion'])
    pc=sum(1 for x in PERSONAS if x['municipio']=='POR CONFIRMAR')
    from collections import Counter
    top=Counter(x['residencia'] for x in fir).most_common(1)[0][0]
    return ("**Resumen de la base de datos**\n"
            f"- Tienes **{n} registros**; {loc} votan en Villa Ejemplo.\n"
            f"- **Firmes con el voto: {len(fir)}** ({round(len(fir)*100/n)} %). El barrio con más firmes es **{top}**.\n"
            f"- **{sinp} personas sin preguntar**: llámalas primero, son la mayor oportunidad.\n"
            f"- {pc} registros **por confirmar**: no aparecen en el censo; pide a su líder que los valide.")


IA_TEXTO = {'bd': _ia_bd()}


def _fila(d):
    return next((x for x in PERSONAS if x['documento'] == str(d)), None)


def _iso(dd, h='10:30'):
    return dd.strftime('%Y-%m-%d') + ' ' + h


def _traza(d):
    c = _fila(d) or {}
    lid = next((l for l in LIDERES if l['codigo'] == c.get('referencia')), None)
    persona = {'NOMBRE': c.get('nombre', ''), 'DOCUMENTO': d, 'CONTACTO': c.get('telefono', ''), 'RESIDENCIA': c.get('residencia', ''),
               'REFERENCIA': c.get('referencia', ''), 'LIDER': lid['nombre'] if lid else '', 'DEPARTAMENTO': 'DEPARTAMENTO EJEMPLO' if c.get('puestoCrudo') else '',
               'MUNICIPIO': c.get('municipio', ''), 'PUESTO': c.get('puestoCrudo', ''), 'DIRECCION': 'CALLE 5 # 3-10' if c.get('puestoCrudo') else '',
               'MESA': c.get('mesa', ''), 'ESTADO': c.get('estado', 'ACTIVO'), 'INTENCION': c.get('intencion', ''), 'FECHA_REGISTRO': c.get('fechaRegistro', ''),
               'FECHA_ACTUALIZACION': c.get('fechaActualizacion', '')}
    base = HOY - dt.timedelta(days=60)
    items = [
        {'k': 'formulario', 'tit': 'Inscripción: Jornada de salud', 'det': 'Se inscribió desde la app pública', 'est': 'CONFIRMADO', 'f': _iso(HOY - dt.timedelta(days=3), '09:15')},
        {'k': 'compromiso', 'tit': 'Arreglo del alumbrado de su calle', 'det': 'Gestionado con la junta de acción comunal', 'est': 'CUMPLIDO', 'f': _iso(HOY - dt.timedelta(days=9), '16:40')},
        {'k': 'evento', 'tit': 'Asistió: Encuentro con comerciantes', 'det': 'Plaza principal', 'est': '', 'f': _iso(HOY - dt.timedelta(days=16), '15:05')},
        {'k': 'servicio', 'tit': 'Servicio: Asesoría jurídica', 'det': 'Atendido por profesional de la casa social', 'est': 'ATENDIDO', 'f': _iso(HOY - dt.timedelta(days=24), '11:20')},
        {'k': 'datos', 'tit': 'Datos actualizados', 'det': 'Cambio de WhatsApp', 'est': '', 'f': _iso(HOY - dt.timedelta(days=33), '08:50')},
        {'k': 'lider', 'tit': 'Referido por ' + (lid['nombre'] if lid else 'un líder'), 'det': '', 'est': '', 'f': ''},
        {'k': 'alta', 'tit': 'Registro en la base de datos', 'det': 'Agregado desde el panel privado', 'est': '', 'f': _iso(base, '10:00')},
    ]
    return {'ok': True, 'persona': persona, 'esLider': bool(c.get('esLider')), 'items': items, 'total': len(items),
            'resumen': {'servicios': 1, 'serviciosAtendidos': 1, 'compromisos': 1, 'compromisosCumplidos': 1, 'eventos': 1, 'formularios': 1}, 'rv': {}}
