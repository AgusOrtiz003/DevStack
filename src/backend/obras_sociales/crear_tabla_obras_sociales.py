import sqlite3

def crear_tabla_obras_sociales():
    with sqlite3.connect('src/backend/bdd.db') as conexion:
        cursor = conexion.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Obras (
                idObra INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL
            )
        ''')
        conexion.commit()
    conexion.close()

def crear_tabla_turno_obra():
    with sqlite3.connect('src/backend/bdd.db') as conexion:
        cursor = conexion.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Turno_ObrasSociales (
                idTurno INTEGER,
                obraSocial TEXT NOT NULL,

                PRIMARY KEY(idTurno, obraSocial),
                FOREIGN KEY(idTurno)
                    REFERENCES Turnos(idTurno)
            )        
        ''')
    conexion.close()

crear_tabla_obras_sociales()
crear_tabla_turno_obra()