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

from backend.kinesiologos.registar_kinesiologo import (
    modal_registrar_kinesiologo
)

from backend.kinesiologos.listar_kinesiologos import (
    obtener_kinesiologos
)

from backend.kinesiologos.buscar_kinesiologo import (
    modal_buscar_kinesiologos
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
    # HEADER
    # =========================

    with ui.header().classes('row items-center'):

        ui.button(
            on_click=lambda: left_drawer.toggle(),
            icon='menu'
        ).props('flat color=white')

        with ui.tabs() as tabs:

            tab_kines = ui.tab(
                'Gestionar Kinesiologos'
            )

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

    with ui.left_drawer().classes(
        'bg-blue-100'
    ) as left_drawer:

        ui.label('Side menu')

    # =========================
    # TAB PANELS
    # =========================

    with ui.tab_panels(
        tabs,
        value=tab_kines
    ).classes('w-full'):

        # =====================================================
        # TAB KINESIÓLOGOS
        # =====================================================

        with ui.tab_panel(tab_kines):

            ui.label(
                'Gestión de Kinesiólogos'
            ).classes(
                'text-3xl font-bold'
            )

            ui.separator()

            # =========================
            # BOTÓN REGISTRAR
            # =========================

            ui.button(
                'Registrar Kinesiólogo',
                icon='person_add',
                on_click=modal_registrar_kinesiologo
            ).classes(
                'mt-4 bg-primary text-white'
            )

            # =========================
            # LISTAR KINESIÓLOGOS
            # =========================

            with ui.expansion(
                'Listar Kinesiologos',
                icon='groups'
            ).classes('w-full mt-4'):

                # =====================
                # CONTENEDOR TABLA
                # =====================

                tabla_container = ui.column().classes(
                    'w-full'
                )

                # =====================
                # RENDER TABLA
                # =====================

                def renderizar_tabla(datos):

                    tabla_container.clear()

                    columnas = [

                        {
                            'name': 'cuit',
                            'label': 'CUIT',
                            'field': 'cuit',
                            'align': 'left'
                        },

                        {
                            'name': 'nombre',
                            'label': 'Nombre',
                            'field': 'nombre',
                            'align': 'left'
                        },

                        {
                            'name': 'apellido',
                            'label': 'Apellido',
                            'field': 'apellido',
                            'align': 'left'
                        },

                        {
                            'name': 'horaDesde',
                            'label': 'Hora Desde',
                            'field': 'horaDesde',
                            'align': 'left'
                        },

                        {
                            'name': 'horaHasta',
                            'label': 'Hora Hasta',
                            'field': 'horaHasta',
                            'align': 'left'
                        },

                        {
                            'name': 'tratamiento',
                            'label': 'Tratamiento',
                            'field': 'tratamiento',
                            'align': 'left'
                        },
                    ]

                    rows = []

                    for k in datos:

                        rows.append({

                            'cuit': k[0],

                            'nombre': k[1],

                            'apellido': k[2],

                            'horaDesde': k[3],

                            'horaHasta': k[4],

                            'tratamiento': k[5],
                        })

                    with tabla_container:

                        ui.table(
                            columns=columnas,
                            rows=rows,
                            row_key='cuit'
                        ).classes('w-full')

                # =====================
                # BOTÓN BUSCAR
                # =====================

                ui.button(
                    'Buscar / Filtrar',
                    icon='search',
                    on_click=lambda: modal_buscar_kinesiologos(
                        renderizar_tabla
                    )
                ).classes('mb-4')

                # =====================
                # TABLA INICIAL
                # =====================

                renderizar_tabla(
                    obtener_kinesiologos()
                )

        # =====================================================
        # TAB B
        # =====================================================

        with ui.tab_panel(tab_b):

            ui.label('Content of B')

        # =====================================================
        # TAB C
        # =====================================================

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