#!/usr/bin/env python3

import pathlib
import sqlite3

# =========================
# RUTA BASE
# =========================

BASE_DIR = pathlib.Path(__file__).resolve().parents[2]

DB_PATH = BASE_DIR / 'backend' / 'bdd.db'

print(f'Usando base de datos: {DB_PATH}')

# =========================
# CREAR TABLA
# =========================

def crear_tabla_kinesiologos():

    try:

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

        print('Tabla Kinesiologos creada correctamente')

    except Exception as e:

        print(f'Error creando tabla: {e}')


# =========================
# EJECUCIÓN
# =========================

if __name__ == '__main__':

    crear_tabla_kinesiologos()