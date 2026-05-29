from nicegui import ui, app
from backend.reservas.listar_reservas import listar_reservas
from backend.reservas.cancelar_reserva import cancelar_reserva

# Página de listado de reservas del paciente
def pagina_listar_reservas():

    async def cancelar_y_actualizar(idReserva):
        with ui.dialog() as dialog, ui.card().classes('w-100'):
            ui.label('¿Desea cancelar la reserva?')
            ui.separator()
            with ui.row().classes('w-full justify-center gap-2'):
                ui.button('Si', on_click=lambda: dialog.submit(True)).props('color=red-500')
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
        {'name': 'accion', 'label': 'Accion', 'field': 'accion'},
    ],
    rows=reservas,
    row_key='idReserva').classes('w-full overflow-hidden shadow-md')

    tabla.add_slot('body-cell-accion', r'''
        <q-td :props="props">
            <q-btn
                label="Cancelar reserva"
                color="negative"
                flat
                @click="$parent.$emit('eliminar', props.row.idReserva)"
            />
        </q-td>
    ''')

    tabla.on('eliminar', lambda e: cancelar_y_actualizar(e.args))

    return tabla