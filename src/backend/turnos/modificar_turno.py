import sqlite3

DB_PATH = 'src/backend/bdd.db'

def modificar_turno(
    id_turno,
    fecha,
    hora,
    kinesiologos,
):
    with sqlite3.connect(DB_PATH) as conexion:
        
        conexion.execute('PRAGMA foreign_keys = ON')

        if not kinesiologos:
            raise ValueError('Seleccione al menos un kinesiólogo')
        
        cursor = conexion.cursor()
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
                    AND t.idTurno != ?
            """, (
                fecha,
                hora,
                id_kinesiologo,
                id_turno
            ))

            existe_kinesiologo = cursor.fetchone()

            if existe_kinesiologo:
                raise ValueError('Un kinesiólogo ya tiene un turno en ese horario')

        cursor.execute("""
            DELETE FROM Turno_Kinesiologos
            WHERE idTurno = ?
        """, (id_turno,))

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

        conexion.commit()