from nicegui import ui
from backend.listar_turnos_para_secretarias import listar_los_turnos
from backend.eliminar_turno import eliminar_turno_seleccionado
import sqlite3

DB_PATH = 'src/backend/bdd.db'


def actualizar_turno(
    id_turno,
    fecha,
    hora,
    tratamiento,
    cupo_maximo
):
    conexion = sqlite3.connect(DB_PATH)

    cursor = conexion.cursor()

    cursor.execute("""
        UPDATE turnos
        SET
            fecha = ?,
            hora = ?,
            tratamiento = ?,
            cupoMaximo = ?
        WHERE id = ?
    """, (
        fecha,
        hora,
        tratamiento,
        cupo_maximo,
        id_turno
    ))

    conexion.commit()
    conexion.close()


# Página de listado de reservas pendientes
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

    turnos = listar_los_turnos()

####################################### PÁGINA ##################################################

    ui.page_title('Historial de Turnos')

    with ui.header().classes('items-center justify-between'):

        ui.button(
            icon='home',
            on_click=ui.navigate.back
        ).props('flat color=white')

        with ui.row().classes('items-center gap-1'):
            ui.button(icon='account_circle').props('flat color=white')

    tabla = ui.table(
        columns=columnas,
        rows=turnos,
        row_key='id',
        selection='single'
    ).classes('w-full')

####################################### DIALOG MODIFICAR ########################################

    dialogo = ui.dialog()

    with dialogo, ui.card().classes('w-96'):

        ui.label('Modificar Turno').classes('text-h6')

        ui.label('Fecha')
        input_fecha = ui.date().props(
            'mask=YYYY-MM-DD'
        )

        # 🔽 DROPDOWN SIMPLE DE HORAS
        horas_disponibles = [
            '08:00', '08:30',
            '09:00', '09:30',
            '10:00', '10:30',
            '11:00', '11:30',
            '12:00', '12:30',
            '13:00', '13:30',
            '14:00', '14:30',
            '15:00', '15:30',
            '16:00', '16:30',
            '17:00', '17:30',
            '18:00', '18:30',
            '19:00', '19:30',
            '20:00'
        ]
        
        ui.label('Hora')
        input_hora = ui.select(
        horas_disponibles
        ).props('outlined dense')

        tratamientos = [
            'Tren superior',
            'Tren medio',
            'Tren inferior'
        ]   

        input_tratamiento = ui.select(
            tratamientos,
            label='Tratamiento'
        ).props('outlined dense')
        
        input_cupo_maximo = ui.number(
            'Cupo Máximo'
        )

        turno_id = {'valor': None}

####################################### GUARDAR #################################################

        def guardar_cambios():

            actualizar_turno(
                id_turno=turno_id['valor'],
                fecha=input_fecha.value,
                hora=input_hora.value,
                tratamiento=input_tratamiento.value,
                cupo_maximo=input_cupo_maximo.value
            )

            tabla.rows = listar_los_turnos()
            tabla.update()

            dialogo.close()

            ui.notify(
                'Turno modificado correctamente',
                color='green'
            )

####################################### BOTONES DIALOGO #########################################

        with ui.row().classes('w-full justify-end'):

            ui.button(
                'Cancelar',
                on_click=dialogo.close
            ).props('flat')

            ui.button(
                'Guardar',
                icon='save',
                on_click=guardar_cambios
            )

####################################### FUNCION MODIFICAR #######################################

    def abrir_modificacion():

        if not tabla.selected:

            ui.notify(
                'Seleccioná un turno',
                color='red'
            )

            return

        turno = tabla.selected[0]

        turno_id['valor'] = turno['id']

        input_fecha.value = turno['fecha']
        input_hora.value = turno['hora']
        input_tratamiento.value = turno['tratamiento']
        input_cupo_maximo.value = turno['cupoMaximo']

        dialogo.open()

####################################### BOTONES #################################################

    with ui.row():

        ui.button(
            'Modificar',
            icon='edit',
            on_click=abrir_modificacion
        )

        ui.button(
            'Eliminar',
            icon='delete',
            color='red',
            on_click=lambda: eliminar_turno_seleccionado(tabla)
        )