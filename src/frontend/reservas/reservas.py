from nicegui import ui, app
from backend.reservas.registrar_reserva import registrar_reserva
from backend.turnos.listar_turnos import listar_los_turnos
from backend.exceptions.turno_lleno_exception import TurnoLlenoException
from backend.reservas.listar_reservas import listar_reservas
import sqlite3

def pagina_reservas(tabla_principal):
    metodos_pago = ['Efectivo', 'Transferencia', 'Billetera virtual']
    obras_sociales = ['IOMA', 'OSDE', 'Particular']

    def actualizar_listado():
        todas = listar_reservas(dniPaciente)
        tabla_principal.rows = [r for r in todas if r['estado'] == 'Pendiente']
        tabla_principal.update()
        tabla.rows = listar_los_turnos()
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
                ui.button('Confirmar reserva', on_click=lambda: dialog.submit({
                    'obra': obra_select.value,
                    'metodo': metodo_select.value,
                })).props('color=primary')

        resultado = await dialog
        if not resultado:
            return
        if not resultado['obra'] or not resultado['metodo']:
            ui.notify('Seleccione todos los datos', color='red')
            return
        try:
            registrar_reserva(turno['idTurno'], resultado['obra'], resultado['metodo'], dniPaciente)
            ui.notify('Turno reservado con éxito', color='green')
            actualizar_listado()
        except sqlite3.IntegrityError:
            ui.notify('Ya tenés este turno reservado', color='red')
        except TurnoLlenoException:
            ui.notify('El turno está lleno', color='red')

    dniPaciente = app.storage.user.get('dni')
    turnos = listar_los_turnos()

    with ui.card().classes('w-full border-l-4 border-blue-400'):
        with ui.row().classes('items-center gap-2 px-4 pt-3 pb-1 justify-between'):
            with ui.row().classes('items-center gap-2'):
                ui.icon('event', size='sm').classes('text-blue-400')
                ui.label('Turnos disponibles').classes('text-base font-semibold text-blue-400')
                ui.badge(str(len(turnos)), color='blue').classes('ml-1')
            ui.button(icon='sync', on_click=actualizar_listado).props('flat round dense')

        tabla = ui.table(
            columns=[
                {'name': 'fecha',        'label': 'Fecha',              'field': 'fecha'},
                {'name': 'hora',         'label': 'Hora',               'field': 'hora'},
                {'name': 'tratamiento',  'label': 'Tratamiento',        'field': 'tratamiento'},
                {'name': 'cupos',        'label': 'Cupos disponibles',  'field': 'cupoActual'},
                {'name': 'kinesiologos', 'label': 'Kinesiólogo/s',      'field': 'kinesiologos'},
                {'name': 'accion',       'label': 'Acción',             'field': 'accion'},
            ],
            rows=turnos,
            row_key='idTurno'
        ).classes('w-full')

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