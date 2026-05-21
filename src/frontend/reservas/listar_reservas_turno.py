from nicegui import ui,app

# Página de listado de reservas del paciente
@ui.page('/listadoReservas/{idTurno}')
def pagina_listar_reservas_secretaria(idTurno):
    def logout() -> None:
        app.storage.user.clear()
        ui.navigate.to('/login')

    with ui.header().classes(replace='row items-center gap-4') as header:
        with ui.tabs() as tabs:
            volver_tab = ui.tab('Volver',icon='arrow_back').on('click',lambda: ui.navigate.back())
        with ui.row().classes('ml-auto'):
            ui.button(icon='account_circle').props('flat color=white round')
            ui.button(on_click=logout, icon='logout').props('flat color=white round')
