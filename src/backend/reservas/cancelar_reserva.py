import sqlite3

def cancelar_reserva(idReserva):
    with sqlite3.connect('src/backend/bdd.db') as conexion:
        cursor = conexion.cursor()
        cursor.execute('SELECT idTurno FROM reservas WHERE idReserva=?',(idReserva,))
        resultado = cursor.fetchone()

        if resultado is None:
            return

        idTurno = resultado[0]
        cursor.execute('UPDATE turnos SET cupoActual = MAX(cupoActual - 1, 0) WHERE idTurno=?',(idTurno,))
        cursor.execute('UPDATE reservas SET estado = "Cancelado" WHERE idReserva=?',(idReserva,))
        conexion.commit()
    conexion.close()