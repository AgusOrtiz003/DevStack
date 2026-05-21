from nicegui import ui, app
from backend.turnos.listar_turnos import listar_reservas_turno
from backend.reservas.confirmar_reserva import confirmar_reserva

@ui.page('/listadoReservas/{idTurno}')
def pagina_listar_reservas_secretaria(idTurno: int):

    def logout():
        app.storage.user.clear()
        ui.navigate.to('/login')
    
    def realizar_check_in(idReserva):
        confirmar_reserva(idReserva)
        tabla.rows = listar_reservas_turno(idTurno)
        tabla.update()
        ui.notify('Check-in realizado', color='green')

    reservas = listar_reservas_turno(idTurno)

    with ui.header().classes(replace='row items-center gap-4'):
        ui.button('Volver', icon='arrow_back').on('click',lambda: ui.navigate.back()).props('flat color=white')
        with ui.row().classes('ml-auto'):
            ui.button(icon='account_circle').props('flat color=white round')
            ui.button(
                on_click=logout,
                icon='logout'
            ).props('flat color=white round')

    ui.label(f'Reservas del turno #{idTurno}') \
        .classes('text-2xl font-bold m-4')

    tabla = ui.table(
        columns=[
            {'name': 'dniPaciente','label': 'DNI Paciente','field': 'dniPaciente',},
            {'name': 'obraSocial','label': 'Obra Social','field': 'obraSocial',},
            {'name': 'metodoPago','label': 'Método de Pago','field': 'metodoPago',},
            {'name': 'estado','label': 'Estado','field': 'estado',},
            {'name': 'fechaCreacion','label': 'Fecha creación','field': 'fechaCreacion',},
            {'name': 'accion', 'label': 'Acción', 'field': 'accion'},
        ],
        rows=reservas,
        row_key='idReserva',
    ).classes('w-full overflow-hidden shadow-md')

    tabla.add_slot('body-cell-accion', r'''
        <q-td :props="props">

            <q-btn
                v-if="props.row.estado != 'Confirmado'"
                icon="check"
                color="positive"
                flat
                round
                dense
                @click="$parent.$emit('check_in', props.row.idReserva)"
            />

        </q-td>
    ''')

    tabla.on('check_in',lambda e: realizar_check_in(e.args))