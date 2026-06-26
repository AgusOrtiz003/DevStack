import qrcode
import io
import base64
from nicegui import ui, app
from backend.reservas.listar_reservas import listar_reservas
from backend.reservas.cancelar_reserva import cancelar_reserva
from backend.pagos.crear_preferencia import crear_preferencia_mp


# Página de listado de reservas del paciente
def pagina_listar_reservas():

    def generar_qr_base64(url: str) -> str:
        qr = qrcode.make(url)
        buffer = io.BytesIO()
        qr.save(buffer, format='PNG')
        buffer.seek(0)
        return base64.b64encode(buffer.read()).decode()

    async def pagar_reserva(reserva):
        try:
            url_pago = crear_preferencia_mp(
                idReserva=reserva['idReserva'],
                descripcion="Turno de kinesiología",
                monto=5000.0
            )
        except Exception as e:
            ui.notify(f'Error al conectar con MercadoPago: {e}', color='red')
            return
        
        qr_base64 = generar_qr_base64(url_pago)
        
        with ui.dialog() as dialog, ui.card().classes('w-[600px]'):
            ui.label('Resumen del turno').classes('text-lg font-bold')
            ui.separator()

            with ui.row().classes('w-full gap-6 items-start'):

                with ui.column().classes('items-center gap-2'):
                    ui.label('Escaneá con la app de MercadoPago').classes('text-xs text-gray-500')
                    ui.image(f'data:image/png;base64,{qr_base64}').classes('w-48 h-48')

                with ui.column().classes('flex-1 gap-1'):
                    with ui.grid(columns=2).classes('w-full gap-x-4 gap-y-1 text-sm'):
                        ui.label('Tratamiento:').classes('text-gray-500')
                        ui.label(reserva['tratamiento'])
                        ui.label('Fecha:').classes('text-gray-500')
                        ui.label(reserva['fecha'])
                        ui.label('Hora:').classes('text-gray-500')
                        ui.label(reserva['hora'])

                    ui.separator()
                    ui.label('Total: $50.000 ARS').classes('text-xl font-semibold mt-2')
                    ui.label('O si preferís, pagá desde el navegador:').classes('text-xs text-gray-500 mt-2')
                    ui.button(
                        'Ir a pagar',
                        icon="payments",
                        on_click=lambda: ui.navigate.to(url_pago, new_tab=True)
                    ).props('color=primary').classes('w-full mt-1')

            ui.separator()

            async def verificar():
                from backend.pagos.verificar_pago import verificar_pago
                from backend.pagos.registrar_pago import registrar_pago

                estado, monto, token = verificar_pago(reserva['idReserva'])
                print("Estado:", estado, "Monto:", monto, "Token:", token)

                if estado == "approved":
                    registrar_pago(reserva['idReserva'], monto, token)
                    reservas_actualizadas = listar_reservas(dniPaciente)
                    recargar_tablas()
                    ui.notify('¡Pago confirmado!', color='green')
                    dialog.close()
                else:
                    ui.notify('El pago no fue aprobado todavía', color='warning')

            with ui.row().classes('w-full justify-between items-center'):
                ui.button('Ya pagué, verificar', on_click=verificar).props('flat color=green')
                ui.button('Cerrar', on_click=dialog.close).props('flat')

        dialog.open()

    async def cancelar_y_actualizar(idReserva):
        with ui.dialog() as dialog, ui.card().classes('w-100'):
            ui.label('¿Desea cancelar la reserva?')
            ui.separator()
            with ui.row().classes('w-full justify-center gap-2'):
                ui.button('Si', on_click=lambda: dialog.submit(True)).props('color=red-500')
                ui.button('No', on_click=lambda: dialog.submit(False)).props('flat')
        if await dialog:
            cancelar_reserva(idReserva)
            recargar_tablas()
            ui.notify('Reserva cancelada', color='green')

    dniPaciente = app.storage.user.get('dni')
    reservas = listar_reservas(dniPaciente)

    pendientes = [r for r in reservas if r['estado'] == 'Pendiente']
    pagadas    = [r for r in reservas if r['estado'] == 'Pagado']
    canceladas = [r for r in reservas if r['estado'] == 'Cancelado']

    columnas_con_accion = [
        {'name': 'fecha',       'label': 'Fecha',          'field': 'fecha'},
        {'name': 'hora',        'label': 'Hora',           'field': 'hora'},
        {'name': 'tratamiento', 'label': 'Tratamiento',    'field': 'tratamiento'},
        {'name': 'obraSocial',  'label': 'Obra Social',    'field': 'obraSocial'},
        {'name': 'accion',      'label': 'Acción',         'field': 'accion'},
    ]

    columnas_sin_accion = [
        {'name': 'fecha',       'label': 'Fecha',          'field': 'fecha'},
        {'name': 'hora',        'label': 'Hora',           'field': 'hora'},
        {'name': 'tratamiento', 'label': 'Tratamiento',    'field': 'tratamiento'},
        {'name': 'obraSocial',  'label': 'Obra Social',    'field': 'obraSocial'},
    ]


    def recargar_tablas():
        nuevas = listar_reservas(dniPaciente)
        tabla_pendientes.rows = [r for r in nuevas if r['estado'] == 'Pendiente']
        tabla_pagadas.rows    = [r for r in nuevas if r['estado'] == 'Pagado']
        tabla_canceladas.rows = [r for r in nuevas if r['estado'] == 'Cancelado']
        tabla_pendientes.update()
        tabla_pagadas.update()
        tabla_canceladas.update()

    slot_pendientes = r'''
        <q-td :props="props">
            <q-btn label="Pagar" color="primary" flat @click="$parent.$emit('pagar', props.row)"/>
            <q-btn label="Cancelar" color="negative" flat @click="$parent.$emit('eliminar', props.row.idReserva)"/>
        </q-td>
    '''

    with ui.card().classes('w-full border-l-4 border-blue-400'):
        with ui.row().classes('items-center gap-2 px-4 pt-3 pb-1 justify-between'):
            ui.icon('calendar_month', size='sm').classes('text-blue-400')
            ui.label('Mis reservas').classes('text-base font-semibold text-blue-400')
            ui.button(
                icon='sync',
                on_click=recargar_tablas
            ).props('flat round dense')

        # Tabla pendientes
        with ui.card().classes('w-full mt-4 border-l-4 border-orange-400'):
            with ui.row().classes('items-center gap-2 px-4 pt-3 pb-1'):
                ui.icon('schedule', size='sm').classes('text-orange-400')
                ui.label('Reservas pendientes').classes('text-base font-semibold text-orange-400')
                ui.badge(str(len(pendientes)), color='orange').classes('ml-1')
            tabla_pendientes = ui.table(columns=columnas_con_accion, rows=pendientes, row_key='idReserva').classes('w-full')
            tabla_pendientes.add_slot('body-cell-accion', slot_pendientes)
            tabla_pendientes.on('eliminar', lambda e: cancelar_y_actualizar(e.args))
            tabla_pendientes.on('pagar',    lambda e: pagar_reserva(e.args))

        # Tabla pagadas
        with ui.card().classes('w-full mt-4 border-l-4 border-green-500'):
            with ui.row().classes('items-center gap-2 px-4 pt-3 pb-1'):
                ui.icon('check_circle', size='sm').classes('text-green-500')
                ui.label('Reservas pagadas').classes('text-base font-semibold text-green-600')
                ui.badge(str(len(pagadas)), color='green').classes('ml-1')
            tabla_pagadas = ui.table(columns=columnas_sin_accion, rows=pagadas, row_key='idReserva').classes('w-full')

        # Tabla canceladas
        with ui.card().classes('w-full mt-4 border-l-4 border-red-400'):
            with ui.row().classes('items-center gap-2 px-4 pt-3 pb-1'):
                ui.icon('cancel', size='sm').classes('text-red-400')
                ui.label('Reservas canceladas').classes('text-base font-semibold text-red-400')
                ui.badge(str(len(canceladas)), color='red').classes('ml-1')
            tabla_canceladas = ui.table(columns=columnas_sin_accion, rows=canceladas, row_key='idReserva').classes('w-full')

    return tabla_pendientes