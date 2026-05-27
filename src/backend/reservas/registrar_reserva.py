import sqlite3

from backend.registro import existe
from backend.exceptions.turno_lleno_exception import TurnoLlenoException


def registrar_reserva(idTurno, obraSoc, metPag, dniPac):

    with sqlite3.connect('src/backend/bdd.db') as conexion:
        conexion.execute('PRAGMA foreign_keys = ON')
        
        cursor = conexion.cursor()
        
        if not existe(dniPac):
            raise ValueError('El DNI no está registrado')
        
        cursor.execute('''
            SELECT
                cupoActual,
                cupoMaximo
            FROM Turnos
            WHERE idTurno = ?
        ''', (idTurno,))

        turno = cursor.fetchone()

        cupoActual = turno[0]
        cupoMaximo = turno[1]

        if cupoActual >= cupoMaximo:
            raise TurnoLlenoException('Turno lleno')

        cursor.execute('''
            INSERT INTO Reservas (
                dniPaciente,
                idTurno,
                obraSocial,
                metodoPago
            )
            VALUES (?, ?, ?, ?)
        ''', (
            dniPac,
            idTurno,
            obraSoc,
            metPag
        ))

        cursor.execute('''
            UPDATE Turnos
            SET cupoActual = cupoActual + 1
            WHERE idTurno = ?
        ''', (idTurno,))

        conexion.commit()