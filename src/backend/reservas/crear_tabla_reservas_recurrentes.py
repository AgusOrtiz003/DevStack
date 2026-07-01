import sqlite3

DB_PATH = 'src/backend/bdd.db'


def crear_tabla_reservas_recurrentes():

    with sqlite3.connect(DB_PATH) as conexion:

        cursor = conexion.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ReservasRecurrentes (
                idReservaRecurrente INTEGER PRIMARY KEY AUTOINCREMENT,
                cantidad INTEGER NOT NULL,
                descuento BOOLEAN NOT NULL DEFAULT 0,
                pago BOOLEAN NOT NULL DEFAULT 0
            )
        """)

        conexion.commit()

    print(
        'Tabla ReservasRecurrentes creada correctamente'
    )


if __name__ == '__main__':
    crear_tabla_reservas_recurrentes()