from nicegui import ui

from nicegui import ui
from datetime import date, timedelta
from backend.reservas.registrar_reserva import registrar_reserva
from backend.turnos.listar_turnos import listar_los_turnos
from backend.exceptions.turno_lleno_exception import TurnoLlenoException
import sqlite3

# Página de registar reserva secretaria
def pagina_reservas_secretaria():
    metodos_pago = [
        'Efectivo',
        'Transferencia',
        'Billetera virtual'
    ]

    def actualizar_listado():
        tabla.rows = listar_los_turnos()
        tabla.update()

    async def reservar_turno(turno):
        obras = turno['obrasSociales'].split(', ')
        with ui.dialog() as dialog, ui.card().classes('w-100'):
            
            ui.label('Reservar turno').classes('text-xl font-bold')
            
            ui.separator()
            
            ui.label(
                f"{turno['fecha']} - {turno['hora']} - {turno['tratamiento']}"
            )
            dni_input = ui.input(
                label='DNI Paciente',
                placeholder='44555666',
                validation={'DNI no válido': lambda value: len(value) == 8}
            )
            obra_select = ui.select(
                options=obras,
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
                dni_input.value
            )
            ui.notify('Turno reservado con éxito',color='green-500')
        except sqlite3.IntegrityError:
            ui.notify('Turno ya reservado',color='red-500')
        except TurnoLlenoException:
            ui.notify('Turno lleno',color='red-500')
        except ValueError:
            ui.notify('El DNI no existe',color='red-500')

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
        {'name': 'obrasSociales', 'label': 'Obras sociales', 'field': 'obrasSociales'},
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