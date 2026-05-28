from nicegui import ui, app
from backend.reservas.registrar_reserva import registrar_reserva
from backend.turnos.listar_turnos import listar_los_turnos
from backend.exceptions.turno_lleno_exception import TurnoLlenoException
import sqlite3

# Página de registar reserva
def pagina_reservas(tabs,reservas_tab,tabla_reservas):
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
        tabla.rows = listar_los_turnos()
        tabla.update()

    async def reservar_turno(turno):
        with ui.dialog() as dialog, ui.card().classes('w-100'):
            
            ui.label('Reservar turno').classes('text-xl font-bold')
            
            ui.separator()
            
            ui.label(
                f"{turno['fecha']} - {turno['hora']} - {turno['tratamiento']}"
            )

            obra_select = ui.select(
                options=obras_sociales,
                label='Obra social'
            ).classes('w-full').props('outlined')

            metodo_select = ui.select(
                options=metodos_pago,
                label='Método de pago'
            ).classes('w-full').props('outlined')
            with ui.row().classes('w-full justify-end'):
                ui.button(
                    'Cancelar',
                    on_click=lambda: dialog.submit(None)
                ).props('flat')
                ui.button(
                    'Confirmar',
                    on_click=lambda: dialog.submit({
                        'obra': obra_select.value,
                        'metodo': metodo_select.value,
                    })
                )
        resultado = await dialog
        if not resultado:
            return
        if not resultado['obra'] or not resultado['metodo']:
            ui.notify('Seleccione los datos',color='red-500')
            return
        try:
            registrar_reserva(
                turno['idTurno'],
                resultado['obra'],
                resultado['metodo'],
                dniPaciente
            )
            ui.notify('Turno reservado con éxito',color='green-500')
        except sqlite3.IntegrityError:
            ui.notify('Turno ya reservado',color='red-500')
        except TurnoLlenoException:
            ui.notify('Turno lleno',color='red-500')

    dniPaciente = app.storage.user.get('dni')
    turnos=listar_los_turnos()
####################################### PÁGINA ##################################################
    # Parte central
    ui.label('Turnos disponibles').classes('text-2xl font-bold m-4')
    tabla = ui.table(
    columns=[
        {'name': 'fecha', 'label': 'Fecha', 'field': 'fecha'},
        {'name': 'hora', 'label': 'Hora', 'field': 'hora'},
        {'name': 'tratamiento', 'label': 'Tratamiento', 'field': 'tratamiento'},
        {'name': 'cupos', 'label': 'Cupos Disponibles', 'field': 'cupoActual'},
        {'name': 'kinesiologos', 'label': 'Kinesiólogo/s', 'field': 'kinesiologos'},
        {'name': 'accion', 'label': 'Accion', 'field': 'accion'},
    ],
    rows=turnos,
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

    tabla.on(
        'reservar',
        lambda e: reservar_turno(e.args)
    )

    return tabla

