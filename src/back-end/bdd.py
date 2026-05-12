import sqlite3
con = sqlite3.connect("bdd.db")

cur = con.cursor()
cur.execute("CREATE TABLE reserva(fecha,)")