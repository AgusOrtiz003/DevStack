import sqlite3

def crear_tablas_lista_espera():
    with sqlite3.connect('src/backend/bdd.db') as conexion:
        cursor = conexion.cursor()

        # Crear tabla reservas en la BDD
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS ListaEspera (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            idTurno INTEGER NOT NULL,
            dniPaciente INTEGER NOT NULL,
            obraSocial TEXT NOT NULL,
            metodoPago TEXT NOT NULL,
            estado TEXT NOT NULL,
            FOREIGN KEY (idTurno) REFERENCES turnos(idTurno),
            FOREIGN KEY (dniPaciente) REFERENCES pacientes(dniPaciente),
            UNIQUE(dniPaciente, idTurno)
    )
""")

        conexion.commit()
    conexion.close()
crear_tablas_lista_espera()