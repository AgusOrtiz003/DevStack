from nicegui import ui

# Página principal
@ui.page('/')
def page():
    ui.page_title('Página principal')
    ui.query('body').style('background-color: #1E73B7')
    with ui.card().classes('fixed-center'):
        ui.image('UI\Icons\kinePro-logo.png').props('w-10 h-10')
        ui.button('Reservar turno',on_click=lambda: ui.navigate.to('/reservas'))