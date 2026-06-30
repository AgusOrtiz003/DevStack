import sqlite3
from datetime import datetime


def listar_reservas_recurrentes_secretaria():

    with sqlite3.connect('src/backend/bdd.db') as conexion:

        cursor = conexion.cursor()

        cursor.execute('''
            SELECT
                r.idReservaRecurrente,
                r.dniPaciente,
                u.nombre,
                u.apellido,
                r.metodoPago,
                COUNT(*) as cantidad,
                MIN(t.fecha) as fecha_desde,
                MAX(t.fecha) as fecha_hasta
            FROM Reservas r
            INNER JOIN Usuarios u
                ON r.dniPaciente = u.dni
            INNER JOIN Turnos t
                ON r.idTurno = t.idTurno
            WHERE r.idReservaRecurrente <> 0
            AND r.estado = 'Pendiente'
            AND (
                r.metodoPago = 'Efectivo'
                OR r.metodoPago = 'Transferencia'
            )
            GROUP BY
                r.idReservaRecurrente,
                r.dniPaciente,
                u.nombre,
                u.apellido,
                r.metodoPago
            ORDER BY fecha_desde
        ''')

        resultados = []

        for fila in cursor.fetchall():

            resultados.append({
                'idReservaRecurrente': fila[0],
                'dni': fila[1],
                'nombre': fila[2],
                'apellido': fila[3],
                'metodoPago': fila[4],
                'cantidadTurnos': fila[5],
                'fechaDesde': datetime.strptime(
                    fila[6],
                    '%Y-%m-%d'
                ).strftime('%d/%m/%Y'),
                'fechaHasta': datetime.strptime(
                    fila[7],
                    '%Y-%m-%d'
                ).strftime('%d/%m/%Y'),
            })

        return resultados
    
    
def obtener_detalle_recurrente(idReservaRecurrente):

    with sqlite3.connect('src/backend/bdd.db') as conexion:

        cursor = conexion.cursor()

        cursor.execute('''
            SELECT
                r.idReserva,
                t.fecha,
                t.hora,
                t.tratamiento
            FROM Reservas r
            INNER JOIN Turnos t
                ON r.idTurno = t.idTurno
            WHERE r.idReservaRecurrente = ?
            ORDER BY t.fecha
        ''', (idReservaRecurrente,))

        return [
            {
                'idReserva': fila[0],
                'fecha': fila[1],
                'hora': fila[2],
                'tratamiento': fila[3]
            }
            for fila in cursor.fetchall()
        ]