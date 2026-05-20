from nicegui import app,ui
import utils.imports as imports 
from pacientes.home import logout 
from utils import fetchUsuarios


@ui.page('/ver_perfil')
def ver_perfil ():
    usuario = fetchUsuarios.get_datos(app.storage.user["dni"])

    with ui.header().classes(replace='row items-center justify-between gap-4') as header:
        with ui.tabs() as tabs:
            ui.tab('Inicio',icon='home').on('click',lambda: ui.navigate.to(f'/{app.storage.user["rol"]}/home'))

        ui.button(on_click=logout, icon='logout').classes('group rounded-full overflow-hidden w-12 \
                        hover: w-10 transition-all duration- 300 ml').props('flat color=white round,')
    ui.label('Mi perfil').classes('')
    
    with ui.column().classes('w-full h-screen items-center justify-center'):
        with ui.card().classes('p-6'):
            ui.label(f'Nombre : {usuario['nombre']}').classes('text-2xl font-bold text-blue-500 mb-4').on('click', lambda :print("este es el nombre"))
            ui.label(f'Apellido : {usuario['apellido']}').classes('text-2xl font-bold text-blue-500 mb-4').on('click', lambda :print("este es el apellido"))
            ui.label(f'DNI : {usuario['dni']}').classes('text-2xl font-bold text-blue-500 mb-4').on('click', lambda :print("este es el dni"))
            ui.label(f'Email : {usuario['email']}').classes('text-2xl font-bold text-blue-500 mb-4')
            ui.label(f'Fecha de nacimiento : {usuario['fechaNac']}').classes('text-2xl font-bold text-blue-500 mb-4')

    
 
            
            