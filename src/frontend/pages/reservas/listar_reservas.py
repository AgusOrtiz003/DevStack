from nicegui import ui

# Página de listado de reservas del paciente
@ui.page('/listarReservas')
def pagina_listar_reservas():
    ui.page_title('Mis Turnos')
    
    # Parte superior
    with ui.header().classes('items-center justify-between'):
        ui.button(icon='home',on_click=ui.navigate.back).props('flat color=white')
        with ui.row().classes('items-center gap-1'):
            ui.button(icon='account_circle').props('flat color=white')