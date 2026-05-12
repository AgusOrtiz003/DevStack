import sqlite3
con = sqlite3.connect("reservas.db")

cur = con.cursor()
cur.execute("CREATE TABLE reservas")

res = cur.execute("SELECT name FROM sqlite_master")
res.fetchone()

cur.execute("""
    INSERT INTO 
""")