from nicegui import ui

# Página de reservas
@ui.page('/reservas')
def reservas():
    ui.page_title('Reservas')
    # Parte superior
    with ui.header().classes('items-center justify-between'):
        ui.button(icon='home',on_click=ui.navigate.back).props('flat color=white')
        with ui.row().classes('items-center gap-1'):
            ui.button(on_click=lambda: right_drawer.toggle(), icon='menu').props('flat color=white')
            ui.button(icon='account_circle').props('flat color=white')
    
    # Parte central
    with ui.card().classes('fixed-center items-center p-20%'):
        ui.label("Ingresar reserva").classes('')
        ui.date_input('Fecha de reserva').props('locale=es')
        with ui.row():
            ui.button("Reservar")
            ui.button("Lista de espera")

    # Parte izquierda
    ui.left_drawer(top_corner=False, bottom_corner=True)

    # Parte derecha
    with ui.right_drawer(fixed=False).style('background-color: #ebf1fa').classes('items-center').props('bordered') as right_drawer:
        ui.button('Reservas pendientes',on_click=lambda: ui.navigate.to('/reservasPendientes'))