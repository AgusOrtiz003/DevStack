from nicegui import ui, app
from backend.turnos.listar_turnos import listar_reservas_turno
from backend.reservas.confirmar_reserva import confirmar_reserva

@ui.page('/listadoReservas/{idTurno}')
def pagina_listar_reservas_secretaria(idTurno: int):

    def logout():
        app.storage.user.clear()
        ui.navigate.to('/login')

    def recargar():
        reservas = listar_reservas_turno(idTurno)
        tabla_confirmadas.rows = [r for r in reservas if r['estado'] == 'Confirmado']
        tabla_pendientes.rows  = [r for r in reservas if r['estado'] == 'Pendiente']
        tabla_pagadas.rows     = [r for r in reservas if r['estado'] == 'Pagado']
        tabla_canceladas.rows  = [r for r in reservas if r['estado'] == 'Cancelado']
        tabla_confirmadas.update()
        tabla_pendientes.update()
        tabla_pagadas.update()
        tabla_canceladas.update()

    def realizar_check_in(idReserva):
        confirmar_reserva(idReserva)
        recargar()
        ui.notify('Check-in realizado', color='green')

    reservas = listar_reservas_turno(idTurno)
    confirmadas = [r for r in reservas if r['estado'] == 'Confirmado']
    pendientes = [r for r in reservas if r['estado'] == 'Pendiente']
    pagadas    = [r for r in reservas if r['estado'] == 'Pagado']
    canceladas = [r for r in reservas if r['estado'] == 'Cancelado']

    with ui.header().classes(replace='row items-center gap-4'):
        ui.button('Volver', icon='arrow_back').on('click', lambda: ui.navigate.back()).props('flat color=white')
        with ui.row().classes('ml-auto'):
            ui.button(icon='account_circle').props('flat color=white round')
            ui.button(on_click=logout, icon='logout').props('flat color=white round')

    with ui.column().classes('w-full p-4 gap-4'):

        ui.label(f'Reservas del turno #{idTurno}').classes('text-2xl font-bold')

        columnas = [
            {'name': 'dniPaciente',  'label': 'DNI Paciente',    'field': 'dniPaciente'},
            {'name': 'obraSocial',   'label': 'Obra Social',      'field': 'obraSocial'},
            {'name': 'metodoPago',   'label': 'Método de Pago',   'field': 'metodoPago'},
            {'name': 'estado',       'label': 'Estado',           'field': 'estado'},
            {'name': 'fechaCreacion','label': 'Fecha y Hora de Reserva',   'field': 'fechaCreacion'},
            {'name': 'accion',       'label': 'Acción',           'field': 'accion'},
        ]

        columnas_sin_accion = [c for c in columnas if c['name'] != 'accion']

        slot_check_in = r'''
            <q-td :props="props">
                <q-btn
                    label="Check-in"
                    color="positive"
                    flat
                    dense
                    icon="how_to_reg"
                    @click="$parent.$emit('check_in', props.row.idReserva)"
                />
            </q-td>
        '''

        # Confirmadas
        with ui.card().classes('w-full border-l-4 border-blue-400'):
            with ui.row().classes('items-center gap-2 px-4 pt-3 pb-1'):
                ui.icon('how_to_reg', size='sm').classes('text-blue-400')
                ui.label('Confirmadas').classes('text-base font-semibold text-blue-400')
                ui.badge(str(len(confirmadas)), color='blue').classes('ml-1')
            tabla_confirmadas = ui.table(columns=columnas_sin_accion, rows=confirmadas, row_key='idReserva').classes('w-full')
        
        # Pagadas
        with ui.card().classes('w-full border-l-4 border-green-500'):
            with ui.row().classes('items-center gap-2 px-4 pt-3 pb-1'):
                ui.icon('check_circle', size='sm').classes('text-green-500')
                ui.label('Pagadas').classes('text-base font-semibold text-green-600')
                ui.badge(str(len(pagadas)), color='green').classes('ml-1')
            tabla_pagadas = ui.table(columns=columnas, rows=pagadas, row_key='idReserva').classes('w-full')
            tabla_pagadas.add_slot('body-cell-accion', slot_check_in)
            tabla_pagadas.on('check_in', lambda e: realizar_check_in(e.args))

        # Pendientes
        with ui.card().classes('w-full border-l-4 border-orange-400'):
            with ui.row().classes('items-center gap-2 px-4 pt-3 pb-1'):
                ui.icon('schedule', size='sm').classes('text-orange-400')
                ui.label('Pendientes').classes('text-base font-semibold text-orange-400')
                ui.badge(str(len(pendientes)), color='orange').classes('ml-1')
            tabla_pendientes = ui.table(columns=columnas_sin_accion, rows=pendientes, row_key='idReserva').classes('w-full')
            tabla_pendientes.add_slot('body-cell-accion', slot_check_in)
            tabla_pendientes.on('check_in', lambda e: realizar_check_in(e.args))


        # Canceladas
        with ui.card().classes('w-full border-l-4 border-red-400'):
            with ui.row().classes('items-center gap-2 px-4 pt-3 pb-1'):
                ui.icon('cancel', size='sm').classes('text-red-400')
                ui.label('Canceladas').classes('text-base font-semibold text-red-400')
                ui.badge(str(len(canceladas)), color='red').classes('ml-1')
            tabla_canceladas = ui.table(columns=columnas_sin_accion, rows=canceladas, row_key='idReserva').classes('w-full')