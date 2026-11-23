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
for _k, (_t, _l, _c, _i, _f) in enumerate([('Reunión con la junta de acción comunal', 'El Prado', 'Rosa León', '09:00', '10:30'), ('Visita a comerciantes del Centro', 'Centro', 'Paola Vargas', '15:30', '17:00')]):
    AGENDA.append({'id': 'AG1%02d' % _k, 'fecha': _fecha(dt.date.today()), 'inicia': _i, 'termina': _f, 'titulo': _t, 'lugar': _l, 'contacto': _c, 'estado': 'PROGRAMADA'})
for _a in AGENDA: _a.update({'telefono': '573005551' + str(100 + len(_a['id'])), 'detalles': 'Frente al parque principal', 'mensaje': 'Te esperamos puntual.', 'bitacora': '', 'idCalendar': 'cal', 'creada': _fecha(dt.date.today())})
EVENTOS = [{'id': str(30 + k), 'evento': e, 'fecha': _fecha(dt.date.today() + dt.timedelta(days=d)), 'inicia': i, 'termina': f, 'lugar': l, 'contacto': c, 'telefono': '573005552' + str(300 + k),
            'asistentes': a, 'estado': est, 'creada': _fecha(dt.date.today() - dt.timedelta(days=10)), 'mensaje': '', 'bitacora': ''}
           for k, (e, d, i, f, l, c, a, est) in enumerate([
               ('Gran encuentro de líderes', -12, '16:00', '19:00', 'Centro', 'Ana Rojas Peña', 86, 'TERMINADO'),
               ('Jornada de salud', -3, '08:00', '12:00', 'El Prado', 'Jorge Castro León', 54, 'TERMINADO'),
               ('Foro con jóvenes', 0, '18:00', '20:00', 'Las Palmas', 'Camila Peña Torres', 23, 'CORRIENDO'),
               ('Caminata por la vereda El Llano', 6, '07:00', '11:00', 'Vereda El Llano', 'Felipe Ortiz Ríos', 0, 'PROGRAMADO')])]


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
        return {'ok': True, 'candidato': {'nombre': 'Candidato Ejemplo', 'pnombre': 'Candidato', 'wa': '573005559999'}, 'manejo': 'Laura',
                'plantillas': {'resumen': 'Hola {pn_candidato}, {tiempo} 👋\nEstas son tus reuniones de {jornada}:\n{lista_reuniones}\n\nAgenda: {u_agenda}',
                               'aviso': '🔔 AVISO\n{bloque_aviso}', 'previa': '⏰ En 30 minutos:\n{bloque_aviso}', 'decision': '⚠️ Necesitamos tu decisión sobre:\n{bloque_aviso}',
                               'directo': 'Hola {contacto} 👋 Te confirmamos la reunión con {n_candidato}:\n🗓️ {fecha_larga} · {hora_inicio} a {hora_fin}\n📍 {lugar}\n{detalles}\n{mensaje}'}}
    if accion == 'priv.reunionMeta':
        return {'ok': True, 'invitados': 2}
    if accion == 'priv.reunionGuardar':
        c = dict(p, id='AG2%02d' % len(AGENDA), estado='PROGRAMADA', idCalendar='cal', creada=_fecha(dt.date.today())); c.pop('caller', None)
        AGENDA.append(c); return {'ok': True, 'card': c}
    if accion == 'priv.reunionVer':
        return {'ok': True, 'reunion': next(x for x in AGENDA if str(x['id']) == str(p.get('id')))}
    if accion == 'priv.reunionEstado':
        c = next(x for x in AGENDA if str(x['id']) == str(p.get('id'))); c['estado'] = p.get('estado'); return {'ok': True, 'card': c}
    if accion == 'priv.eventos':
        return {'ok': True, 'items': EVENTOS}
    if accion == 'priv.eventoVer':
        return {'ok': True, 'evento': next(x for x in EVENTOS if str(x['id']) == str(p.get('id')))}
    if accion == 'priv.eventoAsistentes':
        its = [{'nombre': x['nombre'], 'documento': x['documento'], 'contacto': x.get('telefono', ''), 'fecha': _fecha(dt.date.today() - dt.timedelta(days=3)) + ' 08:%02d' % (5 + k)} for k, x in enumerate(PERSONAS[:24])]
        return {'ok': True, 'items': its}
    if accion == 'priv.eventoMeta':
        return {'ok': True}
    if accion == 'priv.eventoGuardar':
        c = dict(p, id=str(30 + len(EVENTOS)), evento=p.get('evento') or p.get('nombre', ''), asistentes=0, estado='PROGRAMADO', creada=_fecha(dt.date.today())); c.pop('caller', None)
        EVENTOS.insert(0, c); return {'ok': True, 'card': c}
    if accion == 'priv.eventoEstado':
        c = next(x for x in EVENTOS if str(x['id']) == str(p.get('id'))); c['estado'] = p.get('estado'); return {'ok': True, 'card': c}
    if accion == 'priv.iaEstado':
        return {'ok': True, 'configurada': True}
    if accion == 'priv.vozEstado':
        return {'ok': True, 'configurada': False}
    if accion == 'priv.iaAnalizar':
        return {'ok': True, 'modelo': 'Análisis', 'generado': 'hace un momento', 'texto': IA_TEXTO.get(p.get('vista'), IA_TEXTO['bd'])}
    if accion == 'priv.lideres':
        return {'ok': True, 'items': LIDERES_FULL, 'columnas': [], 'rv': {}, 'plantillas': PLANT_LID}
    if accion == 'priv.liderReferidos':
        cod = str(p.get('codigo')); its = []
        for x in PERSONAS:
            if x.get('referencia') == cod and x['estado'] == 'ACTIVO':
                its.append({'documento': x['documento'], 'nombre': x['nombre'], 'contacto': x.get('telefono', ''), 'residencia': x['residencia'], 'municipio': x['municipio'], 'puesto': x['puestoCrudo'], 'mesa': x['mesa'], 'intencion': x['intencion'], 'foto': ''})
        return {'ok': True, 'items': its, 'columnas': [], 'rv': {}}
    if accion == 'priv.personaReasignarLote':
        for d in p.get('documentos', []):
            c = _fila(d)
            if c: c['referencia'] = str(p.get('referencia'))
        return {'ok': True, 'n': len(p.get('documentos', []))}
    if accion == 'priv.liderAhijados':
        cod = str(p.get('codigo')); pad = next(x for x in LIDERES_FULL if x['codigo'] == cod)
        aj = [{'codigo': x['codigo'], 'nombre': x['nombre'], 'referidos': x['referidos'], 'pct': x['pctTrabajo'], 'delegado': x['codigo'] in DELEG} for x in LIDERES_FULL if x['padrino'] == pad['nombre']]
        return {'ok': True, 'padrino': {'codigo': cod, 'nombre': pad['nombre']}, 'ahijados': aj, 'columna': True}
    if accion == 'priv.liderDelegar':
        (DELEG.add if p.get('on') else DELEG.discard)(str(p.get('ahijado'))); return {'ok': True}
    if accion == 'priv.liderAccion':
        return {'ok': True, 'msg': 'Enviado por el bot'}
    if accion == 'priv.liderMeses':
        cod = str(p.get('codigo')); l = next(x for x in LIDERES_FULL if x['codigo'] == cod); r0 = l['referidos']
        meses = [{'mes': '2026-%02d' % m, 'ref': round(r0 * f), 'trab': round(r0 * f * t), 'pct': round(t * 100), 'noFid': round(r0 * f * (1 - t))} for m, f, t in ((7, .4, .3), (8, .55, .42), (9, .7, .5), (10, .85, .61))]
        return {'ok': True, 'codigo': cod, 'meses': meses, 'bitacoras': BITS.get(cod, [])}
    if accion == 'priv.liderBitacoraGuardar':
        it = {'id': 'B%03d' % (len(BITS.get(str(p.get('codigo')), [])) + 50), 'mes': p.get('mes'), 'fecha': dt.datetime.now().strftime('%Y-%m-%d %H:%M'), 'autor': 'Laura Gómez Ruiz', 'refiere': p.get('refiere', ''), 'compromiso': p.get('compromiso', ''), 'texto': p.get('texto', ''), 'propia': True}
        BITS.setdefault(str(p.get('codigo')), []).insert(0, it); return {'ok': True, 'item': it}
    if accion == 'priv.liderBitacoraInforme':
        cols = ['codigo', 'mes', 'fecha', 'autor', 'refiere', 'compromiso', 'nota', 'editado']; filas = []
        for cod, its in BITS.items():
            for b in its: filas.append([cod, b['mes'], b['fecha'], b['autor'], b['refiere'], b['compromiso'], '', ''])
        ms = sorted(set(f[1] for f in filas), reverse=True)
        meses = [{'mes': m, 'n': sum(1 for f in filas if f[1] == m), 'lideres': len(set(f[0] for f in filas if f[1] == m)), 'cods': sorted(set(f[0] for f in filas if f[1] == m))} for m in ms]
        return {'ok': True, 'meses': meses, 'lideres': {l['codigo']: l['nombre'] for l in LIDERES_FULL}, 'completo': True, 'cols': cols, 'filas': filas}
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
    if accion == 'priv.contactoBuscar':
        q = str(p.get('q', '')).lower()
        its = [{'documento': x['documento'], 'nombre': x['nombre'], 'contacto': x.get('telefono', '')} for x in PERSONAS if q in x['nombre'].lower()][:8]
        return {'ok': True, 'items': its}
    if accion in ('priv.compromisos', 'priv.solicitudes'):
        L = COMP if accion == 'priv.compromisos' else SOLI
        cont = {}
        for x in L: cont[x['estado']] = cont.get(x['estado'], 0) + 1
        return {'ok': True, 'items': L, 'contadores': cont, 'plantilla': 'Hola [ASIGNADO] 👋 Te asignamos este compromiso con [NOMBRE]:%0A%0A[COMPROMISO]%0A%0APor favor cuéntanos cómo va.', 'rv': {}}
    if accion in ('priv.compromisoVer', 'priv.solicitudVer'):
        L = COMP if 'compromiso' in accion else SOLI; k = 'compromiso' if 'compromiso' in accion else 'solicitud'
        return {'ok': True, k: next(x for x in L if str(x['id']) == str(p.get('id')))}
    if accion in ('priv.compromisoGuardar', 'priv.solicitudGuardar'):
        L = COMP if 'compromiso' in accion else SOLI
        lid = next((l for l in LIDERES_FULL if l['nombre'] == p.get('asignado')), None)
        per = _fila(p.get('nombreDoc')) or {}
        c = {'id': str(500 + len(L)), 'nombre': p.get('nombre', ''), 'residencia': per.get('residencia', ''), 'compromiso': p.get('compromiso', ''), 'solicitud': p.get('solicitud', ''),
             'asignado': p.get('asignado', ''), 'telefono': '573005551234', 'estado': 'ASIGNADO', 'usuarioNombre': 'Laura Gómez Ruiz', 'ts': int(dt.datetime.now().timestamp()*1000), 'traza': [], 'trazaResumen': '', 'foto': '', 'fotoAsg': '', 'contacto': per.get('telefono', '')}
        if p.get('bitacora'): c['traza'] = [{'autor': 'Laura Gómez Ruiz', 'fecha': 'hoy', 'texto': p['bitacora'], 'origen': 'priv'}]
        L.insert(0, c); return {'ok': True, 'card': c}
    if accion in ('priv.compromisoEstado', 'priv.solicitudEstado'):
        L = COMP if 'compromiso' in accion else SOLI; c = next(x for x in L if str(x['id']) == str(p.get('id'))); c['estado'] = p.get('estado'); return {'ok': True, 'card': c}
    if accion in ('priv.compromisoTraza', 'priv.solicitudTraza'):
        L = COMP if 'compromiso' in accion else SOLI; c = next(x for x in L if str(x['id']) == str(p.get('id')))
        c['traza'] = c.get('traza', []) + [{'autor': 'Laura Gómez Ruiz', 'fecha': dt.datetime.now().strftime('%d/%m/%Y %I:%M %p').lower(), 'texto': p.get('texto', ''), 'origen': 'priv'}]
        c['trazaResumen'] = 'Última: ' + p.get('texto', '')[:40]
        return {'ok': True, 'entries': c['traza'], 'resumen': c['trazaResumen'], 'card': c}
    if accion in ('priv.compromisoWaBot', 'priv.solicitudWaBot'):
        return {'ok': True, 'msg': 'Enviado por el bot de WhatsApp'}
    if accion == 'priv.formularios':
        return {'ok': True, 'items': FORMS}
    if accion == 'priv.formImagen':
        return {'ok': True, 'id': 'img_nueva'}
    if accion == 'priv.formGuardar':
        it = {'id': 'F' + str(10 + len(FORMS)), 'nombre': p.get('nombre', ''), 'estado': 'CREADO', 'imagen': '/__assets/form5.jpg' if (p.get('imagenId') or p.get('imagen')) and p.get('imagen') != 'QUITAR' else '',
              'n': 0, 'cupo': p.get('cupo') or '', 'cierre': p.get('cierre') or '', 'varios': bool(p.get('varios')), 'menores': bool(p.get('menores')),
              'campos': p.get('campos') or [], 'creado': _ahora(), 'autor': 'Laura Gómez Ruiz', 'slug': 'nuevo', 'editable': True}
        FORMS.insert(0, it); return {'ok': True, 'item': it}
    if accion == 'priv.formEncender':
        it = next(x for x in FORMS if x['id'] == p.get('id')); it.update(estado='ENCENDIDO', encendido=_ahora(), ajustable=True); return {'ok': True, 'item': it}
    if accion == 'priv.formApagar':
        it = next(x for x in FORMS if x['id'] == p.get('id')); it.update(estado='APAGADO', apagado=_ahora()); return {'ok': True, 'item': it}
    if accion == 'priv.formRegistros':
        f = next((x for x in FORMS if x['id'] == p.get('id')), FORMS[0])
        return {'ok': True, 'items': FREG.get(f['id'], []), 'form': {'nombre': f['nombre'], 'campos': f['campos'], 'marcable': True},
                'wa': {'plantilla': 'Hola {nombre_corto} 👋, te escribe {Usuario_app} del equipo de {nombre_candidato}.\n\nRecibimos tu inscripción en *{nombre_formulario}*. ¿Nos confirmas tu asistencia?', 'candidato': 'Candidato Ejemplo'}}
    if accion == 'priv.formMarcar':
        return {'ok': True, 'conf': {'por': 'Laura Gómez Ruiz', 'fecha': _ahora()} if p.get('accion') == 'confirmar' else None}
    if accion == 'priv.formAgregarBd':
        lid = next((l for l in LIDERES_FULL if l['codigo'] == str(p.get('referencia'))), LIDERES_FULL[0])
        docs = p.get('documentos') or []
        if isinstance(docs, str):
            import json as _j
            try: docs = _j.loads(docs)
            except Exception: docs = docs.split(',')
        return {'ok': True, 'lider': {'codigo': lid['codigo'], 'nombre': lid['nombre']}, 'agregados': docs, 'yaEstaban': [], 'n': len(docs)}
    if accion == 'priv.notificaciones':
        cont = {}
        for x in NOTIS: cont[x['estado']] = cont.get(x['estado'], 0) + 1
        return {'ok': True, 'items': NOTIS, 'contadores': cont, 'alcance': 1240, 'pushTitulo': 'Candidato Ejemplo', 'firebaseListo': True}
    if accion == 'priv.notifVer':
        return {'ok': True, 'noticia': next(x for x in NOTIS if str(x['id']) == str(p.get('id')))}
    if accion == 'priv.notifGuardar':
        n = {'id': str(900 + len(NOTIS)), 'titulo': p.get('titulo', ''), 'cuerpo': p.get('cuerpo', ''), 'enlace': p.get('enlace', ''), 'estado': 'PUBLICADA' if p.get('enviar') else 'BORRADOR',
             'fecha': dt.datetime.now().strftime('%d/%m/%Y %H:%M'), 'ts': int(dt.datetime.now().timestamp() * 1000), 'enviados': 1238 if p.get('enviar') else 0, 'fallidos': 2 if p.get('enviar') else 0}
        NOTIS.insert(0, n); return {'ok': True, 'card': n, 'push': {'enviados': 1238} if p.get('enviar') else None}
    if accion in ('priv.lideres_x',):
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


