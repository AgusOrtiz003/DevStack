import sqlite3
def confirmar_reserva(idReserva):
    with sqlite3.connect('./src/backend/bdd.db') as conexion:
        cursor = conexion.cursor()

        cursor.execute(
            'UPDATE reservas SET estado="Confirmado" WHERE idReserva=?',
            (idReserva,)
        )

        conexion.commit()
    conexion.close()