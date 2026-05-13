from nicegui import ui

# Página principal
@ui.page('/')
def pagina_home():
    ui.page_title('Página principal')
    ui.query('body').style('background-color: #1E73B7')
    with ui.card().classes('fixed-center items-center').classes('w-150'):
        ui.image('src/frontend/icons/texto-kinePro-logo.png').classes('w-25')
        with ui.row():
            ui.button('Reservar turno',on_click=lambda: ui.navigate.to('/reservas'))
            ui.button('Registrar turno',on_click=lambda: ui.navigate.to('/registrarTurno'))
            ui.button('Listar turnos - Secretaria',on_click=lambda: ui.navigate.to('/listarTurnos'))