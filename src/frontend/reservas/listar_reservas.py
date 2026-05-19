from nicegui import ui, app
from backend.reservas.reserva_bdd import listarReservas, cancelarReserva
# Página de listado de reservas del paciente
def pagina_listar_reservas():

    def modificarReserva(idReserva):
        ui.notify('Modificación exitosa')

    def cancelar_y_actualizar(idReserva):
        cancelarReserva(idReserva)
        reservas_actualizadas = listarReservas(dniPaciente)
        tabla.rows = reservas_actualizadas
        tabla.update()
        ui.notify('Reserva cancelada', color='positive')

    dniPaciente = app.storage.user.get('dni')
    reservas=listarReservas(dniPaciente)
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
                            icon="edit"
                            color="primary"
                            flat
                            round
                            dense
                            @click="$parent.$emit('modificar', props.row.idReserva)"
                        />
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

    tabla.on('modificar', lambda e: modificarReserva(e.args))
    tabla.on('eliminar', lambda e: cancelar_y_actualizar(e.args))

    return tabla