import sqlite3

from backend.registro import existe
from backend.exceptions.turno_lleno_exception import TurnoLlenoException
from backend.crear_notificacion_pendiente import crear_notificacion_pendiente


def registrar_reservas_recurrentes(
    idsTurnos,
    obraSoc,
    metPag,
    dniPac
):

    if not idsTurnos:
        raise ValueError(
            'No se recibieron turnos'
        )

    with sqlite3.connect('src/backend/bdd.db') as conexion:

        conexion.execute(
            'PRAGMA foreign_keys = ON'
        )

        cursor = conexion.cursor()

        if not existe(dniPac):
            raise ValueError(
                'El DNI no está registrado'
            )

        cantidad_turnos = len(idsTurnos)

        descuento = cantidad_turnos >= 2

        # Crear la reserva recurrente
        cursor.execute('''
            INSERT INTO ReservasRecurrentes (
                cantidad,
                descuento,
                pago
            )
            VALUES (?, ?, ?)
        ''', (
            cantidad_turnos,
            descuento,
            False
        ))

        idReservaRecurrente = cursor.lastrowid

        datos_notificaciones = []

        for idTurno in idsTurnos:

            cursor.execute('''
                SELECT
                    cupoRecurrenteActual,
                    cupoRecurrenteMaximo,
                    fecha,
                    hora
                FROM Turnos
                WHERE idTurno = ?
            ''', (idTurno,))

            turno = cursor.fetchone()

            if turno is None:
                raise ValueError(
                    f'El turno {idTurno} no existe'
                )

            cupo_actual = turno[0]
            cupo_maximo = turno[1]

            if cupo_actual >= cupo_maximo:
                raise TurnoLlenoException(
                    'Uno de los turnos ya no tiene cupos recurrentes'
                )

            cursor.execute('''
                INSERT INTO Reservas (
                    dniPaciente,
                    idTurno,
                    obraSocial,
                    metodoPago,
                    idReservaRecurrente
                )
                VALUES (?, ?, ?, ?, ?)
            ''', (
                dniPac,
                idTurno,
                obraSoc,
                metPag,
                idReservaRecurrente
            ))

            idReserva = cursor.lastrowid

            cursor.execute('''
                UPDATE Turnos
                SET cupoRecurrenteActual =
                    cupoRecurrenteActual + 1
                WHERE idTurno = ?
            ''', (idTurno,))

            datos_notificaciones.append({
                'idReserva': idReserva,
                'fecha': turno[2],
                'hora': turno[3]
            })

        conexion.commit()

    for dato in datos_notificaciones:

        crear_notificacion_pendiente(
            dniPaciente=dniPac,
            idReserva=dato['idReserva'],
            fechaRecordatorio=dato['fecha'],
            asunto='Recordatorio de turno',
            mensaje=(
                f'Tienes un turno reservado para el día '
                f'{dato["fecha"]} a las {dato["hora"]}.'
            )
        )