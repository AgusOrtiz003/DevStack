import sqlite3

def registrar_una_reserva(fecha,hora,id_paciente,tratamiento):
    conexion = sqlite3.connect('./src/backend/bdd.db')
    cursor = conexion.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reservas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha DATE NOT NULL,
            hora TIME NOT NULL,
            id_paciente INTEGER NOT NULL,
            tratamiento TEXT NOT NULL,
            estado TEXT NOT NULL DEFAULT "Pendiente",
            fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        INSERT INTO reservas(
            fecha,
            hora,
            id_paciente,
            tratamiento
        )
        VALUES(?, ?, ?, ?)
    """,(fecha,
         hora,
         id_paciente,
         tratamiento
        )
    )
    conexion.commit()
    conexion.close()