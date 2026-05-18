import sqlite3
from datetime import datetime, timedelta

DB_PATH = 'src/backend/bdd.db'


def turno_pendiente(id_turno):
    conexion = sqlite3.connect(DB_PATH)

    cursor = conexion.cursor()

    cursor.execute("""
        SELECT fecha, hora
        FROM turnos
        WHERE id = ?
    """, (id_turno,))

    resultado = cursor.fetchone()

    conexion.close()

    # Si el turno no existe
    if resultado is None:
        return False

    fecha, hora = resultado

    # Convertir fecha y hora del turno a datetime
    fecha_hora_turno = datetime.strptime(
        f'{fecha} {hora}',
        '%Y-%m-%d %H:%M'
    )

    # Restar 1 hora
    limite_pendiente = fecha_hora_turno - timedelta(hours=1)

    # Hora actual
    ahora = datetime.now()

    # Sigue pendiente solamente si todavía falta más de 1 hora
    return ahora < limite_pendiente