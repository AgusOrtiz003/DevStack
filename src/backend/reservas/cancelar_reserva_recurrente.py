import sqlite3
from backend.listas_de_espera.quitar_de_lista_espera import intentar_registrar_reserva_desde_lista_espera

def cancelar_reserva_recurrente(idReservaRecurrente):

    with sqlite3.connect('src/backend/bdd.db') as conexion:

        conexion.execute(
            'PRAGMA foreign_keys = ON'
        )

        cursor = conexion.cursor()

        cursor.execute('''
            SELECT
                idReserva,
                idTurno
            FROM Reservas
            WHERE idReservaRecurrente = ?
        ''', (idReservaRecurrente,))

        reservas = cursor.fetchall()

        if not reservas:
            raise ValueError(
                'La reserva recurrente no existe'
            )

        for idReserva, idTurno in reservas:

            cursor.execute('''
                UPDATE Turnos
                SET cupoRecurrenteActual =
                    CASE
                        WHEN cupoRecurrenteActual > 0
                        THEN cupoRecurrenteActual - 1
                        ELSE 0
                    END
                WHERE idTurno = ?
            ''', (idTurno,))

            cursor.execute('''
                DELETE FROM NotificacionesPendientes
                WHERE idReserva = ?
            ''', (idReserva,))

        cursor.execute('''
            DELETE FROM Reservas
            WHERE idReservaRecurrente = ?
        ''', (idReservaRecurrente,))

        cursor.execute('''
            DELETE FROM ReservasRecurrentes
            WHERE idReservaRecurrente = ?
        ''', (idReservaRecurrente,))

        conexion.commit()

        import sqlite3


def cancelar_reserva_recurrente_individual(idReserva):

    with sqlite3.connect('src/backend/bdd.db') as conexion:

        conexion.execute(
            'PRAGMA foreign_keys = ON'
        )

        cursor = conexion.cursor()

        cursor.execute('''
            SELECT
                idTurno,
                idReservaRecurrente
            FROM Reservas
            WHERE idReserva = ?
        ''', (idReserva,))

        reserva = cursor.fetchone()

        if reserva is None:
            raise ValueError(
                'La reserva no existe'
            )

        idTurno = reserva[0]
        idReservaRecurrente = reserva[1]

        cursor.execute('''
            UPDATE Turnos
            SET cupoRecurrenteActual =
                CASE
                    WHEN cupoRecurrenteActual > 0
                    THEN cupoRecurrenteActual - 1
                    ELSE 0
                END
            WHERE idTurno = ?
        ''', (idTurno,))

        cursor.execute('''
            DELETE FROM NotificacionesPendientes
            WHERE idReserva = ?
        ''', (idReserva,))

        cursor.execute('''
            DELETE FROM Reservas
            WHERE idReserva = ?
        ''', (idReserva,))

        # Actualizar cantidad de la reserva recurrente

        cursor.execute('''
            SELECT COUNT(*)
            FROM Reservas
            WHERE idReservaRecurrente = ?
        ''', (idReservaRecurrente,))

        cantidad = cursor.fetchone()[0]

        if cantidad == 0:

            cursor.execute('''
                DELETE FROM ReservasRecurrentes
                WHERE idReservaRecurrente = ?
            ''', (idReservaRecurrente,))

        else:

            cursor.execute('''
                UPDATE ReservasRecurrentes
                SET
                    cantidad = ?,
                    descuento = ?
                WHERE idReservaRecurrente = ?
            ''', (
                cantidad,
                cantidad >= 2,
                idReservaRecurrente
            ))

        conexion.commit()
    intentar_registrar_reserva_desde_lista_espera(idTurno)