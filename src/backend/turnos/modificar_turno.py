import sqlite3

DB_PATH = 'src/backend/bdd.db'


def obtener_turno_por_id(id_turno):
    conexion = sqlite3.connect(DB_PATH)
    conexion.row_factory = sqlite3.Row

    cursor = conexion.cursor()

    cursor.execute("""
        SELECT *
        FROM turnos
        WHERE id = ?
    """, (id_turno,))

    turno = cursor.fetchone()

    conexion.close()

    return dict(turno) if turno else None


def modificar_turno(
    id_turno,
    fecha,
    hora,
    kinesiologo,
    tratamiento,
    cupo_actual,
    cupo_maximo
):
    conexion = sqlite3.connect(DB_PATH)

    cursor = conexion.cursor()

    cursor.execute("""
        UPDATE turnos
        SET
            fecha = ?,
            hora = ?,
            kinesiologo = ?,
            tratamiento = ?,
            cupoActual = ?,
            cupoMaximo = ?
        WHERE id = ?
    """, (
        fecha,
        hora,
        kinesiologo,
        tratamiento,
        cupo_actual,
        cupo_maximo,
        id_turno
    ))

    conexion.commit()
    conexion.close()