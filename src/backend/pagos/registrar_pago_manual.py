# backend/reservas/registrar_pago_manual.py

import sqlite3

def registrar_pago_manual(idReserva):

    with sqlite3.connect('src/backend/bdd.db') as conexion:

        cursor = conexion.cursor()

        cursor.execute('''
            UPDATE Reservas
            SET estado = 'Pagado'
            WHERE idReserva = ?
        ''', (idReserva,))

        conexion.commit()