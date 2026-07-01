import sqlite3
from backend.listas_de_espera.quitar_de_lista_espera import intentar_registrar_reserva_desde_lista_espera
def cancelar_reserva(idReserva):
    with sqlite3.connect('src/backend/bdd.db') as conexion:
        cursor = conexion.cursor()
        cursor.execute('SELECT idTurno FROM reservas WHERE idReserva=?',(idReserva,))
        resultado = cursor.fetchone()

        if resultado is None:
            return

        idTurno = resultado[0]
        cursor.execute('UPDATE reservas SET estado = "Cancelado" WHERE idReserva=?',(idReserva,))
        cursor.execute('UPDATE turnos SET cupoActual = MAX(cupoActual - 1, 0) WHERE idTurno=?',(idTurno,))
        conexion.commit()
    conexion.close()
    intentar_registrar_reserva_desde_lista_espera(idTurno)