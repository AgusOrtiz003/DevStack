import sqlite3

DB_PATH = 'src/backend/bdd.db'

def crear_turno(
    fecha,
    hora,
    tratamiento,
    cupo_maximo,
    kinesiologos
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
                SELECT 1
                FROM Turnos t
                INNER JOIN Turno_Kinesiologos tk
                    ON t.idTurno = tk.idTurno
                WHERE
                    t.fecha = ?
                    AND t.hora = ?
                    AND tk.idKinesiologo = ?
            """, (
                fecha,
                hora,
                id_kinesiologo
            ))

            existe_kinesiologo = cursor.fetchone()

            if existe_kinesiologo:
                raise ValueError('Un kinesiólogo ya tiene un turno en ese horario')

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
        conexion.commit()
    conexion.close()