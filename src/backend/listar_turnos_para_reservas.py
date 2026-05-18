import sqlite3

def listar_los_turnos_para_reservas():
    conexion = sqlite3.connect('./src/backend/bdd.db')
    cursor = conexion.cursor()
    cursor.execute('SELECT fecha, hora, tratamiento ,cupoActual FROM turnos')
    resultados = cursor.fetchall()
    conexion.close()
    turnos = []

    for fila in resultados:
        turnos.append({
            'fecha': fila[0],
            'hora': fila[1],
            'tratamiento': fila[2],
            'cupoActual': fila[3],
        })
    conexion.close()
    return turnos