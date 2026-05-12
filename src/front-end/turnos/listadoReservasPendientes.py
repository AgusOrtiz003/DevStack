from nicegui import ui

reservas_pendientes = [
    {
        'fecha': '12/05/2026',
        'hora': '10:00',
        'kinesiologo': 'Dr. Pérez'
    },
    {
        'fecha': '14/05/2026',
        'hora': '16:30',
        'kinesiologo': 'Lic. Gómez'
    },
]

columnas = [
    {'name': 'fecha', 'label': 'Fecha', 'field': 'fecha'},
    {'name': 'hora', 'label': 'Hora', 'field': 'hora'},
    {'name': 'kinesiologo', 'label': 'Kinesiólogo', 'field': 'kinesiologo'},
]

# Página de listado de reservas pendientes
@ui.page('/reservasPendientes')
def reservasPendientes():
    ui.page_title('Reservas Pendientes')
    # Parte superior
    with ui.header().classes('items-center justify-between'):
        ui.button(icon='home',on_click=ui.navigate.back).props('flat color=white')
        with ui.row().classes('items-center gap-1'):
            ui.button(icon='account_circle').props('flat color=white')

    ui.table(
        columns=columnas,
        rows=reservas_pendientes,
        row_key='fecha'
    ).classes('w-full')