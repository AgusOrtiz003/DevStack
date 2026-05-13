import sqlite3
# LO ESTOY USANDO PARA PROBAR COMANDOS

conexion = sqlite3.connect('bdd.db')
cursor = conexion.cursor()
conexion.close()