import sqlite3

def crear_tabla_reserva():
    with sqlite3.connect('src/backend/bdd.db') as conexion:
        cursor = conexion.cursor()

        # Crear tabla reservas en la BDD
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Reservas (
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