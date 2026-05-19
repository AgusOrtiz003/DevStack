from nicegui import ui, app
from backend.reservas.reserva_bdd import listarReservas

# Página de listado de reservas del paciente
@ui.page('/listarReservas')
def pagina_listar_reservas():
    ui.page_title('Mis Turnos')
    
    # Parte superior
    with ui.header().classes('bg-transparent items-center justify-between'):
        ui.button(icon='arrow_back',on_click=lambda: ui.navigate.to('/reservas'))
        with ui.row().classes('items-center gap-1'):
            ui.button(icon='account_circle')

    reservas=listarReservas(dniPaciente)
    # Parte central
    for 