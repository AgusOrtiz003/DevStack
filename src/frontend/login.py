#!/usr/bin/env python3

from fastapi import Request
from fastapi.responses import RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware

from nicegui import app, ui
from src.backend import registro

# in reality users passwords would obviously need to be hashed
passwords = {'user1': 'pass1', 'user2': 'pass2'}

# top-level static routes like /favicon.ico must be unrestricted, otherwise the middleware redirects them to /login
unrestricted_page_routes = {'/favicon.ico', '/login'}

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
        ui.label(f'Hello {app.storage.user["username"]}!').classes('text-2xl')
        ui.button(on_click=logout, icon='logout').props('outline round')

@ui.page('/subpage')
def test_page() -> None:
    ui.label('This is a sub page.')

@ui.page('/login')
def login(redirect_to: str = '/') -> RedirectResponse | None:
    if app.storage.user.get('authenticated'):
        return RedirectResponse('/')

    def try_login() -> None:
        if passwords.get(username.value) == password.value:
            app.storage.user.update(username=username.value, authenticated=True)
            ui.navigate.to(redirect_to)  # go back to where the user wanted to go
        else:
            ui.notify('Nombre de Usuario o Contraseña incorrectos', color='negative')

    with ui.card().classes('absolute-center items-stretch'):
        username = ui.input('DNI').props('autofocus').on('keydown.enter', lambda: password.run_method('focus'))
        password = ui.input('Contraseña', password=True, password_toggle_button=True).on('keydown.enter', try_login)
        ui.button('Login', on_click=try_login)
        ui.button('Register', on_click=None)

    return None
## VOY A HACER QUE SE LOGUEEN CON SU DNI
@ui.page('/register')
    with ui.card().classes('absolute-center items-stretch'):
        dni = ui.input('DNI').props('autofocus').on('keydown.enter', lambda: password.run_method('focus'))
        password = ui.input('Contraseña', password=True, password_toggle_button=True).on('keydown.enter', try_login)
        nombre = ui.input('Nombre/s').props('autofocus').on('keydown.enter', lambda: password.run_method('focus'))
        apellido = ui.input('Apellido').props('autofocus').on('keydown.enter', lambda: password.run_method('focus'))
        email = ui.input('Email').props('autofocus').on('keydown.enter', lambda: password.run_method('focus'))
        fnac = ui.input('Fecha de nacimiento').props('autofocus').on('keydown.enter', lambda: password.run_method('focus'))
        ui.button('Register', on_click=)
    
if __name__ in {'__main__', '__mp_main__'}:
    ui.run(storage_secret='THIS_NEEDS_TO_BE_CHANGED')