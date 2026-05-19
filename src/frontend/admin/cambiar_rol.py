from nicegui import ui

from backend.cambiarRol import cambiar_rol

@ui.page('/Administrador/cambiar_rol')
def cambiar_rol_page():
    with ui.card().classes('absolute-center items-stretch'):
        dni_input = ui.input('DNI del usuario').props('autofocus')
        nuevo_rol_input = ui.select(['Paciente', 'Medico', 'Administrador'], label='Nuevo rol')
        ui.button('Cambiar rol', on_click=lambda: cambiar_rol(dni_input.value, nuevo_rol_input.value))
