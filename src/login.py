#!/usr/bin/env python3

import pathlib
import sys

# =========================
# ROOT DEL PROYECTO (src/)
# =========================

ROOT_DIR = pathlib.Path(__file__).resolve().parents[1]

sys.path.append(str(ROOT_DIR))

# =========================
# IMPORTS
# =========================
import pathlib
import sys
import sqlite3
from fastapi import Request
from fastapi.responses import RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware
src_path=pathlib.Path(__file__).resolve().parent.parent
sys.path.append(str(src_path))
from nicegui import app, ui
from backend.registro import registrar, cumple_edad, enviar_mail
from frontend.pacientes.home import main_page as paciente_home
from src.utils.fetch_usuarios import chequear_contraseña, get_datos, chequear_correo, existe, verificar_correo
# in reality users passwords would obviously need to be hashed
passwords = {'user1': 'pass1', 'user2': 'pass2'}

# top-level static routes like /favicon.ico must be unrestricted, otherwise the middleware redirects them to /login
unrestricted_page_routes = {'/favicon.ico', '/login','/register'}

@app.add_middleware
class AuthMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):

        path = request.url.path

        authenticated = app.storage.user.get('authenticated')
        rol = app.storage.user.get('rol')

        # usuario autenticado entrando a raíz
        if authenticated and path == '/':
            return RedirectResponse(f'/{rol}/home')

        # rutas permitidas sin login
        if (
            authenticated
            or path in unrestricted_page_routes
            or path.startswith('/_nicegui')
        ):
            return await call_next(request)

        # usuario no autenticado
        return RedirectResponse('/login')

@ui.page('/register')
def register() -> None:
    def try_register(dni, password, nombre, apellido, email, fechaNac):
        if all([dni, password, nombre, apellido, email, fechaNac]):
            if cumple_edad(fechaNac):
                if not existe(dni):
                    if verificar_correo(email):
                        if not chequear_correo(email):
                            registrar(dni, password, nombre, apellido, email, fechaNac)

                            ui.notify('Registro exitoso', color='positive')
                            ui.timer(2.5, lambda: ui.navigate.to('/login'),once=True)
                            enviar_mail(email,nombre,apellido)
                            ui.navigate.to('/login', timeout=3.0)
                        else:
                            ui.notify('El email ingresado ya tiene una cuenta asociada', color='negative')
                    else:
                        ui.notify('Email no válido')
                else:
                    ui.notify('El DNI ingresado ya existe', color='negative')
            else:
                ui.notify("Debes ser mayor de 13 años para crear una cuenta", color='negative')
        else:
            ui.notify("Tenes que llenar todos los campos para registrarte", color='negative')

    with ui.card().classes('absolute-center items-stretch'):
        dni = ui.input('DNI').props('autofocus').props('''inputmode=numeric maxlength=8 onkeypress="return event.charCode >= 48 && event.charCode <= 57"''').on('keydown.enter', lambda: password.run_method('focus'))
        password = ui.input('Contraseña', password=True, password_toggle_button=True)
        nombre = ui.input('Nombre/s').props('autofocus').on('keydown.enter', lambda: password.run_method('focus'))
        apellido = ui.input('Apellido').props('autofocus').on('keydown.enter', lambda: password.run_method('focus'))
        email = ui.input('Email').props('autofocus').on('keydown.enter', lambda: password.run_method('focus'))
        fnac = ui.date_input('Fecha de nacimiento').props('autofocus').on('keydown.enter', lambda: password.run_method('focus'))
        ui.button('Register', on_click=lambda: try_register(dni.value, password.value, nombre.value, apellido.value, email.value, fnac.value))
    return None

@ui.page('/login')
def login(redirect_to: str = '/'):

    # Si ya está logueado
    if app.storage.user.get('authenticated'):

        return RedirectResponse('/')

    def try_login(user,passwd) -> None:
        if(chequear_contraseña(user, passwd)):
            datos=get_datos(user)
            username=datos['nombre']
            rol=datos['rol']
            app.storage.user.update(username=username, authenticated=True, dni=user, rol=rol)
            ui.navigate.to(f'/{rol}/home')

        else:

            ui.notify(
                'Nombre de Usuario o Contraseña incorrectos',
                color='negative'
            )

    def go_to_register():

        ui.navigate.to('/register')

    # =========================
    # UI LOGIN
    # =========================

    with ui.card().classes('absolute-center items-stretch'):

        username = ui.input('DNI')

        password = ui.input(
            'Contraseña',
            password=True,
            password_toggle_button=True
        )

        password.on(
            'keydown.enter',
            lambda: try_login(
                username.value,
                password.value
            )
        )

        ui.button(
            'Login',
            on_click=lambda: try_login(
                username.value,
                password.value
            )
        )

        ui.button(
            'Register',
            on_click=go_to_register
        )

# =========================
# RUN
# =========================

if __name__ in {'__main__', '__mp_main__'}:

    ui.run(
        storage_secret='THIS_NEEDS_TO_BE_CHANGED',
        language='es'
    )
