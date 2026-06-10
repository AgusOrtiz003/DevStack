import sqlite3

from nicegui import app, ui
from frontend.reservas.reservas import pagina_reservas
from frontend.reservas.listar_reservas import pagina_listar_reservas
from frontend.perfil import perfil
from src.utils.fetch_usuarios import logout

DB_PATH = 'src/backend/bdd.db'


def obtener_no_leidas():

    dni = app.storage.user.get('dni')

    if not dni:
        return 0

    with sqlite3.connect(DB_PATH) as conn:

        cursor = conn.cursor()

        cursor.execute("""
            SELECT COUNT(*)
            FROM Notificaciones
            WHERE dniPaciente = ?
            AND leido = 0
        """, (dni,))

        resultado = cursor.fetchone()

        return resultado[0] if resultado else 0


def marcar_como_leidas():

    dni = app.storage.user.get('dni')

    if not dni:
        return

    with sqlite3.connect(DB_PATH) as conn:

        cursor = conn.cursor()

        cursor.execute("""
            UPDATE Notificaciones
            SET leido = 1
            WHERE dniPaciente = ?
            AND leido = 0
        """, (dni,))

        conn.commit()


def obtener_notificaciones():

    dni = app.storage.user.get('dni')

    if not dni:
        return []

    with sqlite3.connect(DB_PATH) as conn:

        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                asunto,
                mensaje,
                fechaHoraCreacion,
                leido
            FROM Notificaciones
            WHERE dniPaciente = ?
            ORDER BY fechaHoraCreacion DESC
        """, (dni,))

        return cursor.fetchall()


@ui.page('/Paciente/home')
def main_page():

    with ui.header().classes(replace='row items-center gap-4'):

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

        with ui.row().classes('ml-auto items-center'):

            cantidad = obtener_no_leidas()

            badge = None

            def mostrar_notificaciones():

                nonlocal badge

                try:

                    marcar_como_leidas()

                    if badge:
                        badge.visible = False

                    notificaciones = obtener_notificaciones()

                    with ui.dialog() as dialog, ui.card().style(
                        'min-width:700px; max-width:900px'
                    ):

                        ui.label(
                            'Notificaciones'
                        ).classes(
                            'text-h5'
                        )

                        if not notificaciones:

                            ui.label(
                                'No tienes notificaciones.'
                            )

                        else:

                            with ui.scroll_area().style(
                                'height:500px; width:100%'
                            ):

                                for asunto, mensaje, fechaHora, leido in notificaciones:

                                    color = (
                                        '#f5f5f5'
                                        if leido
                                        else '#e3f2fd'
                                    )

                                    with ui.card().style(
                                        f'width:100%; background:{color};'
                                    ):

                                        with ui.row().classes(
                                            'w-full justify-between items-center'
                                        ):

                                            ui.label(
                                                asunto
                                            ).classes(
                                                'text-subtitle1 font-bold'
                                            )

                                            ui.label(
                                                str(fechaHora)
                                            ).classes(
                                                'text-caption'
                                            )

                                        ui.separator()

                                        ui.label(
                                            mensaje
                                        )

                        ui.button(
                            'Cerrar',
                            on_click=dialog.close
                        )

                    dialog.open()

                except Exception as e:

                    ui.notify(
                        f'Error al cargar notificaciones: {e}',
                        color='negative'
                    )

            with ui.button(
                icon='notifications',
                on_click=mostrar_notificaciones
            ).props('flat round color=white'):

                if cantidad > 0:

                    badge = ui.badge(
                        str(cantidad)
                    ).props(
                        'floating color=red'
                    )

            ui.button(
                icon='account_circle',
                on_click=lambda: ui.navigate.to('/ver_perfil')
            ).props(
                'flat round color=white'
            )

            ui.button(
                icon='logout',
                on_click=logout
            ).props(
                'flat round color=white'
            )

    with ui.tab_panels(
        tabs,
        value=inicio_tab
    ).classes('w-full'):

        with ui.tab_panel(inicio_tab).classes(
            'items-center'
        ):

            with ui.column().classes(
                'w-full items-center justify-center'
            ):

                ui.image(
                    'src/frontend/icons/kinePro-logo.png'
                ).classes(
                    'w-110'
                )

        with ui.tab_panel(reservas_tab):

            tabla_reservas = pagina_listar_reservas()

        with ui.tab_panel(reservar_tab):

            pagina_reservas(tabla_reservas)