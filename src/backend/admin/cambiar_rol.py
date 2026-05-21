#!/usr/bin/env python3

import pathlib
import sqlite3

from nicegui import ui

# =========================
# RUTA BASE
# =========================

BASE_DIR = pathlib.Path(__file__).resolve().parents[2]

DB_PATH = BASE_DIR / 'backend' / 'bdd.db'

# =========================
# ROLES VÁLIDOS
# =========================

ROLES_VALIDOS = [
    'Paciente',
    'Secretaria',
    'Administrador'
]

# =========================
# CAMBIAR ROL
# =========================

def cambiar_rol_usuario(dni, nuevo_rol):

    try:

        # =====================
        # VALIDAR INPUTS
        # =====================

        if not dni:

            ui.notify(
                'Debe ingresar un DNI',
                color='warning'
            )

            return False

        if nuevo_rol not in ROLES_VALIDOS:

            ui.notify(
                'Rol inválido',
                color='negative'
            )

            return False

        # =====================
        # CONEXIÓN DB
        # =====================

        conn = sqlite3.connect(str(DB_PATH))

        cursor = conn.cursor()

        # =====================
        # VERIFICAR USUARIO
        # =====================

        cursor.execute("""
            SELECT id, rol
            FROM Usuarios
            WHERE dni = ?
        """, (dni,))

        usuario = cursor.fetchone()

        if not usuario:

            conn.close()

            ui.notify(
                'No existe un usuario con ese DNI',
                color='negative'
            )

            return False

        # =====================
        # UPDATE
        # =====================

        cursor.execute("""
            UPDATE Usuarios
            SET rol = ?
            WHERE dni = ?
        """, (
            nuevo_rol,
            dni
        ))

        conn.commit()

        conn.close()

        ui.notify(
            'Rol actualizado correctamente',
            color='positive'
        )

        return True

    except Exception as e:

        print(f'Error cambiando rol: {e}')

        ui.notify(
            'Error cambiando rol',
            color='negative'
        )

        return False

# =========================
# MODAL CAMBIAR ROL
# =========================

def modal_cambiar_rol():

    with ui.dialog() as dialog, ui.card().classes('w-96'):

        ui.label(
            'Cambiar Rol de Usuario'
        ).classes(
            'text-xl font-bold'
        )

        # =====================
        # INPUT DNI
        # =====================

        dni_input = ui.input(
            'DNI'
        ).classes('w-full')

        # =====================
        # SELECT ROL
        # =====================

        rol_input = ui.select(
            ROLES_VALIDOS,
            label='Nuevo Rol'
        ).classes('w-full')

        # =====================
        # CONFIRMAR
        # =====================

        def confirmar():

            ok = cambiar_rol_usuario(
                dni_input.value,
                rol_input.value
            )

            if ok:

                dialog.close()

        # =====================
        # BOTONES
        # =====================

        with ui.row().classes(
            'w-full justify-end'
        ):

            ui.button(
                'Cancelar',
                on_click=dialog.close
            ).props('flat')

            ui.button(
                'Cambiar Rol',
                icon='admin_panel_settings',
                on_click=confirmar
            )

    dialog.open()

# =========================
# TEST
# =========================

if __name__ == '__main__':

    ui.button(
        'Cambiar Rol',
        on_click=modal_cambiar_rol
    )

    ui.run()