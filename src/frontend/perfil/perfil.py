from nicegui import app,ui
import utils.imports as imports 
from pacientes.home import logout 
from src.utils import fetch_usuarios
from backend.reservas.usuario_tiene_reservas import usuario_tiene_reservas
@ui.page('/ver_perfil')
def ver_perfil ():
    
    
    usuario = fetch_usuarios.get_datos(app.storage.user["dni"])
    
    def try_eliminar_cuenta(dni):
        if (usuario_tiene_reservas(dni)):
            ui.notify("No se puede eliminar la cuenta porque tiene reservas activas", color = "red")
        else:
            fetch_usuarios.eliminar_cuenta(usuario["dni"])
   
   
    ui.run_javascript('localStorage.clear()')
   
   
    with ui.dialog() as dialog, ui.card():
        ui.label('¿Seguro que querés eliminar tu cuenta?').classes('text-lg')

        with ui.row().classes('justify-end w-full gap-2 mt-4'):
            ui.button('Cancelar', on_click=dialog.close)

            ui.button('Eliminar',on_click=lambda: (try_eliminar_cuenta(usuario["dni"]),dialog.close() )).classes('bg-red-600 text-white')
    
    
    
        
        
    with ui.dialog() as cambio_correo, ui.card():
        ui.label('Ingrese un nuevo correo para cambiarlo').classes('text-lg')
        correo = ui.input().on('keydown.enter', lambda: change_email(correo.value))

        with ui.row().classes('justify-end w-full gap-2 mt-4'):
            ui.button('Cancelar', on_click=cambio_correo.close)

            ui.button('Confirmar',on_click=lambda: change_email(correo.value) )
    
    
    with ui.dialog() as confirmar_contra, ui.card():
        ui.label('Ingrese su contraseña para hacer el cambio de correo')
        
        contra = ui.input(password=True ,password_toggle_button=True).on('keydown.enter', lambda: cerrar_contra(contra.value))
        
        with ui.row().classes('justify-end w-full gap-2 mt-4'):
            
            ui.button('Cancelar', on_click= confirmar_contra.close)
        
            ui.button('Comprobar', on_click =lambda:  cerrar_contra(contra.value))
    
    def abrir_dialogo():
        dialog.open()
    
    def cerrar_contra(contrasenia):
        if(contrasenia == ""): 
            ui.notify("Ingrese una contraseña", color = "red")
        else :
            if(fetch_usuarios.chequear_contraseña(usuario["dni"],contrasenia)):
                confirmar_contra.close()
                cambio_correo.open()
            else:
                ui.notify ("La contraseña no es correcta", color = "red")
            
        
    def change_email(correo):
        if(fetch_usuarios.verificar_correo(correo)):
            if (not fetch_usuarios.chequear_correo(correo)):
                fetch_usuarios.cambiar_correo(correo,usuario["dni"])
                cambio_correo.close()
                ui.navigate.reload()
            else:
                ui.notify("El correo ya se encuentra registrado en el sistema", color= "red")
        else:
            ui.notify("Correo no valido", color= "red")
        
        

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
            with ui.label(f'Email : {usuario['email']}').classes('text-2xl font-bold text-blue-500 mb-4'):
                ui.button(icon ="edit", on_click= confirmar_contra.open).classes('ml-2')
            ui.label(f'Fecha de nacimiento : {usuario['fechaNac']}').classes('text-2xl font-bold text-blue-500 mb-4')
            if (usuario["rol"] == "Paciente"):
                ui.button('Eliminar cuenta',on_click= abrir_dialogo).classes('bg-red-600 text-white mt-4 px-6 py-2 rounded-lg ')
        

 
            
            # chequear con contraseña a la hora 