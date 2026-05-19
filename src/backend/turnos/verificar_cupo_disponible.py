import sqlite3

##ESTO SIRVE PARA VER SI EL TURNO ESTÁ DISPONIBLE O SI ESTÁ COMPLETAMENTE OCUPADO
DB_PATH = 'src/backend/bdd.db'


def verificar_cupo_disponible(id_turno):
    conexion = sqlite3.connect(DB_PATH)

    cursor = conexion.cursor()

    cursor.execute("""
        SELECT cupoActual, cupoMaximo
        FROM turnos
        WHERE id = ?
    """, (id_turno,))

    resultado = cursor.fetchone()

    conexion.close()

    # Si no existe el turno
    if resultado is None:
        return False

    cupo_actual, cupo_maximo = resultado

    return cupo_actual < cupo_maximo