import sqlite3
def usuario_tiene_reservas(dni):
    """Revisa si un dni tiene reservas asociadas"""
    with sqlite3.connect('src/backend/bdd.db') as conexion:
        cursor = conexion.cursor()
        cursor.execute('SELECT COUNT(*) FROM reservas WHERE dniPaciente=?',(dni,))
        resultado = cursor.fetchone()
        conexion.close()
        return resultado[0] > 0