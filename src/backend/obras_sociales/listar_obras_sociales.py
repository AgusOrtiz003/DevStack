import sqlite3

def listar_obras_sociales():
    with sqlite3.connect() as conexion:
        cursor = conexion.cursor()
        cursor.execute('''
                SELECT idObra, nombre FROM Obras
        ''')
        resultados = cursor.fetchall()
        obras = []
        for o in resultados:
            obras.append({
                'idObra': o[0],
                'nombre': o[1],
            })
        return obras
    conexion.close()