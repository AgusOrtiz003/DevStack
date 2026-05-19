#!/usr/bin/env python3

import pathlib
import sqlite3

from nicegui import app, ui

from frontend.reservas.reservas import pagina_reservas
from frontend.reservas.listar_reservas import pagina_listar_reservas

# =========================
# BASE DIR
# =========================

BASE_DIR = pathlib.Path(__file__).resolve().parents[2]

DB_PATH = BASE_DIR / 'backend' / 'bdd.db'

# =========================
# OBTENER USUARIO
# =========================

def obtener_usuario(dni):

    try:

        conn = sqlite3.connect(str(DB_PATH))

        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                dni,
                nombre,
                apellido,
                email,
                fechaNac,
                rol
            FROM Usuarios
            WHERE dni = ?
        """, (dni,))

        usuario = cursor.fetchone()

        conn.close()

        return usuario

    except Exception as e:

        print('ERROR SQLITE:', e)

        return None


# =========================
# HOME PACIENTE
# =========================

@ui.page('/Paciente/home')
def main_page():

    # =========================
    # SESIÓN
    # =========================

    dni_usuario = app.storage.user.get('dni')

    usuario = None

    if dni_usuario:

        usuario = obtener_usuario(dni_usuario)

    # =========================
    # LOGOUT
    # =========================

    def logout():

        app.storage.user.clear()

        ui.navigate.to('/login')

    # =========================
    # DATOS USUARIO
    # =========================

    nombre = ''
    apellido = ''
    email = ''
    fechaNac = ''
    rol = ''
    dni = ''

    if usuario:

        dni, nombre, apellido, email, fechaNac, rol = usuario

    # =========================
    # HEADER
    # =========================

    with ui.header().classes('row items-center gap-4'):

        with ui.tabs() as tabs:

            inicio_tab = ui.tab(
                'Inicio',
                icon='home'
            )

            reservas_tab = ui.tab(
                'Mis reservas',
                icon='calendar_month'
            )

            reservar_tab = ui.tab(
                'Reservar turno',
                icon='event'
            )

        # =========================
        # BOTONES DERECHA
        # =========================

        with ui.row().classes('ml-auto items-center'):

            # =========================
            # MENU USUARIO
            # =========================

            with ui.button(
                icon='account_circle'
            ).props('flat round color=white'):

                with ui.menu():

                    ui.label(
                        f'{nombre} {apellido}'
                    ).classes('text-lg font-bold')

                    ui.separator()

                    ui.label(f'DNI: {dni}')
                    ui.label(f'Email: {email}')
                    ui.label(f'Fecha de nacimiento: {fechaNac}')
                    ui.label(f'Rol: {rol}')

            # =========================
            # LOGOUT
            # =========================

            ui.button(
                icon='logout',
                on_click=logout
            ).props('flat round color=white')

    # =========================
    # FOOTER
    # =========================

    with ui.footer(value=False):

        ui.label('Footer')

    # =========================
    # TAB PANELS
    # =========================

    with ui.tab_panels(
        tabs,
        value=reservas_tab
    ).classes('w-full'):

        # =========================
        # INICIO
        # =========================

        with ui.tab_panel(inicio_tab):

            ui.label(
                f'Hola, {nombre} {apellido}!'
            ).classes('text-3xl font-bold')

        # =========================
        # MIS RESERVAS
        # =========================

        with ui.tab_panel(reservas_tab):

            tabla_reservas = pagina_listar_reservas()

        # =========================
        # RESERVAR
        # =========================

        with ui.tab_panel(reservar_tab):

            pagina_reservas(
                tabs,
                reservas_tab,
                tabla_reservas
            )