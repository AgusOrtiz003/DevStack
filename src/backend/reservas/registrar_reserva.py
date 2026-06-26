import sqlite3

from backend.registro import existe
from backend.exceptions.turno_lleno_exception import TurnoLlenoException
from backend.crear_notificacion_pendiente import crear_notificacion_pendiente


def registrar_reserva(idTurno, obraSoc, metPag, dniPac):

    with sqlite3.connect('src/backend/bdd.db') as conexion:
        conexion.execute('PRAGMA foreign_keys = ON')

        cursor = conexion.cursor()

        if not existe(dniPac):
            raise ValueError('El DNI no está registrado')

        cursor.execute('''
            SELECT
                cupoActual,
                cupoMaximo
            FROM Turnos
            WHERE idTurno = ?
        ''', (idTurno,))

        turno = cursor.fetchone()

        if turno is None:
            raise ValueError('El turno no existe')

        cupoActual = turno[0]
        cupoMaximo = turno[1]

        if cupoActual >= cupoMaximo:
            raise TurnoLlenoException('Turno lleno')

        # Crear reserva
        cursor.execute('''
            INSERT INTO Reservas (
                dniPaciente,
                idTurno,
                obraSocial,
                metodoPago
            )
            VALUES (?, ?, ?, ?)
        ''', (
            dniPac,
            idTurno,
            obraSoc,
            metPag
        ))

        idReserva = cursor.lastrowid

        # Actualizar cupo del turno
        cursor.execute('''
            UPDATE Turnos
            SET cupoActual = cupoActual + 1
            WHERE idTurno = ?
        ''', (idTurno,))

        # Obtener fecha y hora del turno
        cursor.execute('''
            SELECT fecha, hora
            FROM Turnos
            WHERE idTurno = ?
        ''', (idTurno,))

        datos_turno = cursor.fetchone()

        if datos_turno is None:
            raise ValueError('No se encontraron los datos del turno')

        fecha_turno = datos_turno[0]
        hora_turno = datos_turno[1]

        # IMPORTANTE:
        # guardar primero los cambios para liberar el lock
        conexion.commit()

    # Crear notificación pendiente fuera de la conexión anterior
    crear_notificacion_pendiente(
        dniPaciente=dniPac,
        idReserva=idReserva,
        fechaRecordatorio=fecha_turno,
        asunto='Recordatorio de turno',
        mensaje=(
            f'Tienes un turno reservado para el día '
            f'{fecha_turno} a las {hora_turno}.'
        )
    )