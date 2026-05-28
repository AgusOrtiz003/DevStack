from nicegui import ui

from backend.turnos.listar_turnos import listar_los_turnos
from backend.turnos.eliminar_turno import eliminar_turno

def pagina_cancelar_turno():

    async def cancelar_turno(turno):
        with ui.dialog() as dialog, ui.card():

            ui.label(
                f'¿Cancelar turno del {turno["fecha"]}?'
            )

            with ui.row().classes('w-full justify-center gap-2'):

                ui.button(
                    'Si',
                    on_click=lambda: dialog.submit(True)
                ).props('color=red-500')

                ui.button(
                    'No',
                    on_click=lambda: dialog.submit(False)
                ).props('flat')

        resultado = await dialog

        if not resultado:
            return

        eliminar_turno(turno['idTurno'])

        actualizar_listado()

        ui.notify(
            'Turno cancelado',
            color='green-500'
        )

    def actualizar_listado():
        tabla.rows = listar_los_turnos()
        tabla.update()

    turnos = listar_los_turnos()
    
    # Parte central
    ui.label(
        'Gestión de Turnos'
    ).classes('text-3xl font-bold')
    ui.separator()
    
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
                label="Cancelar Turno"
                color="negative"
                flat
                @click="$parent.$emit('cancelar', props.row)"
            />
        </q-td>
    ''')

    tabla.on(
        'cancelar',
        lambda e: cancelar_turno(e.args)
    )

    return tabla