import sqlite3
from backend.turnos.verificar_cupo_disponible import verificar_cupo_disponible
<<<<<<< HEAD
from backend.reservas.registrar_reserva import registrar_reserva
from backend.reservas.registrar_reserva_recurrente import registrar_reservas_recurrentes
=======
>>>>>>> 00da10f64928c896dec7cef92a767c5cf6f83b97

def quitar_de_lista_espera(dniPaciente,idTurno,idgrupo=None):
    """Cambia el estado de la entrada en la lista de espera a 'Inactivo' para un turno y paciente específicos."""
    with sqlite3.connect('src/backend/bdd.db') as conexion:
        cursor = conexion.cursor()
        if (idgrupo is None):
            cursor.execute('''
                UPDATE ListaEspera
                SET estado = 'Inactivo'
                WHERE idTurno = ? AND dniPaciente = ?
            ''', (idTurno, dniPaciente))
        else:
            cursor.execute('''
                UPDATE ListaEspera
                SET estado = 'Inactivo'
                WHERE idTurno = ? AND dniPaciente = ? AND idGrupo = ?
            ''', (idTurno, dniPaciente, idgrupo))
        conexion.commit()

def buscar_en_lista_espera(idTurno):
    """Retorna una lista con el dni, método de pago, obra social y grupo de todos los pacientes activos en la lista de espera para un turno específico."""
    with sqlite3.connect('src/backend/bdd.db') as conexion:
        cursor = conexion.cursor()
        cursor.execute('''
            SELECT dniPaciente, metodoPago, obraSocial, idGrupo
            FROM ListaEspera
            WHERE idTurno = ? AND estado = 'Activo'
            ORDER BY id
        ''', (idTurno,))
        return [dict(fila) for fila in cursor.fetchall()]
    
def buscar_ids_grupo(idGrupo):
    """Retorna una lista con los idTurno de todos los turnos de un grupo"""
    with sqlite3.connect('src/backend/bdd.db') as conexion:
        cursor = conexion.cursor()
        cursor.execute('''
            SELECT idTurno
            FROM ListaEspera
            WHERE idGrupo = ?
        ''', (idGrupo,))
        return [fila[0] for fila in cursor.fetchall()]

def intentar_registrar_reserva_desde_lista_espera(idTurno):    
    pacientes = buscar_en_lista_espera(idTurno)
    if pacientes:
        i=0
        listo=False
        while(not listo and i < len(pacientes)):
            if pacientes[i]["idGrupo"] is not None:
                if(reserva_recurrente_cumple(pacientes[i]["idGrupo"])):
                    ids=buscar_ids_grupo(pacientes[i]["idGrupo"])
                    registrar_reservas_recurrentes(ids,pacientes[i]["obraSocial"],pacientes[i]["metodoPago"],pacientes[i]["dniPaciente"])
                    quitar_de_lista_espera(idTurno, pacientes[i]["dniPaciente"],pacientes[i]["idGrupo"])
                    listo=True
            else:
                registrar_reserva(idTurno, pacientes[i]["obraSocial"],  pacientes[i]["metodoPago"], pacientes[i]["dniPaciente"])
                quitar_de_lista_espera(idTurno, pacientes[i]["dniPaciente"])
                listo=True
            i+=1
            
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