PLANT_LID = {
    'codigo': 'Hola [NOMBRE] 👋 Bienvenido(a) al equipo de Candidato Ejemplo. Tu número de líder es *[CODIGO]*. Entra a la app pública, zona de líderes, con tu documento y empieza a registrar a tus referidos.',
    'tarea': '¡Gracias, [NOMBRE]! Ya vas con *[REFERIDOS] referidos*. Tu trabajo hace la diferencia. ¡Sigamos!',
    'notarea': 'Hola [NOMBRE], te recordamos la meta de referidos de este mes. Hoy tienes [REFERIDOS]. ¿Te ayudamos a avanzar?'}
DELEG = set()
BITS = {'2': [
    {'id': 'B001', 'mes': '2026-10', 'fecha': '2026-10-21 18:40', 'autor': 'Laura Gómez Ruiz', 'refiere': 'Reunión con 12 vecinos del barrio La Esperanza.', 'compromiso': 'Traer el listado de la junta antes del viernes.', 'texto': '', 'propia': True},
    {'id': 'B002', 'mes': '2026-09', 'fecha': '2026-09-14 10:05', 'autor': 'Laura Gómez Ruiz', 'refiere': 'Visita casa a casa en la calle 8.', 'compromiso': 'Llamar a los 5 no contactados.', 'texto': '', 'propia': True}],
    '1': [{'id': 'B003', 'mes': '2026-10', 'fecha': '2026-10-02 17:20', 'autor': 'Laura Gómez Ruiz', 'refiere': 'Encuentro con madres comunitarias.', 'compromiso': 'Agendar jornada de salud.', 'texto': '', 'propia': True}]}


