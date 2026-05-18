import sqlite3

def crearTablaTurno():
    conexion = sqlite3.connect('src/backend/bdd.db')
    cursor = conexion.cursor()

    # Crear tabla turnos en la BDD
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS turnos (
            idTurno INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha DATE NOT NULL,
            hora TIME NOT NULL,
            tratamiento TEXT NOT NULL,
            cupoActual INTEGER NOT NULL,
            cupoMaximo INTEGER NOT NULL,
            fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(fecha, hora, tratamiento)
        )
    """)

    conexion.commit()
    conexion.close()
###################################################################################################