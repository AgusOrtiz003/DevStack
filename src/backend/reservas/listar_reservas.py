import sqlite3
from datetime import datetime

def listar_reservas(dniPac):
    with sqlite3.connect('src/backend/bdd.db') as conexion:
        cursor = conexion.cursor()
        cursor.execute('SELECT r.idReserva, r.obraSocial, r.metodoPago, r.estado, t.fecha, t.hora, t.tratamiento FROM reservas r INNER JOIN turnos t ON r.idTurno = t.idTurno WHERE dniPaciente=? AND estado="Pendiente" ORDER BY 5 ASC',(dniPac,))
        resultados = cursor.fetchall()
        reservas = []
        for resul in resultados:
            fecha_formateada = datetime.strptime(resul[4],'%Y-%m-%d').strftime('%d/%m/%Y')
            reserva = {
                    'idReserva': resul[0],
                    'obraSocial': resul[1],
                    'metodoPago': resul[2],
                    'estado': resul[3],
                    'fecha': fecha_formateada,
                    'hora': resul[5],
                    'tratamiento': resul[6]
                }
            reservas.append(reserva)
        return reservas
    conexion.close()