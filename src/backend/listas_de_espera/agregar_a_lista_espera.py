import sqlite3

def agregar_a_lista_espera(idTurno, dniPaciente, obraSocial, metodoPago):
    with sqlite3.connect('src/backend/bdd.db') as conexion:
        cursor = conexion.cursor()
        cursor.execute('''
            INSERT INTO ListaEspera (idTurno, dniPaciente, obraSocial, metodoPago, estado)
            VALUES (?, ?, ?, ?, ?)
        ''', (idTurno, dniPaciente, obraSocial, metodoPago, 'Activo'))
        conexion.commit()