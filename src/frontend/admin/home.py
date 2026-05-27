#!/usr/bin/env python3

import pathlib
import sys

src_path = pathlib.Path(__file__).resolve().parent.parent
sys.path.append(str(src_path))

from nicegui import app, ui

from frontend.admin.cambiar_rol import cambiar_rol_page
from frontend.perfil import perfil

from src.utils.fetch_usuarios import logout

from backend.kinesiologos.registar_kinesiologo import modal_registrar_kinesiologo
from backend.kinesiologos.borrar_kinesiologo import modal_borrar_kinesiologo
from backend.kinesiologos.listar_kinesiologos import obtener_kinesiologos
from backend.kinesiologos.buscar_kinesiologo import modal_buscar_kinesiologos

from backend.admin.cambiar_rol import modal_cambiar_rol
from backend.admin.listar_usuarios import tabla_usuarios


@ui.page('/Administrador/home')
def main_page() -> None:

    with ui.header().classes(replace='row items-center justify-between'):
        with ui.row().classes('items-center'):
            with ui.tabs() as tabs:
                ui.tab('Inicio', icon='home')
                ui.tab('Kinesiologos', icon='groups')
                ui.tab('Usuarios', icon='admin_panel_settings')
                ui.tab('Cambiar Rol', icon='event')

        with ui.row():
            ui.button(
                icon='account_circle'
            ).props('flat color=white round').on(
                'click',
                lambda: ui.navigate.to('/ver_perfil')
            )

            ui.button(
                on_click=logout,
                icon='logout'
            ).props('flat color=white round')

    with ui.tab_panels(tabs, value='Inicio').classes('w-full'):
        with ui.tab_panel('Inicio').classes('items-center'):
            with ui.column().classes('w-full items-center justify-center'):
                ui.image('src/frontend/icons/kinePro-logo.png').classes('w-110')
        with ui.tab_panel('Kinesiologos'):
            ui.label(
                'Gestión de Kinesiólogos'
            ).classes('text-3xl font-bold')
            ui.separator()
            with ui.row():
                ui.button(
                    'Registrar',
                    icon='person_add',
                    on_click=modal_registrar_kinesiologo
                )

                ui.button(
                    'Borrar',
                    icon='delete',
                    color='negative',
                    on_click=modal_borrar_kinesiologo
                )

                ui.button(
                    'Buscar / Filtrar',
                    icon='search',
                    on_click=lambda: modal_buscar_kinesiologos(renderizar_tabla)
                )

            tabla_container = ui.column().classes('w-full mt-4')

            def renderizar_tabla(datos):
                tabla_container.clear()
                columnas = [
                    {'name': 'cuit', 'label': 'CUIT', 'field': 'cuit'},
                    {'name': 'nombre', 'label': 'Nombre', 'field': 'nombre'},
                    {'name': 'apellido', 'label': 'Apellido', 'field': 'apellido'},
                ]
                rows = [
                    {
                        'cuit': k[0],
                        'nombre': k[1],
                        'apellido': k[2],
                    }
                    for k in datos
                ]
                with tabla_container:
                    ui.table(
                        columns=columnas,
                        rows=rows,
                        row_key='cuit'
                    ).classes('w-full')
            renderizar_tabla(obtener_kinesiologos())

        with ui.tab_panel('Usuarios'):

            ui.label(
                'Gestión de Usuarios'
            ).classes('text-3xl font-bold')

            ui.separator()

            ui.button(
                'Cambiar Rol',
                icon='admin_panel_settings',
                on_click=modal_cambiar_rol
            ).classes('mt-4')

            with ui.expansion(
                'Listar Usuarios',
                icon='groups'
            ).classes('w-full mt-4'):

                tabla_usuarios()

        with ui.tab_panel('Cambiar Rol').classes(
            'w-full items-center justify-center'
        ).style(
            'height: calc(100vh - 70px);'
        ):

            cambiar_rol_page()