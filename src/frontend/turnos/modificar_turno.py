from nicegui import ui
from datetime import datetime
import sqlite3

from backend.turnos.listar_turnos import listar_los_turnos
from backend.kinesiologos.listar_kinesiologos import obtener_kinesiologos
from backend.turnos.modificar_turno import modificar_turno

def pagina_modificar_turno(tabla_principal):

    kinesiologos = {
        k[0]: f'{k[3]} {k[2]}'
        for k in obtener_kinesiologos()
    }
    
    def actualizar_listado():
        turnos = listar_los_turnos()
        tabla_principal.rows = turnos
        tabla_principal.update()
        tabla_modificar.rows = turnos
        tabla_modificar.update()

    async def modificar_turno_dialog(turno):
        with ui.dialog() as dialog, ui.card().classes('w-150'):

            ui.label('Modificar turno').classes('text-xl font-bold')
            ui.separator()
            ui.label(f'{turno["fecha"]} - {turno["hora"]}')

            kines_select = ui.select(
                options=kinesiologos,
                label='Kinesiólogo/s',
                value=turno['idsKinesiologos'],
                multiple=True,
                with_input=True
            ).classes('w-full').props(
                'outlined dense use-chips'
            )

            with ui.row().classes(
                'w-full justify-end'
            ):

                ui.button(
                    'Cancelar',
                    on_click=lambda: dialog.submit(None)
                ).props('flat')

                ui.button(
                    'Guardar',
                    on_click=lambda: dialog.submit({
                        'kinesiologos': kines_select.value,
                    })
                )

        resultado = await dialog

        if not resultado:
            return

        try:
            modificar_turno(
                turno['idTurno'],
                datetime.strptime(turno['fecha'],'%d/%m/%Y').strftime('%Y-%m-%d'),
                turno['hora'],
                resultado['kinesiologos'],
            )
            ui.notify('Turno modificado con éxito', color='green-500')
            actualizar_listado()
        except ValueError as e:
            ui.notify(str(e), color='red-500')

     
    turnos=listar_los_turnos()

    # Parte central
    tabla_modificar = ui.table(
    columns=[
        {'name': 'fecha', 'label': 'Fecha', 'field': 'fecha'},
        {'name': 'hora', 'label': 'Hora', 'field': 'hora'},
        {'name': 'tratamiento', 'label': 'Tratamiento', 'field': 'tratamiento'},
        {'name': 'cupoActual', 'label': 'Cupos disponibles', 'field': 'cupoActual'},
        {'name': 'cupoMaximo', 'label': 'Cupo máximo', 'field': 'cupoMaximo'},
        {'name': 'kinesiologos', 'label': 'Kinesiólogo/s', 'field': 'kinesiologos'},
        {'name': 'accion', 'label': 'Accion', 'field': 'accion'},
    ],
    rows=turnos,
    row_key='idReserva').classes('w-full overflow-hidden shadow-md')

    with tabla_modificar.add_slot('top-left'):
        ui.button(icon='sync',on_click=lambda: actualizar_listado()).props('flat')
    
    tabla_modificar.add_slot('body-cell-accion', r'''
        <q-td :props="props">
            <q-btn
                label="Modificar"
                color="primary"
                flat
                @click="$parent.$emit('modificar_turno', props.row)"
            />
        </q-td>
    ''')

    tabla_modificar.on('modificar_turno',lambda e: modificar_turno_dialog(e.args))

    return tabla_modificar