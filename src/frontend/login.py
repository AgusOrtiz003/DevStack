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
from backend.login import chequearContraseña, getNombre, getRol
from frontend.pacientes.home import main_page as paciente_home
from frontend.secretarias.home import main_page as secretaria_home
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

    with ui.column().classes('absolute-center items-center'):
        ui.label(f'Bienvenido {app.storage.user["username"]}!').classes('text-2xl')
        ui.button(on_click=logout, icon='logout').props('outline round')

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
            username=getNombre(user)
            rol=getRol(user)
            app.storage.user.update(username=username, authenticated=True, dni=user, rol=rol)
            ui.navigate.to(f'/{rol}/home')
        else:
            ui.notify('Nombre de Usuario o Contraseña incorrectos', color='negative')

    def go_to_register():
        ui.navigate.to('/register')

    with ui.card().classes('absolute-center items-stretch'):
        username = ui.input('DNI').props('autofocus').on('keydown.enter', lambda: password.run_method('focus'))
        password = ui.input('Contraseña', password=True, password_toggle_button=True).on('keydown.enter', lambda: try_login(username.value, password.value))
        ui.button('Login', on_click=lambda: try_login(username.value, password.value))
        ui.button('Register', on_click=go_to_register)
    return None

if __name__ in {'__main__', '__mp_main__'}:
    ui.run(storage_secret='THIS_NEEDS_TO_BE_CHANGED',language='es')