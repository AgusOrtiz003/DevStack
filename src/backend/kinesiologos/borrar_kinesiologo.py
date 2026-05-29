#!/usr/bin/env python3

import pathlib
import sqlite3

from nicegui import ui

# =========================
# BASE DIR
# =========================

BASE_DIR = pathlib.Path(__file__).resolve().parents[2]

DB_PATH = BASE_DIR / 'backend' / 'bdd.db'

# =========================
# BORRAR KINESIÓLOGO
# =========================

def borrar_kinesiologo(cuit):

    try:

        # =====================
        # VALIDAR INPUT
        # =====================

        if not cuit:

            ui.notify(
                'Debe ingresar un CUIT',
                color='warning'
            )

            return False

        conn = sqlite3.connect(str(DB_PATH))

        cursor = conn.cursor()

        # =====================
        # VALIDAR EXISTENCIA
        # =====================

        cursor.execute("""
            SELECT idKinesiologo
            FROM Kinesiologos
            WHERE CUIT = ?
        """, (cuit,))

        kines = cursor.fetchone()

        if not kines:

            conn.close()

            ui.notify(
                'No existe un kinesiólogo con ese CUIT',
                color='negative'
            )

            return False

        # =====================
        # DELETE
        # =====================
        cuit_logico = f"{'*'}{cuit}"
        cursor.execute("""
            UPDATE Kinesiologos SET CUIT=?
            WHERE CUIT=?
        """, (cuit_logico,cuit,))

        conn.commit()

        conn.close()

        ui.notify(
            'Kinesiólogo eliminado correctamente',
            color='positive'
        )

        return True

    except Exception as e:

        print(f'Error borrando kinesiólogo: {e}')

        ui.notify(
            'Error borrando kinesiólogo',
            color='negative'
        )

        return False

# =========================
# MODAL BORRAR
# =========================

def modal_borrar_kinesiologo():

    with ui.dialog() as dialog, ui.card().classes('w-96'):

        ui.label(
            'Borrar Kinesiólogo'
        ).classes(
            'text-xl font-bold'
        )

        # =====================
        # INPUT CUIT
        # =====================

        cuit_input = ui.input(
            'CUIT'
        ).classes('w-full')

        # =====================
        # CONFIRMAR
        # =====================

        def confirmar():

            ok = borrar_kinesiologo(
                cuit_input.value
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
                'Borrar',
                icon='delete',
                color='negative',
                on_click=confirmar
            )

    dialog.open()

# =========================
# TEST
# =========================

if __name__ == '__main__':

    ui.button(
        'Borrar Kinesiólogo',
        on_click=modal_borrar_kinesiologo
    )

    ui.run()