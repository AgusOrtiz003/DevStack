#!/usr/bin/env python3

import pathlib
import sqlite3

from nicegui import ui

# =========================
# ROOT
# =========================

BASE_DIR = pathlib.Path(__file__).resolve().parents[2]

DB_PATH = BASE_DIR / 'backend' / 'bdd.db'

# =========================
# CREAR TABLA
# =========================

def crear_tabla_kinesiologos():

    conn = sqlite3.connect(str(DB_PATH))

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Kinesiologos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            cuit TEXT NOT NULL UNIQUE
        )
    """)

    conn.commit()

    conn.close()

# =========================
# INSERTAR KINESIOLOGO
# =========================

def registrar_kinesiologo(
    nombre,
    apellido,
    cuit
):

    try:

        crear_tabla_kinesiologos()

        conn = sqlite3.connect(str(DB_PATH))

        cursor = conn.cursor()

        # =========================
        # VERIFICAR DUPLICADOS
        # =========================

        cursor.execute("""
            SELECT id
            FROM Kinesiologos
            WHERE cuit = ?
        """, (cuit,))

        existe = cursor.fetchone()

        if existe:

            conn.close()

            ui.notify(
                'El kinesiólogo ya existe',
                color='negative'
            )

            return False

        # =========================
        # INSERT
        # =========================

        cursor.execute("""
            INSERT INTO Kinesiologos (
                nombre,
                apellido,
                cuit
            )
            VALUES (?, ?, ?)
        """, (
            nombre,
            apellido,
            cuit
        ))

        conn.commit()

        conn.close()

        ui.notify(
            'Kinesiólogo registrado',
            color='positive'
        )

        return True

    except Exception as e:

        print(e)

        ui.notify(
            'Error registrando kinesiólogo',
            color='negative'
        )

        return False

# =========================
# MODAL NICEGUI
# =========================

def modal_registrar_kinesiologo():

    with ui.dialog() as dialog, ui.card().classes('w-96'):

        ui.label(
            'Registrar Kinesiólogo'
        ).classes('text-2xl font-bold')

        ui.separator()

        cuit = ui.input('CUIT')

        nombre = ui.input('Nombre')

        apellido = ui.input('Apellido')

        # =========================
        # GUARDAR
        # =========================

        def guardar():

            if (
                not cuit.value
                or not nombre.value
                or not apellido.value
            ):

                ui.notify(
                    'Complete todos los campos',
                    color='warning'
                )

                return

            ok = registrar_kinesiologo(
                nombre.value,
                apellido.value,
                cuit.value
            )

            if ok:

                dialog.close()

        # =========================
        # BOTONES
        # =========================

        with ui.row().classes(
            'w-full justify-end'
        ):

            ui.button(
                'Cancelar',
                on_click=dialog.close
            ).props('flat')

            ui.button(
                'Guardar',
                on_click=guardar
            )

    dialog.open()