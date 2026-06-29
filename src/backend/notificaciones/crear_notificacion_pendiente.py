import sqlite3
from datetime import datetime

from backend.notificaciones.crear_tabla_notificaciones import crear_tablas_notificaciones

DB_PATH = 'src/backend/bdd.db'


def crear_notificacion_pendiente(
    dniPaciente,
    idReserva,
    asunto,
    mensaje,
    fechaRecordatorio
):

    crear_tablas_notificaciones()

    fechaHoraCreacion = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO NotificacionesPendientes (
            dniPaciente,
            idReserva,
            asunto,
            mensaje,
            fechaHoraCreacion,
            fechaRecordatorio
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        dniPaciente,
        idReserva,
        asunto,
        mensaje,
        fechaHoraCreacion,
        fechaRecordatorio
    ))

    conn.commit()
    conn.close()