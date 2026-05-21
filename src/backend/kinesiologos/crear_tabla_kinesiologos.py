import sqlite3

# =========================
# RUTA BASE
# =========================

DB_PATH = 'src/backend/bdd.db'

# =========================
# REGLAS DE NEGOCIO
# =========================

HORARIOS_VALIDOS = [
    "13:00",
    "14:00",
    "15:00",
    "16:00",
    "17:00",
    "18:00",
    "19:00",
    "20:00"
]

TRATAMIENTOS_VALIDOS = [
    "Tren superior",
    "Tren medio",
    "Tren inferior"
]

# =========================
# CREAR / RECREAR TABLA
# =========================

def crear_tabla_kinesiologos():

    try:

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE Kinesiologos (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                nombre TEXT NOT NULL,

                apellido TEXT NOT NULL,

                cuit TEXT NOT NULL UNIQUE,

                horaDesde TIME NOT NULL,

                horaHasta TIME NOT NULL,

                tratamiento TEXT NOT NULL,
                       
                fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

        conn.commit()
        conn.close()

        print("Tabla Kinesiologos creada correctamente")

    except Exception as e:

        print(f"Error creando tabla: {e}")

# =========================
# EJECUCIÓN
# =========================

if __name__ == '__main__':

    crear_tabla_kinesiologos()