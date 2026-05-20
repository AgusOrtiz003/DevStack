from nicegui import app,ui
import utils.imports as imports 
from pacientes.home import logout 
from utils import fetchUsuarios


@ui.page('/ver_perfil')
def ver_perfil ():
    usuario = fetchUsuarios.get_datos(app.storage.user["dni"])

    with ui.dialog() as dialog, ui.card():
        ui.label('¿Seguro que querés eliminar tu cuenta?').classes('text-lg')

        with ui.row().classes('justify-end w-full gap-2 mt-4'):
            ui.button('Cancelar', on_click=dialog.close)

            ui.button('Eliminar',on_click=lambda: (fetchUsuarios.eliminar_cuenta(usuario["dni"]),dialog.close())).classes('bg-red-600 text-white')
    
    def abrir_dialogo():
        dialog.open()

    with ui.header().classes(replace='row items-center justify-between gap-4') as header:
        with ui.tabs() as tabs:
            ui.tab('Inicio',icon='home').on('click',lambda: ui.navigate.to(f'/{app.storage.user["rol"]}/home'))

        ui.button(on_click=logout, icon='logout').classes('group rounded-full overflow-hidden w-12 \
                        hover: w-10 transition-all duration- 300 ml').props('flat color=white round,')
    
    with ui.column().classes('w-full h-screen items-center justify-center'):
        with ui.card().classes('p-6 '):
            ui.label(f'Nombre : {usuario['nombre']}').classes('text-2xl font-bold text-blue-500 mb-4')
            ui.label(f'Apellido : {usuario['apellido']}').classes('text-2xl font-bold text-blue-500 mb-4')
            ui.label(f'DNI : {usuario['dni']}').classes('text-2xl font-bold text-blue-500 mb-4')
            ui.label(f'Email : {usuario['email']}').classes('text-2xl font-bold text-blue-500 mb-4')
            ui.label(f'Fecha de nacimiento : {usuario['fechaNac']}').classes('text-2xl font-bold text-blue-500 mb-4')
            ui.button('Eliminar cuenta',on_click= abrir_dialogo).classes(
            'bg-red-600 text-white mt-4 px-6 py-2 rounded-lg ')
    


 
            
            