from nicegui import ui
import sqlite3

# Página de listado de reservas pendientes
@ui.page('/listarTurnos')
def pagina_listar_turnos():

    def listar_los_turnos():
        conexion = sqlite3.connect('bdd.db')
        cursor = conexion.cursor()
        cursor.execute('SELECT id, fecha, hora, kinesiologo, tratamiento ,cupoActual, cupoMaximo FROM turnos')
        resultados = cursor.fetchall()
        conexion.close()
        turnos = []

        for fila in resultados:
            turnos.append({
                'id': fila[0],
                'fecha': fila[1],
                'hora': fila[2],
                'kinesiologo': fila[3],
                'tratamiento': fila[4],
                'cupoActual': fila[5],
                'cupoMaximo': fila[6]
            })
        conexion.close()
        return turnos

    ui.page_title('Historial de Turnos')
    # Parte superior
    with ui.header().classes('items-center justify-between'):
        ui.button(icon='home',on_click=ui.navigate.back).props('flat color=white')
        with ui.row().classes('items-center gap-1'):
            ui.button(icon='account_circle').props('flat color=white')

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
            #on_click=lambda:
            #eliminar_turno(tabla.selected)
        )