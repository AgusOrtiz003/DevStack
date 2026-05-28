#!/usr/bin/env python3

import pathlib
import sqlite3

from nicegui import ui

# =========================
# RUTA DB
# =========================

BASE_DIR = pathlib.Path(__file__).resolve().parents[2]
DB_PATH = BASE_DIR / 'backend' / 'bdd.db'

# =========================
# REGISTRAR KINESIÓLOGO
# =========================

def registrar_kinesiologo(
    nombre,
    apellido,
    cuit
):

    try:

        conn = sqlite3.connect(str(DB_PATH))
        cursor = conn.cursor()

        cursor.execute("""
            SELECT idKinesiologo
            FROM Kinesiologos
            WHERE CUIT = ?
        """, (cuit,))

        if cursor.fetchone():

            conn.close()

            ui.notify(
                "El kinesiólogo ya existe",
                color="negative"
            )

            return False

        # =========================
        # INSERT
        # =========================

        cursor.execute("""
            INSERT INTO Kinesiologos (

                nombre,
                apellido,
                CUIT

            )
            VALUES (?, ?, ?)
        """, (
            nombre,
            apellido,
            cuit,
        ))

        conn.commit()
        conn.close()

        ui.notify(
            "Kinesiólogo registrado correctamente",
            color="positive"
        )

        return True

    except Exception as e:

        print(e)

        ui.notify(
            "Error registrando kinesiólogo",
            color="negative"
        )

        return False

# =========================
# MODAL NICEGUI
# =========================

def modal_registrar_kinesiologo():

    with ui.dialog() as dialog, ui.card().classes('w-96'):

        ui.label(
            "Registrar Kinesiólogo"
        ).classes("text-xl font-bold")

        # =========================
        # INPUTS
        # =========================

        nombre = ui.input("Nombre")

        apellido = ui.input("Apellido")

        cuit = ui.input("CUIT")

        def guardar():

            if not all([
                nombre.value,
                apellido.value,
                cuit.value,
            ]):

                ui.notify(
                    "Complete todos los campos",
                    color="warning"
                )

                return

            ok = registrar_kinesiologo(
                nombre.value,
                apellido.value,
                cuit.value,
            )

            if ok:
                dialog.close()
               

        # =========================
        # BOTONES
        # =========================

        with ui.row().classes("w-full justify-end"):

            ui.button(
                "Cancelar",
                on_click=dialog.close
            ).props("flat")

            ui.button(
                "Guardar",
                on_click=guardar
            )

    dialog.open()