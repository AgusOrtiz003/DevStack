from nicegui import app, ui
from frontend.reservas.reservas import pagina_reservas
from frontend.reservas.listar_reservas import pagina_listar_reservas
from frontend.perfil import perfil
from src.utils.fetch_usuarios import logout

@ui.page('/Paciente/home')
def main_page():

    with ui.header().classes(replace='row items-center gap-4'):
        with ui.tabs() as tabs:
            inicio_tab = ui.tab('Inicio',icon='home')
            reservas_tab = ui.tab('Mis reservas',icon='calendar_month')
            reservar_tab = ui.tab('Reservar turno',icon='event')
        with ui.row().classes('ml-auto items-center'):
            ui.button(icon='account_circle',on_click=lambda: ui.navigate.to('/ver_perfil')).props('flat round color=white')
            ui.button(icon='logout',on_click=lambda:logout()).props('flat round color=white')

    with ui.tab_panels(tabs, value='Inicio').classes('w-full'):
        with ui.tab_panel('Inicio').classes('items-center'):
            with ui.column().classes('w-full items-center justify-center'):
                ui.image('src/frontend/icons/kinePro-logo.png').classes('w-110')
        with ui.tab_panel('Mis reservas'):
            tabla_reservas = pagina_listar_reservas()
        with ui.tab_panel(reservar_tab):
            pagina_reservas(tabla_reservas)