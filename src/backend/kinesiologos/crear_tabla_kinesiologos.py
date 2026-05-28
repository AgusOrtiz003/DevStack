import sqlite3

DB_PATH = 'src/backend/bdd.db'

def crear_tabla_kinesiologos():
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE Kinesiologos (

                idKinesiologo INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                apellido TEXT NOT NULL,
                CUIT TEXT NOT NULL UNIQUE,
                fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        conn.close()

def crear_tabla_turnos_kinesiologos():
    with sqlite3.connect(DB_PATH) as conexion:
        cursor = conexion.cursor()
        cursor.execute('''
                        CREATE TABLE Turno_Kinesiologos (
                        idTurno INTEGER,
                        idKinesiologo INTEGER,

                        PRIMARY KEY(idTurno, idKinesiologo),
                        
                        FOREIGN KEY(idTurno)
                            REFERENCES Turnos(idTurno),
                        FOREIGN KEY(idKinesiologo)
                            REFERENCES Kinesiologos(idKinesiologo)
                        )
                    ''')
        conexion.commit()