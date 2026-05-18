import sqlite3

def registrar_un_turno(fecha,hora,tratamiento,cupo_maximo):
    conexion = sqlite3.connect('./src/backend/bdd.db')
    cursor = conexion.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS turnos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha DATE NOT NULL,
            hora TIME NOT NULL,
            tratamiento TEXT NOT NULL,
            cupoActual INTEGER NOT NULL,
            cupoMaximo INTEGER NOT NULL,
            fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        INSERT INTO turnos (
            fecha,
            hora,
            tratamiento,
            cupoActual,
            cupoMaximo
        )
        VALUES (?, ?, ?, ?, ?)
    """,(fecha,
         hora,
         tratamiento,
         cupo_maximo,
         cupo_maximo
        )
    )
    conexion.commit()
    conexion.close()