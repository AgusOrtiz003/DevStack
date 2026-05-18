from nicegui import ui
from backend.listar_turnos_para_reservas import listar_los_turnos_para_reservas
from backend.crear_reserva import registrar_una_reserva

# Página de registar reserva
@ui.page('/reservas')
def pagina_registar_reserva():

    def reservar(e):

        fila = e.args
        
        # EL 1 EN ID_PACIENTE ES TEMPORAL
        registrar_una_reserva(
            fila['fecha'],
            fila['hora'],
            1,
            fila['tratamiento']
        )

        ui.notify(
            'Reserva registrada correctamente',
            color='positive'
        )

        ui.timer(1.5,lambda: ui.navigate.reload(),once=True)

    def lista_espera(e):
        ui.notify(
            f"Agregado a lista de espera: {e.args['fecha']}"
        )
        ui.navigate.reload()

    # Columnas
    columnas = [
    {'name': 'fecha', 'label': 'Fecha', 'field': 'fecha'},
    {'name': 'hora', 'label': 'Hora', 'field': 'hora'},
    {'name': 'tratamiento', 'label': 'Tratamiento', 'field': 'tratamiento'},
    {'name': 'cupoActual', 'label': 'Cupo Actual', 'field': 'cupoActual'},
    {'name': 'accion','label': 'Acción', 'field': 'accion'}
    ]

    turnos = listar_los_turnos_para_reservas()

####################################### PÁGINA ##################################################
    ui.page_title('Reservas')

    # Parte superior
    with ui.header().classes('items-center justify-between'):
        ui.button(icon='home',on_click=ui.navigate.back).props('flat color=white')
        with ui.row().classes('items-center gap-1'):
            ui.button(on_click=lambda: right_drawer.toggle(), icon='menu').props('flat color=white')
            ui.button(icon='account_circle').props('flat color=white')
    
    # Parte central
    # Tabla
    tabla = ui.table(
        columns=columnas,
        rows=turnos,
        row_key='fecha',
    ).classes('w-full')

     # Personaliza la columna acción
    tabla.add_slot('body-cell-accion', r'''
        <q-td :props="props">

            <q-btn
                v-if="props.row.cupoActual > 0"
                color="positive"
                label="Reservar"
                icon="event_available"
                @click="$parent.$emit('reservar', props.row)"
            />

            <q-btn
                v-else
                color="warning"
                label="Lista de espera"
                icon="hourglass_top"
                @click="$parent.$emit('espera', props.row)"
            />

        </q-td>
    ''')

    tabla.on('reservar', reservar)
    tabla.on('espera', lista_espera)

    # Parte derecha
    with ui.right_drawer(fixed=False).style('background-color: #ebf1fa').classes('items-center').props('bordered') as right_drawer:
        ui.button('Mis reservas', icon='calendar_month', on_click=lambda: ui.navigate.to('/listarReservas'))