import sqlite3

DB_PATH = 'src/backend/bdd.db'


def crear_tablas_notificaciones():

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS NotificacionesPendientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        dniPaciente INTEGER NOT NULL,
        idReserva INTEGER NOT NULL,
        asunto TEXT NOT NULL,
        mensaje TEXT NOT NULL,
        fechaHoraCreacion TIMESTAMP NOT NULL,
        fechaRecordatorio DATE NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Notificaciones (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        dniPaciente INTEGER NOT NULL,
        idReserva INTEGER NOT NULL,
        asunto TEXT NOT NULL,
        mensaje TEXT NOT NULL,
        fechaHoraCreacion TIMESTAMP NOT NULL,
        leido BOOLEAN NOT NULL DEFAULT 0
    )
    """)

    conn.commit()
    conn.close()