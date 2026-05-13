from nicegui import ui

# Acá irian todos los import de páginas .py que se tienen que ejecutar
from frontend.pages import listar_reservas_pendientes
from frontend.pages import home, listar_turnos, listar_turnos_pacientes, registar_turno, reservas

ui.run(language='es')