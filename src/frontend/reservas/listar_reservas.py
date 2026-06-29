import qrcode
import io
import base64
from nicegui import ui, app
from backend.reservas.listar_reservas import listar_reservas, listar_reservas_recurrentes
from backend.reservas.cancelar_reserva import cancelar_reserva
from backend.pagos.crear_preferencia import crear_preferencia_mp
from backend.reservas.cancelar_reserva_recurrente import cancelar_reserva_recurrente_individual

# Página de listado de reservas del paciente
def pagina_listar_reservas():

    async def pagar_recurrente(recurrente):
        from backend.reservas.listar_reservas import listar_reservas_de_recurrente
        from backend.pagos.verificar_pago import verificar_pago
        from backend.pagos.registrar_pago import registrar_pago

        reservas = listar_reservas_de_recurrente(recurrente['idReservaRecurrente'])
        pendientes = [r for r in reservas if r['estado'] == 'Pendiente']

        if not pendientes:
            ui.notify('No hay reservas pendientes de pago', color='warning')
            return

        primera = pendientes[0]

        try:
            url_pago = crear_preferencia_mp(
                idReserva=primera['idReserva'],
                descripcion=f"Reserva recurrente — {recurrente['tratamiento']}",
                monto=5000.0 * len(pendientes)
            )
        except Exception as e:
            ui.notify(f'Error al conectar con MercadoPago: {e}', color='red')
            return

        qr_base64 = generar_qr_base64(url_pago)

        with ui.dialog() as dialog, ui.card().classes('w-[600px]'):
            ui.label('Pago de reserva recurrente').classes('text-lg font-bold')
            ui.separator()

            with ui.row().classes('w-full gap-6 items-start'):
                with ui.column().classes('items-center gap-2'):
                    ui.label('Escaneá con la app de MercadoPago').classes('text-xs text-gray-500')
                    ui.image(f'data:image/png;base64,{qr_base64}').classes('w-48 h-48')

                with ui.column().classes('flex-1 gap-1'):
                    with ui.grid(columns=2).classes('w-full gap-x-4 gap-y-1 text-sm'):
                        ui.label('Tratamiento:').classes('text-gray-500')
                        ui.label(recurrente['tratamiento'])
                        ui.label('Período:').classes('text-gray-500')
                        ui.label(recurrente['periodo'])
                        ui.label('Turnos pendientes:').classes('text-gray-500')
                        ui.label(str(len(pendientes)))

                    ui.separator()
                    ui.label(f'Total: ${5000 * len(pendientes):,} ARS').classes('text-xl font-semibold mt-2')
                    ui.button(
                        'Ir a pagar',
                        icon='payments',
                        on_click=lambda: ui.navigate.to(url_pago, new_tab=True)
                    ).props('color=primary').classes('w-full mt-1')

            ui.separator()

            async def verificar():
                estado, monto, token = verificar_pago(primera['idReserva'])

                if estado == 'approved':
                    for r in pendientes:
                        registrar_pago(r['idReserva'], monto / len(pendientes), token)
                    recargar_tablas()
                    ui.notify('¡Pago confirmado para todas las reservas!', color='green')
                    dialog.close()
                else:
                    ui.notify('El pago no fue aprobado todavía', color='warning')

            with ui.row().classes('w-full justify-between items-center'):
                ui.button('Ya pagué, verificar', on_click=verificar).props('flat color=green')
                ui.button('Cerrar', on_click=dialog.close).props('flat')

        dialog.open()

    async def ver_turnos_recurrente(recurrente):
        from backend.reservas.listar_reservas import listar_reservas_de_recurrente
        reservas = listar_reservas_de_recurrente(recurrente['idReservaRecurrente'])

        with ui.dialog() as dialog, ui.card().classes('w-[700px]'):
            with ui.row().classes('items-center gap-2 pb-2'):
                ui.icon('repeat', size='sm').classes('text-orange-200')
                ui.label(f"Reservas ({recurrente['periodo']})").classes('text-base font-semibold')

            ui.separator()

            columnas_detalle = [
                {'name': 'fecha',      'label': 'Fecha',   'field': 'fecha'},
                {'name': 'hora',       'label': 'Hora',    'field': 'hora'},
                {'name': 'estado',    'label': 'Estado',  'field': 'estado'},
                {'name': 'accion',     'label': 'Accion',  'field': 'accion'},
            ]

            tabla_detalle = ui.table(
                    columns=columnas_detalle,
                    rows=reservas,
                    row_key='idReserva'
            ).classes('w-full')

            tabla_detalle.add_slot('body-cell-accion', r'''
                <q-td :props="props">
                    <q-btn
                        v-if="props.row.estado === 'Pendiente'"
                        label="Cancelar"
                        color="negative"
                        flat
                        dense
                        @click="$parent.$emit('cancelar_individual', props.row.idReserva)"
                    />
                </q-td>
            ''')

            async def cancelar_individual(idReserva):

                try:

                    cancelar_reserva_recurrente_individual(
                        idReserva
                    )

                    tabla_detalle.rows = listar_reservas_de_recurrente(
                        recurrente['idReservaRecurrente']
                    )

                    tabla_detalle.update()

                    recargar_tablas()

                    ui.notify(
                        'Reserva cancelada',
                        color='green'
                    )

                except Exception as e:

                    ui.notify(
                        str(e),
                        color='red'
                    )

            tabla_detalle.on(
                'cancelar_individual',
                lambda e: cancelar_individual(e.args)
            )

            ui.separator()
            ui.button('Cerrar', on_click=dialog.close).props('flat').classes('self-end')

        dialog.open()

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
                    ui.label('Total: $5.000 ARS').classes('text-xl font-semibold mt-2')
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
    reservas_recurrentes = listar_reservas_recurrentes(dniPaciente)

    for r in reservas_recurrentes:
        r['periodo'] = f"{r['fecha_desde']} - {r['fecha_hasta']}"

    pendientes = [r for r in reservas if r['estado'] == 'Pendiente' and not r['idReservaRecurrente']]
    pagadas    = [r for r in reservas if r['estado'] == 'Pagado' and not r['idReservaRecurrente']]
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

    columnas_recurrentes = [
        {'name': 'periodo',     'label': 'Período',        'field': 'periodo'},
        {'name': 'hora',        'label': 'Hora',           'field': 'hora'},
        {'name': 'tratamiento', 'label': 'Tratamiento',    'field': 'tratamiento'},
        {'name': 'obraSocial',  'label': 'Obra Social',    'field': 'obraSocial'},
        {'name': 'accion',      'label': 'Acción',         'field': 'accion'},
    ]


    def recargar_tablas():
        nuevas = listar_reservas(dniPaciente)
        nuevas_recurrentes = listar_reservas_recurrentes(dniPaciente)
        for r in nuevas_recurrentes:
            r['periodo'] = f"{r['fecha_desde']} - {r['fecha_hasta']}"
        tabla_pendientes.rows = [r for r in nuevas if r['estado'] == 'Pendiente' and not r['idReservaRecurrente']]
        tabla_pagadas.rows    = [r for r in nuevas if r['estado'] == 'Pagado' and not r['idReservaRecurrente']]
        tabla_canceladas.rows = [r for r in nuevas if r['estado'] == 'Cancelado']
        tabla_recurrentes.rows = nuevas_recurrentes
        tabla_pendientes.update()
        tabla_pagadas.update()
        tabla_canceladas.update()
        tabla_recurrentes.update()

    slot_pendientes = r'''
        <q-td :props="props">
            <q-btn label="Pagar" color="primary" flat @click="$parent.$emit('pagar', props.row)"/>
            <q-btn label="Cancelar" color="negative" flat @click="$parent.$emit('eliminar', props.row.idReserva)"/>
        </q-td>
    '''

    slot_recurrentes = r'''
        <q-td :props="props">
            <q-btn label="Pagar todo" color="primary" flat @click="$parent.$emit('pagar_recurrente', props.row)"/>
            <q-btn label="Ver reservas" color="secondary" flat @click="$parent.$emit('ver_turnos', props.row)"/>
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

        # Tabla recurrentes
        with ui.card().classes('w-full mt-4 border-l-4 border-orange-200'):
            with ui.row().classes('items-center gap-2 px-4 pt-3 pb-1'):
                ui.icon('schedule', size='sm').classes('text-orange-200')
                ui.label('Reservas recurrentes').classes('text-base font-semibold text-orange-200')
                ui.badge(str(len(reservas_recurrentes)), color='orange-200').classes('ml-1')
            tabla_recurrentes = ui.table(columns=columnas_recurrentes, rows=reservas_recurrentes, row_key='idReserva').classes('w-full')
            tabla_recurrentes.add_slot('body-cell-accion', slot_recurrentes)
            tabla_recurrentes.on('ver_turnos',       lambda e: ver_turnos_recurrente(e.args))
            tabla_recurrentes.on('pagar_recurrente', lambda e: pagar_recurrente(e.args))

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