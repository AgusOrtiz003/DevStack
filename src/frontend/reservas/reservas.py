from nicegui import ui, app
from backend.reservas.registrar_reserva import registrar_reserva
from backend.turnos.listar_turnos import listar_los_turnos
from backend.exceptions.turno_lleno_exception import TurnoLlenoException
from backend.reservas.listar_reservas import listar_reservas
from backend.listas_de_espera.agregar_a_lista_espera import agregar_a_lista_espera
from backend.turnos.verificar_cupo_disponible import verificar_cupo_disponible
from src.backend.reservas.registrar_reserva_recurrente import registrar_reservas_recurrentes
from datetime import datetime

import sqlite3


def pagina_reservas(tabla_principal):

    fecha_desde = None
    fecha_hasta = None

    fecha_desde_label = ui.label(
        'Fecha desde: no seleccionada'
    )

    fecha_hasta_label = ui.label(
        'Fecha hasta: no seleccionada'
    )

    async def seleccionar_fecha_desde():

        nonlocal fecha_desde

        with ui.dialog() as dialog, ui.card():

            calendario = ui.date()

            ui.button(
                'Aceptar',
                on_click=lambda: dialog.submit(
                    calendario.value
                )
            )

        resultado = await dialog

        if resultado:

            fecha_desde = resultado

            fecha_desde_label.set_text(
                f'Fecha desde: {resultado}'
            )

    async def seleccionar_fecha_hasta():

        nonlocal fecha_hasta

        with ui.dialog() as dialog, ui.card():

            calendario = ui.date()

            ui.button(
                'Aceptar',
                on_click=lambda: dialog.submit(
                    calendario.value
                )
            )

        resultado = await dialog

        if resultado:

            fecha_hasta = resultado

            fecha_hasta_label.set_text(
                f'Fecha hasta: {resultado}'
            )

    dias_semana = {
    0: 'Lunes',
    1: 'Martes',
    2: 'Miércoles',
    3: 'Jueves',
    4: 'Viernes',
    }

    turnos_originales = listar_los_turnos()


    def aplicar_filtros():

        if not fecha_desde:
            ui.notify(
                'Seleccione una fecha desde',
                color='red'
            )
            return


        if not fecha_hasta:
            ui.notify(
                'Seleccione una fecha hasta',
                color='red'
            )
            return


        fecha_desde_dt = datetime.strptime(
            fecha_desde,
            '%Y-%m-%d'
        )

        fecha_hasta_dt = datetime.strptime(
            fecha_hasta,
            '%Y-%m-%d'
        )

        if fecha_desde_dt > fecha_hasta_dt:

            ui.notify(
                'La fecha desde no puede ser mayor a la fecha hasta',
                color='red'
            )

            return

        if not dia_select.value:

            ui.notify(
                'Debe seleccionar un día',
                color='red'
            )

            return

        if not hora_select.value:

            ui.notify(
                'Debe seleccionar una hora',
                color='red'
            )

            return

        if not tratamiento_select.value:

            ui.notify(
                'Debe seleccionar un tratamiento',
                color='red'
            )

            return

        filtrados = []

        for turno in turnos_originales:

            fecha = datetime.strptime(
                turno['fecha'],
                '%d/%m/%Y'
            )

            fecha_turno = datetime.strptime(
                turno['fecha'],
                '%d/%m/%Y'
            )

            dia_turno = dias_semana.get(
                fecha.weekday()
            )

            if (
                dia_turno == dia_select.value
                and turno['hora'] == hora_select.value
                and turno['tratamiento'] == tratamiento_select.value
                and fecha_desde_dt <= fecha_turno <= fecha_hasta_dt

            ):
                filtrados.append(turno)

        tabla.rows = filtrados[:100]
        tabla.update()

    metodos_pago = [
        'Efectivo',
        'Transferencia',
        'Billetera virtual'
    ]
    obras_sociales = [
        'IOMA',
        'OSDE',
        'Particular'
    ]
    def actualizar_listado():
        todas = listar_reservas(dniPaciente)
        tabla_principal.rows = [r for r in todas if r['estado'] == 'Pendiente' and not r['idReservaRecurrente']]
        tabla_principal.update()
        tabla.rows = listar_los_turnos()[:100]
        tabla.update()

    async def reservar_turno(turno):
        with ui.dialog() as dialog, ui.card().classes('w-96'):

            with ui.row().classes('items-center gap-2'):
                ui.icon('event_available').classes('text-blue-400')
                ui.label('Reservar turno').classes('text-lg font-semibold')

            ui.separator()

            with ui.card().classes('w-full bg-blue-50'):
                with ui.grid(columns=2).classes('w-full gap-x-4 gap-y-1 text-sm'):
                    ui.label('Fecha:').classes('text-gray-500')
                    ui.label(turno['fecha'])

                    ui.label('Hora:').classes('text-gray-500')
                    ui.label(turno['hora'])

                    ui.label('Tratamiento:').classes('text-gray-500')
                    ui.label(turno['tratamiento'])

            obra_select = ui.select(
                options=obras_sociales,
                label='Obra social'
            ).classes('w-full').props('outlined')

            metodo_select = ui.select(
                options=metodos_pago,
                label='Método de pago'
            ).classes('w-full').props('outlined')

            with ui.row().classes('w-full justify-end gap-2 mt-2'):
                ui.button('Cancelar', on_click=lambda: dialog.submit(None)).props('flat')

                ui.button(
                    'Confirmar',
                    on_click=lambda: dialog.submit({
                        'obra': obra_select.value,
                        'metodo': metodo_select.value
                    })
                ).props('color=primary')

        resultado = await dialog

        if not resultado:
            return

        if not resultado.get('obra') or not resultado.get('metodo'):
            ui.notify('Seleccione todos los datos', color='red')
            return

        if verificar_cupo_disponible(turno['idTurno']):
            try:
                registrar_reserva(
                    turno['idTurno'],
                    resultado['obra'],
                    resultado['metodo'],
                    dniPaciente
                )

                ui.notify('Turno reservado con éxito', color='green')
                actualizar_listado()

            except sqlite3.IntegrityError:
                ui.notify('Ya tenés este turno reservado', color='red')

        else:

            with ui.dialog() as espera_dialog, ui.card().classes('w-96'):
                ui.label(
                    'El turno no tiene cupos disponibles. '
                    '¿Desea entrar en lista de espera?'
                )

                with ui.row().classes('w-full justify-end gap-2 mt-2'):
                    ui.button(
                        'No',
                        on_click=lambda: espera_dialog.submit(False)
                    ).props('flat')

                    ui.button(
                        'Sí',
                        on_click=lambda: espera_dialog.submit(True)
                    ).props('color=primary')

            if await espera_dialog:
                agregar_a_lista_espera(turno['idTurno'], dniPaciente,resultado['obra'], resultado['metodo'])
                ui.notify('Agregado a lista de espera', color='green')

    dniPaciente = app.storage.user.get('dni')
    turnos=listar_los_turnos()

    async def reservar_recurrente():

        if not dia_select.value or not hora_select.value:

            ui.notify(
                'Debe seleccionar día y hora',
                color='red-500'
            )

            return

        if tabla.rows == turnos_originales:
            ui.notify(
                'Debe aplicar los filtros antes de reservar recurrentemente',
                color='red-500'
            )
            return

        turnos_filtrados = tabla.rows

        if not turnos_filtrados:

            ui.notify(
                'No hay turnos para reservar',
                color='red-500'
            )

            return

        with ui.dialog() as dialog, ui.card().classes('w-100'):

            ui.label(
                f'Se reservarán {len(turnos_filtrados)} turnos'
            )

            obra_select = ui.select(
                options=obras_sociales,
                label='Obra social'
            ).classes('w-full')

            metodo_select = ui.select(
                options=metodos_pago,
                label='Método de pago'
            ).classes('w-full')

            with ui.row().classes('w-full justify-end'):

                ui.button(
                    'Cancelar',
                    on_click=lambda: dialog.submit(None)
                )

                ui.button(
                    'Confirmar',
                    on_click=lambda: dialog.submit({
                        'obra': obra_select.value,
                        'metodo': metodo_select.value
                    })
                )

        resultado = await dialog

        if not resultado:
            return

        try:

            ids_turnos = [
                turno['idTurno']
                for turno in turnos_filtrados
            ]

            registrar_reservas_recurrentes(
                ids_turnos,
                resultado['obra'],
                resultado['metodo'],
                dniPaciente
            )

            ui.notify(
                'Reserva recurrente creada',
                color='green-500'
            )

            actualizar_listado()

        except sqlite3.IntegrityError:

            ui.notify(
                'Ya posee alguno de esos turnos',
                color='red-500'
            )

        except TurnoLlenoException:

            ui.notify(
                'Uno de los turnos no tiene cupo recurrente',
                color='red-500'
            )

    with ui.row().classes('items-center gap-4 mb-4'):

        dia_select = ui.select(
            options=[
                'Lunes',
                'Martes',
                'Miércoles',
                'Jueves',
                'Viernes'
            ],
            label='Día'
        ).props('outlined').classes('w-50')

        hora_select = ui.select(
            options=[
                '13:00',
                '14:00',
                '15:00',
                '16:00',
                '17:00',
                '18:00',
                '19:00',
                '20:00'
            ],
            label='Hora'
        ).props('outlined').classes('w-50')

        tratamiento_select = ui.select(
            options=[
                'Tren superior',
                'Tren medio',
                'Tren inferior'
            ],
            label='Tratamiento'
        ).props('outlined').classes('w-50')

        ui.button(
            'Seleccionar fecha desde',
            on_click=seleccionar_fecha_desde
        )

        ui.button(
            'Seleccionar fecha hasta',
            on_click=seleccionar_fecha_hasta
        )


        ui.button(
            'Filtrar',
            icon='search',
            on_click=aplicar_filtros
        )

        def limpiar_filtros():

            dia_select.value = None
            hora_select.value = None
            tratamiento_select.value = None

            tabla.rows = turnos_originales[:100]
            tabla.update()

        ui.button(
            'Limpiar',
            icon='clear',
            on_click=limpiar_filtros
        )

        ui.button(
            'Reservar recurrente',
            icon='event_repeat',
            color='green',
            on_click=reservar_recurrente
        )
