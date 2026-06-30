from nicegui import ui
from backend.reservas.listar_reservas_recurrentes_secretaria import (
    listar_reservas_recurrentes_secretaria,
    obtener_detalle_recurrente
)
from backend.reservas.registrar_pago_recurrente_manual import (
    registrar_pago_recurrente_manual
)

@ui.page('/reservas_recurrentes')

def pagina_reservas_recurrentes():


    columnas = [
        {
            'name': 'dni',
            'label': 'DNI',
            'field': 'dni'
        },
        {
            'name': 'nombre',
            'label': 'Nombre',
            'field': 'nombre'
        },
        {
            'name': 'apellido',
            'label': 'Apellido',
            'field': 'apellido'
        },
        {
            'name': 'cantidadTurnos',
            'label': 'Cantidad de turnos',
            'field': 'cantidadTurnos'
        },
        {
            'name': 'metodoPago',
            'label': 'Método de pago',
            'field': 'metodoPago'
        },
        {
            'name': 'accion',
            'label': 'Acción',
            'field': 'accion'
        }
    ]



    def recargar():

        tabla.rows = listar_reservas_recurrentes_secretaria()

        tabla.update()
    
    async def registrar_pago(recurrente):

        detalles = obtener_detalle_recurrente(
            recurrente['idReservaRecurrente']
        )

        with ui.dialog() as dialog, ui.card().classes('w-[700px]'):

            ui.label(
                'Registrar pago recurrente'
            ).classes('text-h6')

            ui.separator()

            ui.label(
                f'Paciente: {recurrente["nombre"]} {recurrente["apellido"]}'
            )

            ui.label(
                f'DNI: {recurrente["dni"]}'
            )

            ui.label(
                f'Turnos: {recurrente["cantidadTurnos"]}'
            )

            ui.separator()

            ui.table(
                columns=[
                    {
                        'name': 'fecha',
                        'label': 'Fecha',
                        'field': 'fecha'
                    },
                    {
                        'name': 'hora',
                        'label': 'Hora',
                        'field': 'hora'
                    },
                    {
                        'name': 'tratamiento',
                        'label': 'Tratamiento',
                        'field': 'tratamiento'
                    }
                ],
                rows=detalles
            ).classes('w-full')

            with ui.row():

                ui.button(
                    'Cancelar',
                    on_click=lambda: dialog.submit(False)
                )

                ui.button(
                    'Confirmar pago',
                    color='green',
                    on_click=lambda: dialog.submit(True)
                )

        resultado = await dialog

        if not resultado:
            return

        registrar_pago_recurrente_manual(
            recurrente['idReservaRecurrente']
        )

        ui.notify(
            'Pago registrado correctamente',
            color='green'
        )

        recargar()

    slot_pago = r'''
    <q-td :props="props">
        <q-btn
            v-if="
                props.row.metodoPago === 'Efectivo' ||
                props.row.metodoPago === 'Transferencia'
            "
            label="Registrar pago"
            color="green"
            flat
            dense
            icon="payments"
            @click="$parent.$emit('registrar_pago', props.row)"
        />
    </q-td>
    '''
    
    reservas = listar_reservas_recurrentes_secretaria()

    tabla = ui.table(
        columns=columnas,
        rows=reservas,
        row_key='idReservaRecurrente'
    ).classes('w-full')

    tabla.add_slot(
        'body-cell-accion',
        slot_pago
    )

    tabla.on(
        'registrar_pago',
        lambda e: registrar_pago(e.args)
    )