def _cm(k, nom, res, txt, asg, est, dias, traza=None):
    return {'id': str(k), 'nombre': nom, 'residencia': res, 'compromiso': txt, 'asignado': asg, 'telefono': '57300555' + str(4000 + k), 'estado': est,
            'usuarioNombre': 'Laura Gómez Ruiz', 'ts': int((dt.datetime.now() - dt.timedelta(days=dias)).timestamp()*1000), 'traza': traza or [], 'trazaResumen': '', 'foto': '', 'fotoAsg': '', 'contacto': '57300555' + str(5000 + k)}
COMP = [
    _cm(1, 'María Peña Rojas', 'El Prado', 'Gestionar el arreglo de la luminaria de la calle 8.', 'Jorge Castro León', 'PENDIENTE', 12, [{'autor': 'Jorge Castro León', 'fecha': '10/11/2026 5:20 p. m.', 'texto': 'Ya se radicó la solicitud en la empresa de energía.', 'origen': 'pub'}]),
    _cm(2, 'Héctor Duarte Cano', 'Centro', 'Acompañar la inscripción del hijo al programa de becas.', 'Ana Rojas Peña', 'CUMPLIDO', 20),
    _cm(3, 'Gloria Silva Arias', 'Las Palmas', 'Llevar la propuesta del parque al concejo.', 'Paola Vargas Cruz', 'ASIGNADO', 3),
    _cm(4, 'Nelson Ríos Moreno', 'Vereda El Llano', 'Revisar el estado de la vía veredal con la alcaldía.', 'Felipe Ortiz Ríos', 'PENDIENTE', 41),
    _cm(5, 'Sandra Cruz León', 'San José', 'Conseguir cupo en la jornada de salud.', 'Camila Peña Torres', 'CUMPLIDO', 9),
    _cm(6, 'Iván Torres Mejía', 'La Esperanza', 'Gestionar arreglo del alcantarillado.', 'Jorge Castro León', 'DESCARTADO', 30)]
