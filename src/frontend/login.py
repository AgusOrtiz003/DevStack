#!/usr/bin/env python3
import pathlib
import sys
import sqlite3
from fastapi import Request
from fastapi.responses import RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware
src_path=pathlib.Path(__file__).resolve().parent.parent
sys.path.append(str(src_path))
from nicegui import app, ui
from backend.registro import registrar
from backend.login import chequearContraseña
from frontend.pages.reservas import reservas
# in reality users passwords would obviously need to be hashed
passwords = {'user1': 'pass1', 'user2': 'pass2'}

# top-level static routes like /favicon.ico must be unrestricted, otherwise the middleware redirects them to /login
unrestricted_page_routes = {'/favicon.ico', '/login','/register'}

@app.add_middleware
class AuthMiddleware(BaseHTTPMiddleware):
    """This middleware restricts access to all NiceGUI pages.

    It redirects the user to the login page if they are not authenticated.
    """

    async def dispatch(self, request: Request, call_next):
        path = request.url.path
        if app.storage.user.get('authenticated') or path in unrestricted_page_routes or path.startswith('/_nicegui'):
            return await call_next(request)
        return RedirectResponse(f'/login?redirect_to={path}')

@ui.page('/')
def main_page() -> None:
    def logout() -> None:
        app.storage.user.clear()
        ui.navigate.to('/login')

    ui.page_title('Página principal')
    ui.query('body').style('background-color: #1E73B7')

    with ui.header().classes('bg-transparent items-center'):
        ui.button(on_click=logout, icon='logout').classes('bg-transparent text-white').props('flat')

    with ui.card().classes('fixed-center items-center').classes('w-80'):
        ui.image('src/frontend/icons/kinePro-logo.png').classes('h-full w-30 object-contain')
        ui.button('Reservar turno', icon='event', on_click=lambda: ui.navigate.to('/reservas')).classes('w-full justify-start').props('align="left"')
        ui.button('Listar turnos', icon='list', on_click=lambda: ui.navigate.to('/listarTurnos')).classes('w-full justify-start').props('align="left"')

## VOY A HACER QUE SE LOGUEEN CON SU DNI
@ui.page('/register')
def register() -> None:
    def try_register(dni, password, nombre, apellido, email, fechaNac):
        if registrar(dni, password, nombre, apellido, email, fechaNac):
            ui.notify('Registro exitoso', color='positive')
            ui.navigate.to('/login')
        else:
            ui.notify('El DNI ya existe', color='negative')
            
    with ui.card().classes('absolute-center items-stretch'):
        dni = ui.input('DNI').props('autofocus').on('keydown.enter', lambda: password.run_method('focus'))
        password = ui.input('Contraseña', password=True, password_toggle_button=True)
        nombre = ui.input('Nombre/s').props('autofocus').on('keydown.enter', lambda: password.run_method('focus'))
        apellido = ui.input('Apellido').props('autofocus').on('keydown.enter', lambda: password.run_method('focus'))
        email = ui.input('Email').props('autofocus').on('keydown.enter', lambda: password.run_method('focus'))
        fnac = ui.date_input('Fecha de nacimiento').props('autofocus').on('keydown.enter', lambda: password.run_method('focus'))
        ui.button('Register', on_click=lambda: try_register(dni.value, password.value, nombre.value, apellido.value, email.value, fnac.value))
    
    return None    

@ui.page('/login')
def login(redirect_to: str = '/') -> RedirectResponse | None:
    if app.storage.user.get('authenticated'):
        return RedirectResponse('/')

    def try_login(user,passwd) -> None:        
        if(chequearContraseña(user, passwd)):
            app.storage.user.update(username=username.value, authenticated=True)
            ui.navigate.to(redirect_to)  # go back to where the user wanted to go
        else:
            ui.notify('Nombre de Usuario o Contraseña incorrectos', color='negative')
            
    def go_to_register():
        ui.navigate.to('/register')

    with ui.card().classes('absolute-center items-stretch'):
        username = ui.input('DNI').props('autofocus').on('keydown.enter', lambda: password.run_method('focus'))
        password = ui.input('Contraseña', password=True, password_toggle_button=True).on('keydown.enter', try_login)
        ui.button('Login', on_click=lambda: try_login(username.value, password.value))
        ui.button('Register', on_click=go_to_register)

    return None

if __name__ in {'__main__', '__mp_main__'}:
    ui.run(storage_secret='THIS_NEEDS_TO_BE_CHANGED',language='es')