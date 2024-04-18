import entities_db as DB
import entities_zeitplan as ZP
from datetime import datetime
if DB.ExecuteScript('SQL/ZelteSkript.sql'): print("Hurensohn!")
if DB.ExecuteScript('SQL/AktorenSkript.sql'): print("Hurensohn!")
if DB.ExecuteScript('SQL/AusgabenSkript.sql'): print("Hurensohn!")
meinAktor = DB.LoadAktoren()[0]
meinAktor.printAktor()
print(str(datetime.now().month).zfill(2))
print(str(18%15))