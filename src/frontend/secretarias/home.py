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
from frontend.turnos.listar_turnos import pagina_listar_turnos_pendientes
from frontend.reservas.reservar_secretaria import pagina_reservar_secretaria
from src.utils.fetch_usuarios import *

# Página de secretaria
@ui.page('/Secretaria/home')
def main_page() -> None:
        
    with ui.header().classes(replace='row items-center gap-4') as header:
        with ui.tabs() as tabs:
            inicio_tab = ui.tab('Inicio',icon='home')
            turnosP_tab = ui.tab('Turnos pendientes',icon='calendar_month')
            reservar_tab = ui.tab('Reservar turno',icon='event')
        with ui.row().classes('ml-auto'):
            ui.button(icon='account_circle',on_click=lambda: ui.navigate.to('/ver_perfil')).props('flat color=white round')
            ui.button(on_click=lambda: logout(), icon='logout').props('flat color=white round')

    with ui.tab_panels(tabs, value='Inicio').classes('w-full'):
        with ui.tab_panel('Inicio').classes('items-center'):
            with ui.column().classes('w-full items-center justify-center'):
                ui.image('src/frontend/icons/kinePro-logo.png').classes('w-110')
        with ui.tab_panel('Turnos pendientes'):
            pagina_listar_turnos_pendientes()
        with ui.tab_panel('Reservar turno'):
            pagina_reservar_secretaria(tabs, inicio_tab)

ui.run(storage_secret='THIS_NEEDS_TO_BE_CHANGED')