import sqlite3

def crear_tabla_pagos():
    with sqlite3.connect('src/backend/bdd.db') as conexion:
        cursor = conexion.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Pagos (
                idPago INTEGER PRIMARY KEY AUTOINCREMENT,
                idReserva INTEGER NOT NULL,
                monto REAL NOT NULL,
                metodoPago TEXT NOT NULL,
                estado TEXT NOT NULL,
                fechaPago DATETIME,
                tokenPago TEXT,

                FOREIGN KEY (idReserva)
                    REFERENCES Reservas(idReserva)
            )
        ''')
        conexion.commit()