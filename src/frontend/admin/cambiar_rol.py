from nicegui import app, ui

from src.backend.cambiar_rol import cambiar_rol
from src.utils.fetch_usuarios import existe, get_datos

@ui.page('/Administrador/cambiar_rol')
def cambiar_rol_page():
    with ui.card().classes('w-50'):
        dni_input = ui.input('DNI del usuario').props('autofocus')
        nuevo_rol_input = ui.select(['Paciente', 'Medico', 'Administrador'], label='Nuevo rol')
        ui.button('Cambiar rol', on_click=lambda: try_cambiar_rol(app.storage.user['dni'], dni_input.value, nuevo_rol_input.value))
    
def try_cambiar_rol(dni_admin,dni_ingresado,nuevo_rol):
    if(existe(dni_ingresado)):
        rol_actual=get_datos(dni_ingresado)['rol']
        distintos=(dni_admin!=dni_ingresado)
        if distintos:
            if(nuevo_rol!=rol_actual):
                cambiar_rol(dni_ingresado, nuevo_rol)
                ui.notify('Rol cambiado exitosamente', color='positive')
            else:
                ui.notify('El usuario ingresado ya tiene el rol seleccionado', color='negative')
        else:
            ui.notify('No podes cambiar tu propio rol', color='negative')
    else:
        ui.notify('El usuario no existe', color='negative')