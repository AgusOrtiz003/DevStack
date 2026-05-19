from nicegui import ui, app
from backend.reservas.reserva_bdd import listarReservas

# Página de listado de reservas del paciente
def pagina_listar_reservas():
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
    ],
    rows=reservas,
    row_key='idReserva').classes('w-full overflow-hidden shadow-md')

    tabla.add_slot('header', r'''
<q-tr class="bg-primary text-white">
    <q-th
        v-for="col in props.cols"
        :key="col.name"
    >
        {{ col.label }}
    </q-th>
</q-tr>
''')