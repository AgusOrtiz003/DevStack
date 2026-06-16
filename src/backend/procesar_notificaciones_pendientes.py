import sqlite3

from datetime import date
from datetime import timedelta

from backend.crear_tabla_notificaciones import (
    crear_tablas_notificaciones
)

from backend.enviar_mail_notificacion import (
    enviar_mail_notificacion
)

DB_PATH = 'src/backend/bdd.db'


def procesar_notificaciones_pendientes():

    crear_tablas_notificaciones()

    manana = (
        date.today() + timedelta(days=1)
    ).strftime("%Y-%m-%d")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            dniPaciente,
            idReserva,
            asunto,
            mensaje,
            fechaHoraCreacion
        FROM NotificacionesPendientes
        WHERE fechaRecordatorio = ?
    """, (manana,))

    pendientes = cursor.fetchall()

    for (
        idNotificacion,
        dniPaciente,
        idReserva,
        asunto,
        mensaje,
        fechaHoraCreacion
    ) in pendientes:

        # =========================
        # Obtener email del usuario
        # =========================

        cursor.execute("""
            SELECT email
            FROM Usuarios
            WHERE dni = ?
        """, (dniPaciente,))

        resultado = cursor.fetchone()

        if resultado:

            email = resultado[0]

            try:

                enviar_mail_notificacion(
                    email,
                    asunto,
                    mensaje
                )

            except Exception as e:

                print(
                    f'Error enviando mail a {email}: {e}'
                )

        # =========================
        # Crear notificación interna
        # =========================

        cursor.execute("""
            INSERT INTO Notificaciones (
                dniPaciente,
                idReserva,
                asunto,
                mensaje,
                fechaHoraCreacion,
                leido
            )
            VALUES (?, ?, ?, ?, ?, 0)
        """, (
            dniPaciente,
            idReserva,
            asunto,
            mensaje,
            fechaHoraCreacion
        ))

        # =========================
        # Eliminar pendiente
        # =========================

        cursor.execute("""
            DELETE FROM NotificacionesPendientes
            WHERE id = ?
        """, (idNotificacion,))

    conn.commit()
    conn.close()