import sqlite3
from backend.turnos.turno_pendiente import turno_pendiente
from datetime import datetime

def listar_los_turnos():
    with sqlite3.connect('./src/backend/bdd.db') as conexion:
        cursor = conexion.cursor()
        cursor.execute('SELECT idTurno, fecha , hora, tratamiento, cupoActual, cupoMaximo FROM turnos WHERE cupoActual > 0 ORDER BY fecha ASC')
        resultados = cursor.fetchall()
        turnos = []
        for resul in resultados:
            fecha_formateada = datetime.strptime(resul[1],'%Y-%m-%d').strftime('%d/%m/%Y')
            turno = {
                    'idTurno': resul[0],
                    'fecha': fecha_formateada,
                    'hora': resul[2],
                    'tratamiento': resul[3],
                    'cupoActual': resul[4],
                    'cupoMaximo': resul[5],
                }
            if (turno_pendiente(resul[0])):
                turnos.append(turno)
        return turnos
    conexion.close()
###################################################################################################
def listar_reservas_turno(idTurno):
    with sqlite3.connect('./src/backend/bdd.db') as conexion:
        cursor = conexion.cursor()
        cursor.execute('SELECT idReserva, dniPaciente, obraSocial, metodoPago, estado, fecha_creacion FROM reservas WHERE idTurno=? ORDER BY dniPaciente ASC',(idTurno,))
        reservas=[]
        resultados = cursor.fetchall()

        for r in resultados:
            fecha_formateada = datetime.strptime(r[5],'%Y-%m-%d %H:%M:%S').strftime('%d/%m/%Y %H:%M')
            reservas.append({
                'idReserva': r[0],
                'dniPaciente': r[1],
                'obraSocial': r[2],
                'metodoPago': r[3],
                'estado': r[4],
                'fechaCreacion': fecha_formateada,
            })

        return reservas
    conexion.close()