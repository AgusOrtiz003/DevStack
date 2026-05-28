import sqlite3
from backend.turnos.turno_pendiente import turno_pendiente
from datetime import datetime

def listar_los_turnos():
    with sqlite3.connect('./src/backend/bdd.db') as conexion:
        cursor = conexion.cursor()
        cursor.execute('''SELECT t.idTurno, t.fecha , t.hora, t.tratamiento, t.cupoActual, t.cupoMaximo,
                        GROUP_CONCAT(DISTINCT k.apellido || ' ' || k.nombre) AS kinesiologos,
                        GROUP_CONCAT(tk.idKinesiologo) AS idsKinesiologos 
                        FROM turnos t INNER JOIN Turno_Kinesiologos tk ON t.idTurno = tk.idTurno
                        INNER JOIN Kinesiologos k ON tk.idKinesiologo = k.idKinesiologo 
                        GROUP BY t.idTurno ORDER BY fecha ASC
        ''')
        resultados = cursor.fetchall()
        turnos = []
        for resul in resultados:
            fecha_formateada = datetime.strptime(resul[1],'%Y-%m-%d').strftime('%d/%m/%Y')
            turno = {
                    'idTurno': resul[0],
                    'fecha': fecha_formateada,
                    'hora': resul[2],
                    'tratamiento': resul[3],
                    'cupoActual': resul[5]-resul[4],
                    'cupoMaximo': resul[5],
                    'kinesiologos': resul[6].replace(',', ', '),
                    'idsKinesiologos': [int(x) for x in resul[7].split(',')]
                }
            if (turno_pendiente(resul[0])):
                turnos.append(turno)
        return turnos
    conexion.close()
###################################################################################################
def listar_reservas_turno(idTurno):
    with sqlite3.connect('./src/backend/bdd.db') as conexion:
        cursor = conexion.cursor()
        cursor.execute('''SELECT idReserva, dniPaciente, obraSocial, metodoPago, estado, fecha_creacion 
                       FROM reservas WHERE idTurno=? ORDER BY fecha_creacion ASC
        ''',(idTurno,))
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