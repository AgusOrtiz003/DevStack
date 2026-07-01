import sqlite3

def agregar_a_lista_espera(idTurno, dniPaciente, obraSocial, metodoPago,idGrupo=None):
    with sqlite3.connect('src/backend/bdd.db') as conexion:
        cursor = conexion.cursor()
        cursor.execute('''
            INSERT INTO ListaEspera (idTurno, dniPaciente, obraSocial, metodoPago, estado,idGrupo)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (idTurno, dniPaciente, obraSocial, metodoPago, 'Activo', idGrupo))
        conexion.commit()

def crear_grupo():
    with sqlite3.connect('src/backend/bdd.db') as conexion:
        cursor = conexion.cursor()
        cursor.execute('''
            INSERT INTO ListaEsperaRecurrente ()
            DEFAULT VALUES
        ''', )
        conexion.commit()
        return cursor.lastrowid