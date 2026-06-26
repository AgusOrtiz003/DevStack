from nicegui import app, ui
from backend.reservas.usuario_tiene_reservas import usuario_tiene_reservas
from backend.admin.cambiar_rol import cambiar_rol
from src.utils.fetch_usuarios import existe, get_datos

@ui.page('/Administrador/cambiar_rol')
def cambiar_rol_page():
    with ui.card().classes('w-50'):
        dni_input = ui.input('DNI del usuario').props('autofocus')
        nuevo_rol_input = ui.select(['Paciente', 'Secretaria', 'Administrador'], label='Nuevo rol')
        ui.button('Cambiar rol', on_click=lambda: try_cambiar_rol(app.storage.user['dni'], dni_input.value, nuevo_rol_input.value))
    
def try_cambiar_rol(dni_admin,dni_ingresado,nuevo_rol):
    if(existe(dni_ingresado)):
        rol_actual=get_datos(dni_ingresado)['rol']
        distintos=(dni_admin!=dni_ingresado)
        if distintos:
            if not(rol_actual=='Administrador'):
                if(nuevo_rol!=rol_actual):
                    if(rol_actual=='Paciente' and usuario_tiene_reservas(dni_ingresado)):
                        ui.notify('No se puede cambiar el rol de un paciente con reservas activas', color='negative')
                    else:
                        cambiar_rol(dni_ingresado, nuevo_rol)
                        ui.notify('Rol cambiado exitosamente', color='positive')
                else:
                    ui.notify('El usuario ingresado ya tiene el rol seleccionado', color='negative')
            else:
                ui.notify('No podes cambiar el rol de otro administrador', color='negative')
        else:
            ui.notify('No podes cambiar tu propio rol', color='negative')
    else:
        ui.notify('El usuario no existe', color='negative')