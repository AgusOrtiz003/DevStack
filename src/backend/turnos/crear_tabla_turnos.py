import sqlite3

def crear_tabla_turnos():
    with sqlite3.connect('src/backend/bdd.db') as conexion:
        cursor = conexion.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Turnos (
                idTurno INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha DATE NOT NULL,
                hora TIME NOT NULL,
                tratamiento TEXT NOT NULL,

                cupoActual INTEGER NOT NULL DEFAULT 0,
                cupoMaximo INTEGER NOT NULL,

                cupoRecurrenteActual INTEGER NOT NULL DEFAULT 0,
                cupoRecurrenteMaximo INTEGER NOT NULL DEFAULT 0,

                estado TEXT NOT NULL DEFAULT 'Activo',
                fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,

                UNIQUE(fecha, hora, tratamiento)
            )
        """)

        conexion.commit()