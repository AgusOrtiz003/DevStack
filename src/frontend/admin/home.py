#!/usr/bin/env python3

import pathlib
import sys

src_path = pathlib.Path(__file__).resolve().parent.parent
sys.path.append(str(src_path))

from nicegui import app, ui

from frontend.perfil import perfil

from src.utils.fetch_usuarios import logout

from backend.kinesiologos.registar_kinesiologo import modal_registrar_kinesiologo
from backend.kinesiologos.borrar_kinesiologo import modal_borrar_kinesiologo
from backend.kinesiologos.listar_kinesiologos import obtener_kinesiologos
from backend.kinesiologos.buscar_kinesiologo import modal_buscar_kinesiologos


from frontend.admin.cambiar_rol import cambiar_rol_page
from frontend.turnos.cancelar_turno import pagina_cancelar_turno
from frontend.turnos.listar_turnos import pagina_listar_turnos_pendientes
from frontend.reservas.reservas_secretaria import pagina_reservas_secretaria
from frontend.turnos.crear_turno import pagina_crear_turno
from frontend.turnos.modificar_turno import pagina_modificar_turno


@ui.page('/Administrador/home')
def main_page() -> None:

    with ui.header().classes(replace='row items-center justify-between'):
        with ui.row().classes('items-center'):
            with ui.tabs() as tabs:
                ui.tab('Inicio', icon='home')
                ui.tab('Kinesiologos', icon='groups')
                ui.tab('Cambiar Rol', icon='event')
                ui.tab('Turnos pendientes',icon='calendar_month')
                ui.tab('Reservar turno',icon='event')
                ui.tab('Crear turno',icon='add')
                ui.tab('Modificar turnos',icon='edit_calendar')
                ui.tab('Cancelar Turnos', icon='event_busy')

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
                    {'name': 'cuit', 'label': 'CUIT', 'field': 'CUIT'},
                    {'name': 'nombre', 'label': 'Nombre', 'field': 'nombre'},
                    {'name': 'apellido', 'label': 'Apellido', 'field': 'apellido'},
                ]
                rows = [
                    {
                        'CUIT': k[1],
                        'nombre': k[2],
                        'apellido': k[3],
                    }
                    for k in datos
                ]
                with tabla_container:
                    tabla_kinesiologos = ui.table(
                        columns=columnas,
                        rows=rows,
                        row_key='CUIT'
                    ).classes('w-full')
                    with tabla_kinesiologos.add_slot('top-left'):
                        ui.button(icon='sync',on_click=lambda: renderizar_tabla(obtener_kinesiologos())).props('flat')

            renderizar_tabla(obtener_kinesiologos())

        with ui.tab_panel('Cambiar Rol').classes(
            'w-full items-center justify-center'
        ).style(
            'height: calc(100vh - 70px);'
        ):
            
            cambiar_rol_page()
        
        with ui.tab_panel('Turnos pendientes'):
            tabla_turnos = pagina_listar_turnos_pendientes()
        with ui.tab_panel('Reservar turno'):
            pagina_reservas_secretaria(tabla_turnos)
        with ui.tab_panel('Crear turno'):
            pagina_crear_turno(tabla_turnos)
        with ui.tab_panel('Modificar turnos'):
            pagina_modificar_turno(tabla_turnos)
        with ui.tab_panel('Cancelar Turnos'):
            pagina_cancelar_turno()