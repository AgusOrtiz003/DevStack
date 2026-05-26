from nicegui import ui
from backend.turnos.listar_turnos import listar_los_turnos
from frontend.reservas.listar_reservas_turno import pagina_listar_reservas_secretaria
import sqlite3
# Página de listar turnos con reservas
def pagina_listar_turnos_pendientes():
     
    def actualizar_listado():
        tabla.rows = listar_los_turnos()
        tabla.update()
        
    
    turnos=listar_los_turnos()
    # Parte central
    ui.button(icon='sync',on_click=lambda: actualizar_listado())
    tabla = ui.table(
    columns=[
        {'name': 'fecha', 'label': 'Fecha', 'field': 'fecha'},
        {'name': 'hora', 'label': 'Hora', 'field': 'hora'},
        {'name': 'tratamiento', 'label': 'Tratamiento', 'field': 'tratamiento'},
        {'name': 'cupoActual', 'label': 'Cupo Actual', 'field': 'cupoActual'},
        {'name': 'cupoMaximo', 'label': 'Cupo Maximo', 'field': 'cupoMaximo'},
        {'name': 'accion', 'label': 'Accion', 'field': 'accion'},
    ],
    rows=turnos,
    row_key='idReserva').classes('w-full overflow-hidden shadow-md')

    tabla.add_slot('body-cell-accion', r'''
        <q-td :props="props">
            <q-btn
                label="Ver reservas"
                color="primary"
                flat
                @click="$parent.$emit('ver_reservas', props.row.idTurno)"
            />
        </q-td>
    ''')

    tabla.on('ver_reservas',lambda e: ui.navigate.to(f'/listadoReservas/{e.args}'))

    return tabla
