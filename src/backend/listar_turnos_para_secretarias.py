import sqlite3

def listar_los_turnos():
    conexion = sqlite3.connect('./src/backend/bdd.db')
    cursor = conexion.cursor()
    cursor.execute('SELECT id, fecha, hora, tratamiento ,cupoActual, cupoMaximo FROM turnos')
    resultados = cursor.fetchall()
    conexion.close()
    turnos = []

    for fila in resultados:
        turnos.append({
            'id': fila[0],
            'fecha': fila[1],
            'hora': fila[2],
            'tratamiento': fila[3],
            'cupoActual': fila[4],
            'cupoMaximo': fila[5]
        })
    conexion.close()
    return turnos