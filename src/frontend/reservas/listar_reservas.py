from nicegui import ui, app
from backend.reservas.listar_reservas import listar_reservas
from backend.reservas.cancelar_reserva import cancelar_reserva

# Página de listado de reservas del paciente
def pagina_listar_reservas():

    def modificarReserva(idReserva):
        ui.notify('Modificación exitosa')

    async def cancelar_y_actualizar(idReserva):
        with ui.dialog() as dialog, ui.card().classes('w-100'):
            ui.label('¿Desea cancelar la reserva?')
            ui.separator()
            with ui.row().classes('w-full justify-center gap-2'):
                ui.button('Si', on_click=lambda: dialog.submit(True)).props('color=red')
                ui.button('No', on_click=lambda: dialog.submit(False)).props('flat')
        if await dialog:
            cancelar_reserva(idReserva)
            reservas_actualizadas = listar_reservas(dniPaciente)
            tabla.rows = reservas_actualizadas
            tabla.update()
            ui.notify('Reserva cancelada', color='green')

    dniPaciente = app.storage.user.get('dni')
    reservas=listar_reservas(dniPaciente)
    # Parte central
    tabla = ui.table(
    columns=[
        {'name': 'fecha', 'label': 'Fecha', 'field': 'fecha'},
        {'name': 'hora', 'label': 'Hora', 'field': 'hora'},
        {'name': 'tratamiento', 'label': 'Tratamiento', 'field': 'tratamiento'},
        {'name': 'obraSocial', 'label': 'Obra Social', 'field': 'obraSocial'},
        {'name': 'metodoPago', 'label': 'Método de Pago', 'field': 'metodoPago'},
        {'name': 'estado', 'label': 'Estado', 'field': 'estado'},
        {'name': 'accion', 'label': 'Acción', 'field': 'accion'},
    ],
    rows=reservas,
    row_key='idReserva').classes('w-full overflow-hidden shadow-md')

    tabla.add_slot('body', r'''
        <q-tr
            :props="props"
            class="group hover:bg-blue-1 transition-all duration-200"
        >
            <q-td
                v-for="col in props.cols"
                :key="col.name"
                :props="props"
            >

                <template v-if="col.name != 'accion'">
                    {{ col.value }}
                </template>

                <template v-else>
                    <div class="opacity-0 group-hover:opacity-100 transition-opacity duration-200">
                        <q-btn
                            icon="delete"
                            color="negative"
                            flat
                            round
                            dense
                            @click="$parent.$emit('eliminar', props.row.idReserva)"
                        />
                    </div>
                </template>

            </q-td>
        </q-tr>
    ''')

    tabla.on('eliminar', lambda e: cancelar_y_actualizar(e.args))

    return tabla