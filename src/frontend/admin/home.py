#!/usr/bin/env python3

import pathlib
import sys

from nicegui import app, ui

# =========================
# ROOT DIR
# =========================

ROOT_DIR = pathlib.Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT_DIR))

# =========================
# IMPORTS
# =========================

from backend.kinesiologos.registrarKinesiologo import (
    modal_registrar_kinesiologo
)

from backend.kinesiologos.listarKinesiologos import (
    tabla_kinesiologos
)

# =========================
# ADMIN HOME
# =========================

@ui.page('/Administrador/home')
def main_page() -> None:

    # =========================
    # LOGOUT
    # =========================

    def logout() -> None:

        app.storage.user.clear()
        ui.navigate.to('/login')

    # =========================
    # HEADER (RESTAURADO)
    # =========================

    with ui.header().classes('row items-center') as header:

        ui.button(
            on_click=lambda: left_drawer.toggle(),
            icon='menu'
        ).props('flat color=white')

        with ui.tabs() as tabs:

            tab_kines = ui.tab('Gestionar Kinesiologos')
            tab_b = ui.tab('B')
            tab_c = ui.tab('C')

    # =========================
    # FOOTER
    # =========================

    with ui.footer(value=False) as footer:
        ui.label('Footer')

    # =========================
    # DRAWER
    # =========================

    with ui.left_drawer().classes('bg-blue-100') as left_drawer:
        ui.label('Side menu')

    # =========================
    # TAB PANELS
    # =========================

    with ui.tab_panels(tabs, value=tab_kines).classes('w-full'):

        # =========================
        # A: KINESIÓLOGOS
        # =========================

        with ui.tab_panel(tab_kines):

            ui.label('Gestión de Kinesiólogos') \
                .classes('text-3xl font-bold')

            ui.separator()

            # BOTÓN
            ui.button(
                'Registrar Kinesiólogo',
                icon='person_add',
                on_click=modal_registrar_kinesiologo
            ).classes('mt-4 bg-primary text-white')

            # LISTA RETRÁCTIL
            with ui.expansion(
                'Listar Kinesiólogos',
                icon='groups'
            ).classes('w-full mt-4'):

                tabla_kinesiologos()

        # =========================
        # B
        # =========================

        with ui.tab_panel(tab_b):
            ui.label('Content of B')

        # =========================
        # C
        # =========================

        with ui.tab_panel(tab_c):
            ui.label('Content of C')

    # =========================
    # BOTÓN FLOTANTE
    # =========================

    with ui.page_sticky(
        position='bottom-right',
        x_offset=20,
        y_offset=20
    ):
        ui.button(
            on_click=footer.toggle,
            icon='contact_support'
        ).props('fab')