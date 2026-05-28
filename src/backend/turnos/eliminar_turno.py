import sqlite3


def eliminar_turno(id_turno):
        # Conexión a la base de datos
        with sqlite3.connect('./src/backend/bdd.db') as conexion:
            cursor = conexion.cursor()
            # Borrar reservas
            cursor.execute(
                'DELETE FROM Reservas WHERE idTurno=?',
                (id_turno,)      
            )

            # Borrar kinesiologos
            cursor.execute(
                'DELETE FROM Turno_Kinesiologos WHERE idTurno=?',
                (id_turno,)
            )

            # Borrar turnos
            cursor.execute(
                'DELETE FROM Turnos WHERE idTurno = ?',
                (id_turno,)
            )
            conexion.commit()
        conexion.close()