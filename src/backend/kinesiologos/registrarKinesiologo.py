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
# REGLAS DE NEGOCIO
# =========================

HORARIOS_VALIDOS = [
    "08:00", "09:00", "10:00", "11:00",
    "12:00", "13:00", "14:00", "15:00",
    "16:00", "17:00", "18:00", "19:00",
    "20:00"
]

TRATAMIENTOS_VALIDOS = [
    "Tren superior",
    "Tren medio",
    "Tren inferior"
]

# =========================
# CREAR TABLA SI NO EXISTE
# =========================

def crear_tabla_kinesiologos():

    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Kinesiologos (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            nombre TEXT NOT NULL,

            apellido TEXT NOT NULL,

            cuit TEXT NOT NULL UNIQUE,

            horaDesde TIME NOT NULL,

            horaHasta TIME NOT NULL,

            tratamiento TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()

# =========================
# VALIDAR RANGO HORARIO
# =========================

def horario_valido(hora_desde, hora_hasta):

    try:

        return hora_desde <= hora_hasta

    except Exception:
        return False

# =========================
# REGISTRAR KINESIÓLOGO
# =========================

def registrar_kinesiologo(
    nombre,
    apellido,
    cuit,
    hora_desde,
    hora_hasta,
    tratamiento
):

    try:

        crear_tabla_kinesiologos()

        # =========================
        # VALIDACIONES
        # =========================

        if hora_desde not in HORARIOS_VALIDOS:
            ui.notify("Hora desde inválida", color="negative")
            return False

        if hora_hasta not in HORARIOS_VALIDOS:
            ui.notify("Hora hasta inválida", color="negative")
            return False

        if not horario_valido(hora_desde, hora_hasta):
            ui.notify(
                "La hora desde no puede ser mayor a la hora hasta",
                color="negative"
            )
            return False

        if tratamiento not in TRATAMIENTOS_VALIDOS:
            ui.notify("Tratamiento inválido", color="negative")
            return False

        conn = sqlite3.connect(str(DB_PATH))
        cursor = conn.cursor()

        # =========================
        # VALIDAR DUPLICADO
        # =========================

        cursor.execute("""
            SELECT id
            FROM Kinesiologos
            WHERE cuit = ?
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
                cuit,
                horaDesde,
                horaHasta,
                tratamiento

            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            nombre,
            apellido,
            cuit,
            hora_desde,
            hora_hasta,
            tratamiento
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

        # =========================
        # HORA DESDE
        # =========================
        ui.label("Hora desde").classes("font-bold")
        hora_desde = ui.select(
            HORARIOS_VALIDOS,
            label="Hora desde"
        )

        # =========================
        # HORA HASTA
        # =========================
        ui.label("Hora hasta").classes("font-bold")
        hora_hasta = ui.select(
            HORARIOS_VALIDOS,
            label="Hora hasta"
        )

        # =========================
        # TRATAMIENTO
        # =========================
        ui.label("Tratamiento").classes("font-bold")
        tratamiento = ui.select(
            TRATAMIENTOS_VALIDOS,
            label="Tratamiento"
        )

        # =========================
        # GUARDAR
        # =========================

        def guardar():

            if not all([
                nombre.value,
                apellido.value,
                cuit.value,
                hora_desde.value,
                hora_hasta.value,
                tratamiento.value
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
                hora_desde.value,
                hora_hasta.value,
                tratamiento.value
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