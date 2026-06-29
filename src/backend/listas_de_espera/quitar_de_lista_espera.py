import sqlite3

def quitar_de_lista_espera(idTurno, dniPaciente):
    """Cambia el estado de la entrada en la lista de espera a 'Inactivo' para un turno y paciente específicos."""
    with sqlite3.connect('src/backend/bdd.db') as conexion:
        cursor = conexion.cursor()
        cursor.execute('''
            UPDATE ListaEspera
            SET estado = 'Inactivo'
            WHERE idTurno = ? AND dniPaciente = ?
        ''', (idTurno, dniPaciente))
        conexion.commit()

def buscar_en_lista_espera(idTurno):
    """Retorna el dni, método de pago y obra social del primer paciente activo en la lista de espera para un turno específico."""
    with sqlite3.connect('src/backend/bdd.db') as conexion:
        cursor = conexion.cursor()
        cursor.execute('''
            SELECT dniPaciente, obraSocial, metodoPago
            FROM ListaEspera
            WHERE idTurno = ? AND estado = 'Activo'
            ORDER BY id ASC
            LIMIT 1
        ''', (idTurno,))
        resultado = cursor.fetchone()
        if resultado:
            return resultado[0], resultado[1], resultado[2]  # Retorna dniPaciente, obraSocial, metodoPago
        else:
            return None