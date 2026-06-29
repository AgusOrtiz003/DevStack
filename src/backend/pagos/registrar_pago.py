import sqlite3

def registrar_pago(idReserva, monto, tokenPago):
    with sqlite3.connect('src/backend/bdd.db') as conexion:
        cursor = conexion.cursor()
        cursor.execute('''
            INSERT INTO Pagos (idReserva, monto, metodoPago, estado, fechaPago, tokenPago)
            VALUES (?, ?, 'MercadoPago', 'Pagado', CURRENT_TIMESTAMP, ?)
        ''', (idReserva, monto, tokenPago))
        conexion.commit()
        
        cursor.execute('''
            UPDATE Reservas SET estado = "Pagado" WHERE idReserva = ?
        ''', (idReserva,))
        conexion.commit()