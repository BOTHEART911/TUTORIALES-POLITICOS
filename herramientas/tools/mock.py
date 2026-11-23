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
LIDERES = [{'codigo': str(k + 1), 'nombre': n} for k, n in enumerate(['Ana Rojas Peña', 'Jorge Castro León', 'Paola Vargas Cruz', 'Felipe Ortiz Ríos', 'Camila Peña Torres', 'Rosa León Duarte'])]
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
    if accion in ('priv.lideres', 'priv.compromisos', 'priv.solicitudes'):
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
