#!/usr/bin/env python3

import pathlib
import sqlite3

# =========================
# BASE DIR
# =========================

BASE_DIR = pathlib.Path(__file__).resolve().parents[2]

DB_PATH = BASE_DIR / 'backend' / 'bdd.db'

# =========================
# OBTENER KINESIÓLOGOS
# =========================

def obtener_kinesiologos():

    with sqlite3.connect(str(DB_PATH)) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT idKinesiologo, CUIT, nombre, apellido FROM Kinesiologos ORDER BY apellido, nombre')
        datos = cursor.fetchall()
        return datos
    