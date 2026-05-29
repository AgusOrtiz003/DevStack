import sqlite3


def cancelar_turno(id_turno):
        # Conexión a la base de datos
        with sqlite3.connect('./src/backend/bdd.db') as conexion:
            cursor = conexion.cursor()
            # Cancelar reservas
            cursor.execute('UPDATE Reservas SET estado = "Cancelado" WHERE idTurno=?',(id_turno,))

            # Borrar kinesiologos asignados a un turno
            cursor.execute(
                'DELETE FROM Turno_Kinesiologos WHERE idTurno=?',
                (id_turno,)
            )

            # Cancelar turnos
            cursor.execute('UPDATE Turnos SET estado = "Cancelado" WHERE idTurno=?',(id_turno,))
            conexion.commit()
        conexion.close()