####################################### PÁGINA ##################################################
    # Parte central
    ui.label('Turnos disponibles').classes('text-2xl font-bold m-4')
    tabla = ui.table(
    columns=[
        {'name': 'fecha', 'label': 'Fecha', 'field': 'fecha'},
        {'name': 'dia', 'label': 'Día', 'field': 'dia'},
        {'name': 'hora', 'label': 'Hora', 'field': 'hora'},
        {'name': 'tratamiento', 'label': 'Tratamiento', 'field': 'tratamiento'},
        {'name': 'cupos', 'label': 'Cupos Disponibles', 'field': 'cupoActual'},
        {'name': 'cuposRecurrentes','label': 'Cupos Recurrentes Disponibles','field': 'cupoRecurrenteActual'},
        {'name': 'kinesiologos', 'label': 'Kinesiólogo/s', 'field': 'kinesiologos'},
        {'name': 'accion', 'label': 'Accion', 'field': 'accion'},
    ],
    rows=turnos[:100],
    row_key='idTurno').classes('w-full overflow-hidden shadow-md')



    with tabla.add_slot('top-left'):
        ui.button(icon='sync',on_click=lambda: actualizar_listado()).props('flat')

        tabla.add_slot('body-cell-accion', r'''
            <q-td :props="props">
                <q-btn
                    label="Reservar"
                    color="primary"
                    flat
                    @click="$parent.$emit('reservar', props.row)"
                />
            </q-td>
        ''')
        tabla.on('reservar', lambda e: reservar_turno(e.args))

    return tabla
