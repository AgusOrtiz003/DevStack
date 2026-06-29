import sqlite3


def obtener_pacientes():
    conn = sqlite3.connect('src/backend/bdd.db')
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            dni,
            nombre,
            apellido,
            email,
            fechaNac,
            rol
        FROM Usuarios
        WHERE rol = 'Paciente'
        OR  rol = 'Baneado'
        ORDER BY apellido, nombre
    """)

    pacientes = cursor.fetchall()

    conn.close()

    return pacientes