from nicegui import ui, app
from datetime import date, timedelta
from backend.reservas.reserva_bdd import registrarReserva
import sqlite3

# Página de registar reserva
def pagina_reservas():
    def formularioReserva():
        with ui.card().classes('w-150 p-6'):
            with ui.row().classes('w-full no-wrap gap-8 items-start'):
                with ui.column().classes('w-full items-center'):
                    fecha = ui.date().classes('w-full h-90').props(f''':options="d => d >= '{fecha_minima}'"''')
                with ui.column().classes('w-3/5 gap-5'):
                    hora = ui.select(options=horas, label='Horario').classes('w-full')
                    obraSocial = ui.select(options=obrasSociales,label='Obra Social').classes('w-full')
                    metPago = ui.select(options=metodosPago,label='Método de Pago').classes('w-full')
                    tratamiento = ui.select(options=tratamientos,label='Tratamiento').classes('w-full')
            ui.button('Reservar turno',icon='event_available',on_click=lambda: crearReserva(fecha.value,hora.value,tratamiento.value,obraSocial.value,metPago.value,dniPaciente)).classes('w-full text-lg')
    
    def crearReserva(fecha,hora,trat,obraSoc,metPago,dniPac):
        if not fecha:
            ui.notify('Seleccione una fecha', color='warning')
            return
        if not hora:
            ui.notify('Seleccione una hora', color='warning')
            return
        if not obraSoc:
            ui.notify('Seleccione una obra social', color='warning')
            return
        if not metPago:
            ui.notify('Seleccione un método de pago', color='warning')
            return
        if not trat:
            ui.notify('Seleccione un tratamiento', color='warning')
            return
        try:
            registrarReserva(fecha,hora,trat,obraSoc,metPago,dniPac)
            ui.notify('Turno reservado con éxito',color='positive')
        except sqlite3.IntegrityError:
            ui.notify('Turno ya reservado', color='negative')
        except Exception as e: # Verificar errores
            print(e)
### MOVER CONSTANTES A OTRO LADO
    fecha_minima = (date.today() + timedelta(days=7)).strftime('%Y/%m/%d') # EL valor de days se puede cambiar (1 semana)
    dniPaciente = app.storage.user.get('dni')
    tratamientos=['Tren superior','Tren medio','Tren inferior']
    obrasSociales=['IOMA','OSDE','Ninguna']
    metodosPago=['Efectivo','Transferencia','Billetera virtual']
    horas = ['08:00','09:00','10:00','11:00','12:00','13:00','14:00','15:00','16:00','17:00','18:00','19:00','20:00']
####################################### PÁGINA ##################################################
    # Parte superior
    
    # Parte central
    with ui.row().classes('w-full justify-center'):
        formularioReserva()