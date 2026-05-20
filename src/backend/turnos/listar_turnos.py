import sqlite3
from backend.turnos.turno_pendiente import turno_pendiente

def listar_los_turnos():
    with sqlite3.connect('./src/backend/bdd.db') as conexion:
        cursor = conexion.cursor()
        cursor.execute('SELECT idTurno, fecha , hora, tratamiento, cupoActual, cupoMaximo FROM turnos WHERE cupoActual < cupoMaximo')
        resultados = cursor.fetchall()
        turnos = []
        for resul in resultados:
            turno = {
                    'idTurno': resul[0],
                    'fecha': resul[1],
                    'hora': resul[2],
                    'tratamiento': resul[3],
                    'cupoActual': resul[4],
                    'cupoMaximo': resul[5],
                }
            if (turno_pendiente(resul[0],conexion) & resul[4] > 0):
                turnos.append(turno)
        return turnos
    conexion.close()
###################################################################################################