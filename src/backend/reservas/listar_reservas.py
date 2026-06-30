import sqlite3
from datetime import datetime

def listar_reservas(dniPac):
    with sqlite3.connect('src/backend/bdd.db') as conexion:
        cursor = conexion.cursor()
        cursor.execute('''
            SELECT r.idReserva, r.obraSocial, r.metodoPago, r.estado, 
                   t.fecha, t.hora, t.tratamiento, r.idReservaRecurrente 
            FROM reservas r 
            INNER JOIN turnos t ON r.idTurno = t.idTurno 
            WHERE dniPaciente = ? 
            ORDER BY t.fecha ASC, t.hora ASC
        ''', (dniPac,))
        resultados = cursor.fetchall()
        return [
            {
                'idReserva':   res[0],
                'obraSocial':  res[1],
                'metodoPago':  res[2],
                'estado':      res[3],
                'fecha':       datetime.strptime(res[4], '%Y-%m-%d').strftime('%d/%m/%Y'),
                'hora':        res[5],
                'tratamiento': res[6],
                'idReservaRecurrente':  res[7],
            }
            for res in resultados
        ]

def listar_reservas_recurrentes(dniPac):
    with sqlite3.connect('src/backend/bdd.db') as conexion:
        cursor = conexion.cursor()
        cursor.execute('''
            SELECT 
                rr.idReservaRecurrente,
                MIN(t.fecha)        as fecha_desde,
                MAX(t.fecha)        as fecha_hasta,
                COUNT(*)            as cantidad_turnos,
                MAX(t.tratamiento)  as tratamiento,
                MAX(t.hora)         as hora,
                MAX(r.obraSocial)   as obraSocial,
                MAX(r.metodoPago)   as metodoPago
            FROM Reservas r
            INNER JOIN Turnos t ON r.idTurno = t.idTurno
            INNER JOIN ReservasRecurrentes rr ON r.idReservaRecurrente = rr.idReservaRecurrente
            WHERE r.dniPaciente = ?
            GROUP BY rr.idReservaRecurrente
        ''', (dniPac,))
        return [
            {
                'idReservaRecurrente': res[0],
                'fecha_desde':         datetime.strptime(res[1], '%Y-%m-%d').strftime('%d/%m/%Y'),
                'fecha_hasta':         datetime.strptime(res[2], '%Y-%m-%d').strftime('%d/%m/%Y'),
                'cantidad_turnos':     res[3],
                'tratamiento':         res[4],
                'hora':                res[5],
                'obraSocial':          res[6],
                'metodoPago':          res[7],
            }
            for res in cursor.fetchall()
        ]
    
def listar_reservas_de_recurrente(idReservaRecurrente):
    with sqlite3.connect('src/backend/bdd.db') as conexion:
        cursor = conexion.cursor()
        cursor.execute('''
            SELECT r.idReserva, r.obraSocial, r.estado,
                   t.fecha, t.hora, t.tratamiento
            FROM Reservas r
            INNER JOIN Turnos t ON r.idTurno = t.idTurno
            WHERE r.idReservaRecurrente = ?
            ORDER BY t.fecha ASC
        ''', (idReservaRecurrente,))
        return [
            {
                'idReserva':   res[0],
                'obraSocial':  res[1],
                'estado':      res[2],
                'fecha':       datetime.strptime(res[3], '%Y-%m-%d').strftime('%d/%m/%Y'),
                'hora':        res[4],
                'tratamiento': res[5],
            }
            for res in cursor.fetchall()
        ]