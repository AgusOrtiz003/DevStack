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
# OBTENER USUARIOS
# =========================

def obtener_usuarios():

    try:

        conn = sqlite3.connect(str(DB_PATH))

        cursor = conn.cursor()

        cursor.execute("""
            SELECT

                dni,

                nombre,

                apellido,

                email,

                fechaNac,

                rol

            FROM Usuarios

            ORDER BY apellido, nombre
        """)

        datos = cursor.fetchall()

        conn.close()

        return datos

    except Exception as e:

        print(f'Error obteniendo usuarios: {e}')

        return []

# =========================
# TABLA USUARIOS
# =========================

def tabla_usuarios():

    filas = obtener_usuarios()

    columnas = [

        {
            'name': 'dni',
            'label': 'DNI',
            'field': 'dni',
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
            'name': 'email',
            'label': 'Email',
            'field': 'email',
            'align': 'left'
        },

        {
            'name': 'fechaNac',
            'label': 'Fecha Nacimiento',
            'field': 'fechaNac',
            'align': 'left'
        },

        {
            'name': 'rol',
            'label': 'Rol',
            'field': 'rol',
            'align': 'left'
        },
    ]

    rows = []

    for u in filas:

        rows.append({

            'dni': u[0],

            'nombre': u[1],

            'apellido': u[2],

            'email': u[3],

            'fechaNac': u[4],

            'rol': u[5],
        })

    return ui.table(
        columns=columnas,
        rows=rows,
        row_key='dni'
    ).classes('w-full')

# =========================
# TEST
# =========================

if __name__ == '__main__':

    ui.label(
        'Listado de Usuarios'
    ).classes('text-2xl font-bold')

    tabla_usuarios()

    ui.run()