def _sl(k, txt, asg, est, dias):
    c = _cm(k, '', '', '', asg, est, dias); c['solicitud'] = txt; return c
SOLI = [_sl(101, 'Convocar a tus referidos a la caminata del sábado.', 'Ana Rojas Peña', 'ASIGNADO', 1),
        _sl(102, 'Actualizar la intención de voto de tus referidos sin preguntar.', 'Jorge Castro León', 'PENDIENTE', 6),
        _sl(103, 'Enviar fotos de la reunión del barrio para redes.', 'Paola Vargas Cruz', 'CUMPLIDO', 10)]


def _ahora():
    return dt.datetime.now().strftime('%Y-%m-%d %H:%M')
def _dias(d, h='09:00'):
    return (dt.date.today() + dt.timedelta(days=d)).strftime('%Y-%m-%d') + ' ' + h
_C1 = [{'id': 'c1', 'tipo': 'unica', 'etiqueta': '¿Qué jornada prefieres?', 'req': True, 'opciones': ['Mañana', 'Tarde']},
       {'id': 'c2', 'tipo': 'numero', 'etiqueta': '¿Cuántas personas de tu familia asisten?', 'req': False, 'entero': True, 'min': 1, 'max': 6}]
FORMS = [
    {'id': 'F1', 'nombre': 'Jornada de salud oral', 'estado': 'ENCENDIDO', 'imagen': '/__assets/form1.jpg', 'n': 16, 'cupo': 40, 'cierre': _dias(6, '18:00'), 'campos': _C1,
     'creado': _dias(-9), 'encendido': _dias(-8), 'autor': 'Laura Gómez Ruiz', 'slug': 'salud-oral', 'ajustable': True},
    {'id': 'F2', 'nombre': 'Curso de modistería', 'estado': 'ENCENDIDO', 'imagen': '/__assets/form2.jpg', 'n': 23, 'cupo': 30, 'espera': 2, 'campos': [], 'creado': _dias(-15), 'encendido': _dias(-14), 'autor': 'Diego Rincón', 'slug': 'modisteria', 'ajustable': True},
    {'id': 'F3', 'nombre': 'Caminata ecológica', 'estado': 'APAGADO', 'imagen': '/__assets/form3.jpg', 'n': 112, 'campos': [], 'varios': True, 'creado': _dias(-40), 'apagado': _dias(-20), 'autor': 'Laura Gómez Ruiz', 'slug': 'caminata'},
    {'id': 'F4', 'nombre': 'Torneo de microfútbol', 'estado': 'CREADO', 'imagen': '/__assets/form4.jpg', 'n': 0, 'cupo': 16, 'campos': [], 'creado': _dias(-1), 'autor': 'Laura Gómez Ruiz', 'slug': 'torneo', 'editable': True}]
