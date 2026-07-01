import sqlite3
from backend.listas_de_espera.quitar_de_lista_espera import quitar_de_lista_espera,buscar_en_lista_espera
from backend.reservas.registrar_reserva import registrar_reserva
from src.backend.turnos.verificar_cupo_disponible import verificar_cupo_disponible
from backend.reservas.registrar_reserva_recurrente import registrar_reservas_recurrentes
def cancelar_reserva(idReserva):
    with sqlite3.connect('src/backend/bdd.db') as conexion:
        cursor = conexion.cursor()
        cursor.execute('SELECT idTurno FROM reservas WHERE idReserva=?',(idReserva,))
        resultado = cursor.fetchone()

        if resultado is None:
            return

        idTurno = resultado[0]
        cursor.execute('UPDATE reservas SET estado = "Cancelado" WHERE idReserva=?',(idReserva,))
        cursor.execute('UPDATE turnos SET cupoActual = MAX(cupoActual - 1, 0) WHERE idTurno=?',(idTurno,))
        conexion.commit()
    conexion.close()
    dniPaciente = buscar_en_lista_espera(idTurno)
    if dniPaciente:
        if dniPaciente[3]:
            if(reserva_recurrente_cumple(dniPaciente[3])):
                registrar_reservas_recurrentes(dniPaciente[0], dniPaciente[1], dniPaciente[2])
        else:
            registrar_reserva(idTurno, dniPaciente[1], dniPaciente[2], dniPaciente[0])
            quitar_de_lista_espera(idTurno, dniPaciente[0])
        
def reserva_recurrente_cumple(idGrupo):
    with sqlite3.connect('src/backend/bdd.db') as conexion:
        cursor = conexion.cursor()
        cursor.execute('''
            SELECT idTurno
            FROM ListaEspera
            WHERE idGrupo = ?
        ''', (idGrupo,))
        resultado = cursor.fetchall()
        todosDisponibles = True
        for idGrupo in resultado:
            todosDisponibles=verificar_cupo_disponible(idGrupo)
        return todosDisponibles