#!/usr/bin/env python3

import pathlib
import sys

from fastapi import Request
from fastapi.responses import RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware
from backend.kinesiologos.registrarKinesiologo import (
    modal_registrar_kinesiologo
)
# =========================
# ROOT DIR
# =========================

ROOT_DIR = pathlib.Path(__file__).resolve().parents[1]

sys.path.append(str(ROOT_DIR))

# =========================
# IMPORTS
# =========================

from nicegui import app, ui

from backend.kinesiologos.registrarKinesiologo import (
    modal_registrar_kinesiologo
)

# =========================
# HOME ADMIN
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
    # HEADER
    # =========================

    with ui.header().classes(
        replace='row items-center'
    ) as header:

        ui.button(
            on_click=lambda: left_drawer.toggle(),
            icon='menu'
        ).props('flat color=white')

        with ui.tabs() as tabs:

            gestionar_kinesiologos_tab = ui.tab(
                'Gestionar Kinesiologos'
            )

            ui.tab('B')

            ui.tab('C')

    # =========================
    # FOOTER
    # =========================

    with ui.footer(value=False) as footer:

        ui.label('Footer')

    # =========================
    # DRAWER
    # =========================

    with ui.left_drawer().classes(
        'bg-blue-100'
    ) as left_drawer:

        ui.label('Side menu')

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

    # =========================
    # TAB PANELS
    # =========================

    with ui.tab_panels(
        tabs,
        value=gestionar_kinesiologos_tab
    ).classes('w-full'):

        # =========================
        # GESTIONAR KINESIÓLOGOS
        # =========================

        with ui.tab_panel(
            gestionar_kinesiologos_tab
        ):

            ui.label(
                'Gestión de Kinesiólogos'
            ).classes(
                'text-3xl font-bold'
            )

            ui.separator()

            ui.button(
                'Registrar Kinesiólogo',
                icon='person_add',
                on_click=modal_registrar_kinesiologo
            ).classes(
                'mt-4'
            )

        # =========================
        # TAB B
        # =========================

        with ui.tab_panel('B'):

            ui.label('Content of B')

        # =========================
        # TAB C
        # =========================

        with ui.tab_panel('C'):

            ui.label('Content of C')


# =========================
# RUN
# =========================

ui.run(
    storage_secret='THIS_NEEDS_TO_BE_CHANGED'
)