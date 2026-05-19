import sqlite3

def crearTablaReserva():
    conexion = sqlite3.connect('src/backend/bdd.db')
    cursor = conexion.cursor()

    # Crear tabla reservas en la BDD
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reservas (
            idReserva INTEGER PRIMARY KEY AUTOINCREMENT,
            dniPaciente INTEGER NOT NULL,
            idTurno INTEGER NOT NULL,
            obraSocial TEXT,
            metodoPago TEXT,
            estado TEXT NOT NULL DEFAULT 'Pendiente',
            fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (idTurno) REFERENCES turnos(idTurno),
            UNIQUE(dniPaciente, idTurno)
        )
    """)

    conexion.commit()
    conexion.close()
###################################################################################################
def registrarReserva(fecha,hora,trat,obraSoc,metPag,dniPac):
    with sqlite3.connect('src/backend/bdd.db',timeout=10) as conexion:
        conexion.execute('PRAGMA foreign_keys = ON')
        cursor = conexion.cursor()

        cursor.execute('SELECT idTurno, cupoActual, cupoMaximo FROM turnos WHERE fecha=? AND hora=? AND tratamiento=?',(fecha,hora,trat))
        turno = cursor.fetchone()
        if (turno is None): # Si el turno no existe, creo el turno y la reserva
            cursor.execute('INSERT INTO turnos (fecha,hora,tratamiento,cupoActual,cupoMaximo) VALUES(?,?,?,?,?)',(fecha,hora,trat,0,10))
            idTurno = cursor.lastrowid
        else:
            idTurno=turno[0]
            cupoActual = turno[1]
            cupoMaximo = turno[2]
            if cupoActual >= cupoMaximo: # Agregarlo a la lista de espera, prioridad 0 si no es recurrente
                print('Turno lleno')
                conexion.close()
                return
        cursor.execute('INSERT INTO reservas(dniPaciente, idTurno, obraSocial, metodoPago) VALUES(?,?,?,?)',(dniPac,idTurno,obraSoc,metPag))
        cursor.execute('UPDATE turnos SET cupoActual = cupoActual + 1 WHERE idTurno=?',(idTurno,))
        conexion.commit()
###################################################################################################
def listarReservas(dniPac):
    with sqlite3.connect('src/backend/bdd.db') as conexion:
        cursor = conexion.cursor()
        cursor.execute('SELECT r.idReserva, r.obraSocial, r.metodoPago, r.estado, t.fecha, t.hora, t.tratamiento FROM reservas r INNER JOIN turnos t ON r.idTurno = t.idTurno WHERE dniPaciente=? AND estado="Pendiente"',(dniPac,))
        resultados = cursor.fetchall()
        reservas = []
        for resul in resultados:
            reserva = {
                    'idReserva': resul[0],
                    'obraSocial': resul[1],
                    'metodoPago': resul[2],
                    'estado': resul[3],
                    'fecha': resul[4],
                    'hora': resul[5],
                    'tratamiento': resul[6]
                }
            reservas.append(reserva)
        return reservas
    conexion.close()
###################################################################################################
def cancelarReserva(idReserva):
    with sqlite3.connect('src/backend/bdd.db') as conexion:
        cursor = conexion.cursor()
        cursor.execute('SELECT idTurno FROM reservas WHERE idReserva=?',(idReserva,))
        idTurno = cursor.fetchone()
        cursor.execute('UPDATE turnos SET cupoActual = cupoActual - 1 WHERE idTurno=?',(idTurno))
        cursor.execute('DELETE FROM reservas WHERE idReserva=?',(idReserva,))
        conexion.commit()
    conexion.close()