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
# REGLAS DE NEGOCIO
# =========================

HORARIOS_VALIDOS = [
    "08:00",
    "09:00",
    "10:00",
    "11:00",
    "12:00",
    "13:00",
    "14:00",
    "15:00",
    "16:00",
    "17:00",
    "18:00",
    "19:00",
    "20:00"
]

TRATAMIENTOS_VALIDOS = [
    "Tren superior",
    "Tren medio",
    "Tren inferior"
]

# =========================
# CREAR / RECREAR TABLA
# =========================

def crear_tabla_kinesiologos():

    try:

        conn = sqlite3.connect(str(DB_PATH))
        cursor = conn.cursor()

        # ⚠️ RECREAR TABLA PARA APLICAR CAMBIOS
        cursor.execute("DROP TABLE IF EXISTS Kinesiologos")

        cursor.execute("""
            CREATE TABLE Kinesiologos (

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

        print("Tabla Kinesiologos creada correctamente")

    except Exception as e:

        print(f"Error creando tabla: {e}")

# =========================
# EJECUCIÓN
# =========================

if __name__ == '__main__':

    crear_tabla_kinesiologos()