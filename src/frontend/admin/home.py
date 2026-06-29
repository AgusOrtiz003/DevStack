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
from backend.empleados.listar_pacientes import obtener_pacientes
from backend.admin.banear_paciente import modal_cambiar_estado_paciente
from backend.admin.buscar_pacientes import modal_buscar_pacientes
from backend.admin.listar_secretarias import obtener_secretarias
from backend.admin.buscar_secretarias import modal_buscar_secretarias
from frontend.admin.cambiar_rol import cambiar_rol_page
from frontend.turnos.cancelar_turno import pagina_cancelar_turno
from frontend.turnos.listar_turnos import pagina_listar_turnos_pendientes
from frontend.reservas.reservas_secretaria import pagina_reservas_secretaria
from frontend.turnos.crear_turno import pagina_crear_turno
from frontend.turnos.modificar_turno import pagina_modificar_turno


@ui.page('/Administrador/home')
def main_page() -> None:

    with ui.header().classes(replace='row items-center gap-4 no-wrap'):
            with ui.tabs().classes('flex-1 min-w-0') as tabs:
                ui.tab('Inicio', icon='home')
                ui.tab('Kinesiologos', icon='person')
                ui.tab('Secretarias', icon='badge')
                ui.tab('Pacientes', icon='groups')
                ui.tab('Cambiar Rol', icon='manage_accounts')
                ui.tab('Turnos pendientes', icon='pending_actions')
                ui.tab('Reservar turno', icon='event_available')
                ui.tab('Crear turno', icon='event_note')
                ui.tab('Modificar turnos', icon='edit_calendar')
                ui.tab('Cancelar Turnos', icon='event_busy')

            with ui.row().classes('items-center gap-1 shrink-0'):
                ui.button(
                    icon='account_circle',
                    on_click=lambda: ui.navigate.to('/ver_perfil')
                ).props('flat round color=white')
                ui.button(
                    icon='logout',
                    on_click=logout
                ).props('flat round color=white')


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

        with ui.tab_panel('Secretarias'):

            ui.label(
                'Listado de Secretarias'
            ).classes('text-3xl font-bold')

            ui.separator()

            with ui.row():

                ui.button(
                    'Buscar / Filtrar',
                    icon='search',
                    on_click=lambda:
                    modal_buscar_secretarias(
                        renderizar_tabla_secretarias
                    )
                )

            tabla_secretarias_container = ui.column().classes(
                'w-full mt-4'
            )

            def renderizar_tabla_secretarias(datos=None):

                tabla_secretarias_container.clear()

                secretarias = (
                    datos
                    if datos is not None
                    else obtener_secretarias()
                )

                columnas = [
                    {
                        'name': 'dni',
                        'label': 'DNI',
                        'field': 'dni'
                    },
                    {
                        'name': 'nombre',
                        'label': 'Nombre',
                        'field': 'nombre'
                    },
                    {
                        'name': 'apellido',
                        'label': 'Apellido',
                        'field': 'apellido'
                    },
                    {
                        'name': 'email',
                        'label': 'Email',
                        'field': 'email'
                    },
                    {
                        'name': 'fechaNac',
                        'label': 'Fecha Nacimiento',
                        'field': 'fechaNac'
                    },
                    {
                        'name': 'rol',
                        'label': 'Rol',
                        'field': 'rol'
                    }
                ]

                rows = [
                    {
                        'dni': s[0],
                        'nombre': s[1],
                        'apellido': s[2],
                        'email': s[3],
                        'fechaNac': s[4],
                        'rol': s[5]
                    }
                    for s in secretarias
                ]

                with tabla_secretarias_container:

                    tabla = ui.table(
                        columns=columnas,
                        rows=rows,
                        row_key='dni'
                    ).classes('w-full')

                    with tabla.add_slot('top-left'):

                        ui.button(
                            icon='sync',
                            on_click=lambda:
                            renderizar_tabla_secretarias(
                                obtener_secretarias()
                            )
                        ).props('flat')

            renderizar_tabla_secretarias()
        
        with ui.tab_panel('Pacientes'):

            ui.label(
                'Listado de Pacientes'
            ).classes('text-3xl font-bold')

            ui.separator()

            with ui.row():

                ui.button(
                    'Banear/Desbanear',
                    icon='block',
                    on_click=modal_cambiar_estado_paciente
                )
                ui.button(
                    'Buscar / Filtrar',
                    icon='search',
                    on_click=lambda: modal_buscar_pacientes(
                        renderizar_tabla_pacientes
                    )
                )

            tabla_pacientes_container = ui.column().classes('w-full mt-4')


            def renderizar_tabla_pacientes(datos=None):

                tabla_pacientes_container.clear()

                pacientes = datos if datos is not None else obtener_pacientes()



                columnas = [
                    {
                        'name': 'dni',
                        'label': 'DNI',
                        'field': 'dni'
                    },
                    {
                        'name': 'nombre',
                        'label': 'Nombre',
                        'field': 'nombre'
                    },
                    {
                        'name': 'apellido',
                        'label': 'Apellido',
                        'field': 'apellido'
                    },
                    {
                        'name': 'email',
                        'label': 'Email',
                        'field': 'email'
                    },
                    {
                        'name': 'fechaNac',
                        'label': 'Fecha Nac.',
                        'field': 'fechaNac'
                    },
                    {
                        'name': 'rol',
                        'label': 'Rol',
                        'field': 'rol'
                    }
                ]

                rows = [
                    {
                        'dni': p[0],
                        'nombre': p[1],
                        'apellido': p[2],
                        'email': p[3],
                        'fechaNac': p[4],
                        'rol': '🚫 Baneado' if p[5] == 'Baneado' else 'Paciente'
                    }
                    for p in pacientes
                ]

                with tabla_pacientes_container:

                    tabla = ui.table(
                        columns=columnas,
                        rows=rows,
                        row_key='dni'
                    ).classes('w-full')

                    with tabla.add_slot('top-left'):

                        ui.button(
                            icon='sync',
                            on_click=lambda: renderizar_tabla_pacientes(
                                obtener_pacientes()
                            )
                        ).props('flat')

            renderizar_tabla_pacientes()
        
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