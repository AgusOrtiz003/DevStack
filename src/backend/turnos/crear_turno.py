import sqlite3

DB_PATH = 'src/backend/bdd.db'

def crear_turno(
    fecha,
    hora,
    tratamiento,
    cupo_maximo,
    kinesiologos,
    obras,
):

    with sqlite3.connect(DB_PATH) as conexion:
        cursor = conexion.cursor()
        cursor.execute("""
            INSERT INTO Turnos (
                fecha,
                hora,
                tratamiento,
                cupoActual,
                cupoMaximo
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            fecha,
            hora,
            tratamiento,
            0,
            cupo_maximo,
        ))
        id_turno = cursor.lastrowid
        for id_kinesiologo in kinesiologos:
            cursor.execute("""
                INSERT INTO Turno_Kinesiologos (
                    idTurno,
                    idKinesiologo
                )
                VALUES (?, ?)
            """, (
                id_turno,
                id_kinesiologo
            ))
        for obra in obras:
            cursor.execute("""
                INSERT INTO Turno_ObrasSociales (
                    idTurno,
                    obraSocial
                )
                VALUES (?, ?)
            """, (
                id_turno,
                obra
            ))
        conexion.commit()
    conexion.close()