def _freg():
    out = []; lid = LIDERES_FULL
    for i, x in enumerate(PERSONAS[5:21]):
        bd = {'lider': lid[i % 5]['nombre'], 'ref': lid[i % 5]['codigo']} if i % 3 != 0 else None
        out.append({'documento': x['documento'], 'nombre': x['nombre'], 'whatsapp': '300555' + str(7000 + i), 'residencia': x['residencia'], 'fecha': _dias(-(i % 7), '1%d:%02d' % (i % 9, (i * 7) % 60)),
                    'codigo': 'SO-%03d' % (16 - i), 'bd': bd, 'conf': {'por': 'Diego Rincón', 'fecha': _dias(-1, '16:20')} if i in (1, 4) else None,
                    'estado': 'ESPERA' if i == 15 else '', 'r': {'c1': 'Mañana' if i % 2 else 'Tarde', 'c2': 1 + i % 4}})
    return out
FREG = {'F1': _freg()}
NOTIS = [
    {'id': '801', 'titulo': 'Gracias, El Prado', 'cuerpo': 'Más de 200 vecinos nos acompañaron este sábado.\nSeguimos recorriendo barrio por barrio.', 'enlace': 'https://facebook.com/ejemplo', 'estado': 'PUBLICADA',
     'fecha': (dt.datetime.now() - dt.timedelta(days=2)).strftime('%d/%m/%Y %H:%M'), 'ts': int((dt.datetime.now() - dt.timedelta(days=2)).timestamp() * 1000), 'enviados': 1196, 'fallidos': 4},
    {'id': '802', 'titulo': 'Agenda de la semana', 'cuerpo': 'Lunes: Centro.\nMiércoles: Las Palmas.\nViernes: Vereda El Llano.', 'enlace': '', 'estado': 'BORRADOR',
     'fecha': (dt.datetime.now() - dt.timedelta(days=1)).strftime('%d/%m/%Y %H:%M'), 'ts': int((dt.datetime.now() - dt.timedelta(days=1)).timestamp() * 1000), 'enviados': 0},
    {'id': '803', 'titulo': 'Nuevo punto de inscripción', 'cuerpo': 'Ya puedes inscribirte en la sede del barrio San José.', 'enlace': 'https://instagram.com/ejemplo', 'estado': 'PUBLICADA',
     'fecha': (dt.datetime.now() - dt.timedelta(days=6)).strftime('%d/%m/%Y %H:%M'), 'ts': int((dt.datetime.now() - dt.timedelta(days=6)).timestamp() * 1000), 'enviados': 1102, 'fallidos': 0}]
