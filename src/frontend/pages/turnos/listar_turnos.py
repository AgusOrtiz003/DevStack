from nicegui import ui
from backend.listar_turnos_para_secretarias import listar_los_turnos
from backend.eliminar_turno import eliminar_turno_seleccionado
import sqlite3

# Página de listado de reservas pendientes
@ui.page('/listarTurnos')
def pagina_listar_turnos():
    # Columnas
    columnas = [
    {'name': 'id', 'label': 'ID', 'field': 'id'},
    {'name': 'fecha', 'label': 'Fecha', 'field': 'fecha'},
    {'name': 'hora', 'label': 'Hora', 'field': 'hora'},
    {'name': 'kinesiologo', 'label': 'Kinesiólogo/s', 'field': 'kinesiologo'},
    {'name': 'tratamiento', 'label': 'Tratamiento', 'field': 'tratamiento'},
    {'name': 'cupoActual', 'label': 'Cupo Actual', 'field': 'cupoActual'},
    {'name': 'cupoMaximo', 'label': 'Cupo Máximo', 'field': 'cupoMaximo'},
    ]

    # Datos
    turnos = listar_los_turnos()


####################################### PÁGINA ##################################################
    ui.page_title('Historial de Turnos')
    # Parte superior
    with ui.header().classes('items-center justify-between'):
        ui.button(icon='home',on_click=ui.navigate.back).props('flat color=white')
        with ui.row().classes('items-center gap-1'):
            ui.button(icon='account_circle').props('flat color=white')


    # Tabla
    tabla = ui.table(
        columns=columnas,
        rows=turnos,
        row_key='id',
        selection='single'
    ).classes('w-full')

    with ui.row():
        ui.button(
            'Modificar',
            icon='edit',
            #on_click=lambda:
            #modificar_turno(tabla.selected)
        )
        ui.button(
            'Eliminar',
            icon='delete',
            color='red',
            on_click=lambda: eliminar_turno_seleccionado(tabla)
)