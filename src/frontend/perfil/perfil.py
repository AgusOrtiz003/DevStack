from nicegui import app,ui
import utils.imports as imports 

from pacientes.home import logout 
@ui.page('/ver_perfil')

def ver_perfil ():
    with ui.header().classes(replace='row items-center justify-between gap-4') as header:
        with ui.tabs() as tabs:
            ui.tab('Inicio',icon='home').on('click',lambda: ui.navigate.to(f'/{app.storage.user["rol"]}/home'))

        ui.button(on_click=logout, icon='logout').classes('group rounded-full overflow-hidden w-12 \
                        hover: w-10 transition-all duration- 300 ml').props('flat color=white round,')
    ui.label('Mi perfil').classes('')
    
    with ui.card().classes('no-shadow border border-gray-200'):
        ui.label("probando")

    with ui.card().props('flat bordered').on('click'):
        ui.label('Also no shadow!')
    
 
            
            