#!/usr/bin/env python3
import pathlib
import sys
import sqlite3
# Se deberia arreglar esto: from utils import imports
from fastapi import Request
from fastapi.responses import RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware
src_path=pathlib.Path(__file__).resolve().parent.parent
sys.path.append(str(src_path))
from nicegui import app, ui
from frontend.admin.cambiar_rol import cambiar_rol_page
from frontend.perfil import perfil 
from src.utils.fetch_usuarios import logout

@ui.page('/Administrador/home')        
def main_page() -> None:
    
    with ui.header().classes(replace='row items-center justify-between gap-4') as header:
        with ui.tabs() as tabs:
            ui.tab('Inicio',icon='home')
            ui.tab('Cambiar Rol',icon='event')
        ui.space()
        ui.button(icon='account_circle').props('flat color=white round').on('click', lambda: ui.navigate.to('/ver_perfil'))
        ui.button(on_click=logout, icon='logout').props('flat color=white round')
       #ui.button(on_click=lambda: left_drawer.toggle(), icon='menu').props('flat color=white')

    with ui.footer(value=False) as footer:
        ui.label('Footer')

    #with ui.right_drawer(value=False).classes('bg-blue-100') as left_drawer:
    #    ui.label('Side menu')

    with ui.tab_panels(tabs, value='Inicio').classes('w-full'):
        with ui.tab_panel('Inicio'):
            #ui.label(f'Bienvenido {app.storage.user["username"]}!').classes('text-bold')
            ui.label('Hola!')
        with ui.tab_panel('Cambiar Rol').classes('w-full items-center justify-center').style('height: calc(100vh - 70px);'):
            cambiar_rol_page()

ui.run(storage_secret='THIS_NEEDS_TO_BE_CHANGED')