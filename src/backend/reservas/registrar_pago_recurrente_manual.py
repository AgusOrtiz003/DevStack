import sqlite3


def registrar_pago_recurrente_manual(
    idReservaRecurrente
):

    with sqlite3.connect('src/backend/bdd.db') as conexion:

        cursor = conexion.cursor()

        cursor.execute('''
            UPDATE Reservas
            SET estado = 'Pagado'
            WHERE idReservaRecurrente = ?
            AND estado = 'Pendiente'
        ''', (idReservaRecurrente,))

        conexion.commit()