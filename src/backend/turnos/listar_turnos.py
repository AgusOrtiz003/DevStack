import sqlite3
from backend.turnos.turno_pendiente import turno_pendiente
from datetime import datetime


def listar_los_turnos():

    with sqlite3.connect('./src/backend/bdd.db') as conexion:

        cursor = conexion.cursor()

        cursor.execute('''
            SELECT
                t.idTurno,
                t.fecha,
                t.hora,
                t.tratamiento,
                t.cupoActual,
                t.cupoMaximo,
                t.cupoRecurrenteActual,
                t.cupoRecurrenteMaximo,
                GROUP_CONCAT(
                    DISTINCT k.apellido || ' ' || k.nombre
                ) AS kinesiologos,
                GROUP_CONCAT(
                    tk.idKinesiologo
                ) AS idsKinesiologos
            FROM Turnos t
            INNER JOIN Turno_Kinesiologos tk
                ON t.idTurno = tk.idTurno
            INNER JOIN Kinesiologos k
                ON tk.idKinesiologo = k.idKinesiologo
            WHERE t.estado = 'Activo'
            GROUP BY t.idTurno
            ORDER BY fecha ASC
        ''')

        resultados = cursor.fetchall()

        turnos = []

        for resul in resultados:

            fecha_formateada = datetime.strptime(
                resul[1],
                '%Y-%m-%d'
            ).strftime(
                '%d/%m/%Y'
            )

            turno = {
                'idTurno': resul[0],
                'fecha': fecha_formateada,
                'hora': resul[2],
                'tratamiento': resul[3],

                # Cupos normales disponibles
                'cupoActual': resul[5] - resul[4],
                'cupoMaximo': resul[5],

                # Cupos recurrentes disponibles
                'cupoRecurrenteActual': resul[7] - resul[6],
                'cupoRecurrenteMaximo': resul[7],

                'kinesiologos': resul[8].replace(',', ', '),

                'idsKinesiologos': [
                    int(x)
                    for x in resul[9].split(',')
                ]
            }

            if turno_pendiente(resul[0]):
                turnos.append(turno)

        return turnos
    
    ###################################################################################################

def listar_reservas_turno(idTurno):

    with sqlite3.connect('./src/backend/bdd.db') as conexion:

        cursor = conexion.cursor()

        cursor.execute('''
            SELECT
                idReserva,
                dniPaciente,
                obraSocial,
                metodoPago,
                estado,
                fecha_creacion
            FROM Reservas
            WHERE idTurno = ?
            ORDER BY fecha_creacion ASC
        ''', (idTurno,))

        resultados = cursor.fetchall()

        reservas = []

        for r in resultados:

            fecha_formateada = datetime.strptime(
                r[5],
                '%Y-%m-%d %H:%M:%S'
            ).strftime(
                '%d/%m/%Y %H:%M'
            )

            reservas.append({
                'idReserva': r[0],
                'dniPaciente': r[1],
                'obraSocial': r[2],
                'metodoPago': r[3],
                'estado': r[4],
                'fechaCreacion': fecha_formateada,
            })

        return reservas