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
from frontend.reservas.reservas import pagina_reservas
from frontend.reservas.listar_reservas import pagina_listar_reservas

@ui.page('/Paciente/home')
def main_page() -> None:
    def logout() -> None:
        app.storage.user.clear()
        ui.navigate.to('/login')
    
    with ui.header().classes(replace='row items-center gap-4') as header:
        with ui.tabs() as tabs:
            inicio_tab = ui.tab('Inicio',icon='home')
            reservas_tab = ui.tab('Mis reservas',icon='calendar_month')
            reservar_tab = ui.tab('Reservar turno',icon='event')
        with ui.row().classes('ml-auto'):
            ui.button(icon='account_circle').props('flat color=white round')
            ui.button(on_click=logout, icon='logout').props('flat color=white round')

    with ui.footer(value=False) as footer:
        ui.label('Footer')

    with ui.tab_panels(tabs, value='Inicio').classes('w-full'):
        with ui.tab_panel('Inicio'):
            ui.label('Hola!')
        with ui.tab_panel('Mis reservas'):
            tabla_reservas = pagina_listar_reservas()
        with ui.tab_panel('Reservar turno'):
            pagina_reservas(tabs, reservas_tab, tabla_reservas)

ui.run(storage_secret='THIS_NEEDS_TO_BE_CHANGED')