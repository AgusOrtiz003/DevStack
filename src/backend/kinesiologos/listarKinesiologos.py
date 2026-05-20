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
# OBTENER KINESIÓLOGOS
# =========================

def obtener_kinesiologos():

    try:

        conn = sqlite3.connect(str(DB_PATH))

        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                cuit,
                nombre,
                apellido
            FROM Kinesiologos
            ORDER BY apellido, nombre
        """)

        datos = cursor.fetchall()

        conn.close()

        return datos

    except Exception as e:

        print(f'Error obteniendo kinesiólogos: {e}')

        return []

# =========================
# TABLA NICEGUI
# =========================

def tabla_kinesiologos():

    filas = obtener_kinesiologos()

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
    ]

    rows = []

    for k in filas:

        rows.append({
            'cuit': k[0],
            'nombre': k[1],
            'apellido': k[2],
        })

    tabla = ui.table(
        columns=columnas,
        rows=rows,
        row_key='cuit'
    ).classes('w-full')

    return tabla

# =========================
# TEST
# =========================

if __name__ == '__main__':

    ui.label(
        'Listado de Kinesiólogos'
    ).classes('text-2xl font-bold')

    tabla_kinesiologos()

    ui.run()