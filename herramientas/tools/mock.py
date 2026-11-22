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
    'departamento': 'Tu departamento', 'lugar': 'Villa Ejemplo', 'lema': 'Tu campaña',
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
        reg = HOY - dt.timedelta(days=random.randint(3, 200))
        p = {
            'documento': str(1000000100 + i * 37), 'nombre': nom, 'residencia': random.choice(BARRIOS),
            'municipio': mun, 'intencion': random.choice(INTEN), 'estado': 'ACTIVO',
            'fechaRegistro': _fecha(reg), 'fechaActualizacion': _fecha(reg + dt.timedelta(days=random.randint(0, 3))) if i % 3 == 0 else '',
            'esLider': i % 11 == 0, 'foto': '', 'puestoCrudo': random.choice(PUESTOS) if mun == 'Villa Ejemplo' else '',
            'mesa': str(random.randint(1, 18)) if mun == 'Villa Ejemplo' else '', 'motivo': 'NO APARECE EN EL CENSO' if mun == 'POR CONFIRMAR' else '',
            'telefono': '300' + str(5550000 + i),
        }
        out.append(p)
    out.sort(key=lambda x: x['nombre'])
    return out


PERSONAS = _personas()
LIDERES = [p for p in PERSONAS if p['esLider']]


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
        return {'ok': True, 'items': PERSONAS, 'lideres': [{'documento': l['documento'], 'nombre': l['nombre']} for l in LIDERES],
                'columnas': [], 'dash': {'puestos': PUESTOS, 'puestoOtro': 'OTRO MUNICIPIO'}, 'rv': {}, 'registraduriaUrl': ''}
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
