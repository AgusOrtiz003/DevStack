import sqlite3
from backend.registro import existe
from backend.exceptions.turno_lleno_exception import TurnoLlenoException

def registrar_reserva(fecha,hora,trat,obraSoc,metPag,dniPac):
    with sqlite3.connect('src/backend/bdd.db') as conexion:
        conexion.execute('PRAGMA foreign_keys = ON')
        cursor = conexion.cursor()

        # Verificar que exista el DNI
        if not existe(dniPac):
            raise ValueError('El DNI no está registrado')

        cursor.execute('SELECT idTurno, cupoActual, cupoMaximo FROM turnos WHERE fecha=? AND hora=? AND tratamiento=?',(fecha,hora,trat))
        turno = cursor.fetchone()
        if (turno is None): # Si el turno no existe, creo el turno y la reserva
            cursor.execute('INSERT INTO turnos (fecha,hora,tratamiento,cupoActual,cupoMaximo) VALUES(?,?,?,?,?)',(fecha,hora,trat,0,10))
            idTurno = cursor.lastrowid
        else:
            idTurno=turno[0]
            cupoActual = turno[1]
            cupoMaximo = turno[2]
            if cupoActual >= cupoMaximo:
                raise TurnoLlenoException('Turno lleno')
        cursor.execute('INSERT INTO reservas(dniPaciente, idTurno, obraSocial, metodoPago) VALUES(?,?,?,?)',(dniPac,idTurno,obraSoc,metPag))
        cursor.execute('UPDATE turnos SET cupoActual = cupoActual + 1 WHERE idTurno=?',(idTurno,))
        conexion.commit()
    conexion.close()