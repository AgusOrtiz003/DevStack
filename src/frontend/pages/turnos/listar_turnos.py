from nicegui import ui
from backend.listar_turnos_para_secretarias import listar_los_turnos
from backend.eliminar_turno import eliminar_turno_seleccionado
from backend.turno_pendiente import turno_pendiente
from backend.verificar_cupo_disponible import verificar_cupo_disponible
import sqlite3

DB_PATH = 'src/backend/bdd.db'



def actualizar_turno(
    id_turno,
    fecha,
    hora,
    tratamiento,
    cupo_maximo
):
    with sqlite3.connect(DB_PATH) as conexion:
        cursor = conexion.cursor()
        cursor.execute("""
            UPDATE turnos
            SET fecha = ?, hora = ?, tratamiento = ?, cupoMaximo = ?
            WHERE id = ?
        """, (
            fecha,
            hora,
            tratamiento,
            cupo_maximo,
            id_turno
        ))
        conexion.commit()


@ui.page('/listarTurnos')
def pagina_listar_turnos():

    columnas = [
        {'name': 'id', 'label': 'ID', 'field': 'id'},
        {'name': 'fecha', 'label': 'Fecha', 'field': 'fecha'},
        {'name': 'hora', 'label': 'Hora', 'field': 'hora'},
        {'name': 'kinesiologo', 'label': 'Kinesiólogo/s', 'field': 'kinesiologo'},
        {'name': 'tratamiento', 'label': 'Tratamiento', 'field': 'tratamiento'},
        {'name': 'cupoActual', 'label': 'Cupo Actual', 'field': 'cupoActual'},
        {'name': 'cupoMaximo', 'label': 'Cupo Máximo', 'field': 'cupoMaximo'},
    ]

    def cargar_tabla(data=None):
        tabla.rows = data if data is not None else listar_los_turnos()
        tabla.update()


    ui.page_title('Historial de Turnos')

    with ui.header().classes('items-center justify-between'):

        ui.button(
            icon='home',
            on_click=ui.navigate.back
        ).props('flat color=white')

        with ui.row().classes('items-center gap-1'):
            ui.button(icon='account_circle').props('flat color=white')
    ################################ TABLA ################################

    tabla = ui.table(
        columns=columnas,
        rows=listar_los_turnos(),
        row_key='id',
        selection='single'
    ).classes('w-full')

    ################################ FILTROS ################################

    def mostrar_todos():
        cargar_tabla()

    def mostrar_pendientes():
        cargar_tabla([
            t for t in listar_los_turnos()
            if turno_pendiente(t['id'])
        ])

    def mostrar_disponibles():
        cargar_tabla([
            t for t in listar_los_turnos()
            if verificar_cupo_disponible(t['id'])
        ])

    def mostrar_ocupados():
        cargar_tabla([
            t for t in listar_los_turnos()
            if not verificar_cupo_disponible(t['id'])
        ])

    ################################ DIALOG ################################

    dialogo = ui.dialog()

    with dialogo, ui.card().classes('w-96'):

        ui.label('Modificar Turno').classes('text-h6')

        ui.label('Fecha')
        input_fecha = ui.date().props('mask=YYYY-MM-DD')

        horas_disponibles = [
            '08:00','08:30','09:00','09:30','10:00','10:30',
            '11:00','11:30','12:00','12:30','13:00','13:30',
            '14:00','14:30','15:00','15:30','16:00','16:30',
            '17:00','17:30','18:00','18:30','19:00','19:30','20:00'
        ]

        ui.label('Hora')
        input_hora = ui.select(horas_disponibles).props('outlined dense')

        tratamientos = ['Tren superior', 'Tren medio', 'Tren inferior']

        input_tratamiento = ui.select(
            tratamientos,
            label='Tratamiento'
        ).props('outlined dense')

        input_cupo_maximo = ui.number('Cupo Máximo')

        turno_id = {'valor': None}

        def guardar_cambios():

            if (
                not input_fecha.value or
                not input_hora.value or
                not input_tratamiento.value or
                not input_cupo_maximo.value
            ):
                ui.notify('Completá todos los campos', color='red')
                return

            actualizar_turno(
                id_turno=turno_id['valor'],
                fecha=input_fecha.value,
                hora=input_hora.value,
                tratamiento=input_tratamiento.value,
                cupo_maximo=input_cupo_maximo.value
            )

            cargar_tabla()
            dialogo.close()

            ui.notify('Turno modificado correctamente', color='green')

        with ui.row().classes('w-full justify-end'):

            ui.button('Cancelar', on_click=dialogo.close).props('flat')

            ui.button('Guardar', icon='save', on_click=guardar_cambios)

    ################################ MODIFICAR ################################

    def abrir_modificacion():

        if not tabla.selected:
            ui.notify('Seleccioná un turno', color='red')
            return

        turno = tabla.selected[0]

        turno_id['valor'] = turno['id']
        input_fecha.value = turno['fecha']
        input_hora.value = turno['hora'][:5]
        input_tratamiento.value = turno['tratamiento']
        input_cupo_maximo.value = turno['cupoMaximo']

        dialogo.open()

    ################################ BOTONES ################################

    with ui.row():

        ui.button('Modificar', icon='edit', on_click=abrir_modificacion)

        ui.button(
            'Eliminar',
            icon='delete',
            color='red',
            on_click=lambda: eliminar_turno_seleccionado(tabla)
        )

    ################################ FILTROS UI ################################

    ui.separator()

    with ui.row():

        ui.button('Todos', icon='list', on_click=mostrar_todos)

        ui.button('Turnos Pendientes', icon='schedule',
                   color='blue', on_click=mostrar_pendientes)

        ui.button('Turnos Disponibles', icon='event_available',
                   color='green', on_click=mostrar_disponibles)

        ui.button('Turnos Ocupados', icon='event_busy',
                   color='red', on_click=mostrar_ocupados)