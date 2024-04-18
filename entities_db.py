import os
from datetime import datetime 
from enum import Enum
import sqlalchemy as SQL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

speicherort_db = "sqlite:///GrowDB.db"

try:
    # Verbindung zur Datenbank herstellen
    db_engine = SQL.create_engine(speicherort_db, echo=False)
    Base = declarative_base()
    print("Datenbankverbindung erfolgreich Erstellt!")
except Exception as ex :
    print("Fehler beim erstellen der Datenbankverbindung: " + str(ex))


# Enum-Class for more efficient access to "kind of" the CyberPhsicialDevice
class TypenEnum(Enum):
    DEFAULT = 0
    HAUPTLICHT = 1
    BLUETE_LEUCHTE = 2 
    WUCHS_LEUCHTE = 3 
    UV_LEUCHTE = 4
    IR_LEUCHTE = 5
    ABLUFT_FAN = 11
    ZULUFT_FAN = 12
    UMLUFT_FAN = 13
    HEIZMATTE = 14
    INFOMATERIAL = 20
    TEMP_SENSOR_OBEN = 27
    TEMP_SENSOR_UNTEN = 28
    TEMP_SENSOR_ERDE = 29
    RLF_SENSOR = 31

class AusgabenKategorieEnum(Enum):
    DEFAULT = 0
    SAMEN = 1
    ERDE = 2
    TOPF = 3
    ANZUCHT = 4
    ERNTE = 5
    BOVEDA = 6
    LAGERUNG = 7
    DUENGER = 8
    ZELT = 10
    ABLUFT = 11
    UMLUFT = 12
    HAUPTLED = 13
    ZUSATZLED = 14
    ELEKTRONIK = 15
    VERTIEB = 20
    RBPROJEKT = 30


class AusgabeMap(Base):
    __tablename__ = "Ausgaben"

    ID = SQL.Column(SQL.Integer, primary_key=True) 
    Kategorie = SQL.Column(SQL.Enum(AusgabenKategorieEnum),default=AusgabenKategorieEnum.DEFAULT)
    Item = SQL.Column(SQL.String, default="SQLDefault")
    Einzelpreis = SQL.Column(SQL.Float)
    Stueckzahl = SQL.Column(SQL.Integer)
    Shop = SQL.Column(SQL.String, default="SQLDefault")
    Kommentar = SQL.Column(SQL.String)
    Wann = SQL.Column(SQL.DateTime, default=datetime(year=2001, month=9, day=15))

class ZeltMap(Base):
    __tablename__ = "Zelte"

    ID = SQL.Column(SQL.Integer, primary_key=True)
    Name = SQL.Column(SQL.Integer)
    Breite = SQL.Column(SQL.Integer, default=0)
    Laenge = SQL.Column(SQL.Integer, default=0)
    Hoehe = SQL.Column(SQL.Integer, default=0)
    Erstellt = SQL.Column(SQL.DateTime)


# Klassenmapping für den ORM   
class AktorMap(Base):
    __tablename__ = "Aktoren"  

    ID = SQL.Column(SQL.Integer, primary_key=True) 
    Zelt_ID = SQL.Column(SQL.ForeignKey("Zelte.ID"))
    Name = SQL.Column(SQL.String, default="SQLDefault")
    Typ = SQL.Column(SQL.Enum(TypenEnum, default=TypenEnum.DEFAULT))
    RaspberryPort = SQL.Column(SQL.Integer, default=0)
    VersorgungsSpannung = SQL.Column(SQL.Float, default=0.0)
    MaxLeistungsaufnahme = SQL.Column(SQL.Float, default=0.0)
    Erstellt = SQL.Column(SQL.DateTime, default=datetime(year=2001, month=9, day=15))

    def printAktor(self):
        print("---------------------------------------")
        print("Gerät:           " + self.Name)
        print("DB-ID:           " + str(self.ID))
        print("Typ:             " + str(self.Typ))
        print("Zelt:            " + str(self.Zelt_ID))
        print("RaspiPort:       " + str(self.RaspberryPort))
        print("Spannung:        " + str(self.VersorgungsSpannung) + " V") 
        print("Max. Leistung:   " + str(self.MaxLeistungsaufnahme) + " W") 
        print("Erstellt am:     " + str(self.Erstellt))
        print("---------------------------------------")

# Ersetzt den Konstruktor einer eigenen Entity Klasse
def Aktor(id = 0, name = "MeinAktor", zelt_id = 0, typ=TypenEnum.DEFAULT, raspberry_port=0, versorgungs_spannung=0.0, max_leistung= 0, erstellt=datetime.now()):
    aktor_map = AktorMap()
    aktor_map.ID = id 
    aktor_map.Zelt_ID = zelt_id
    aktor_map.Name = name
    aktor_map.Typ = typ
    aktor_map.RaspberryPort = raspberry_port
    aktor_map.VersorgungsSpannung = versorgungs_spannung
    aktor_map.MaxLeistungsaufnahme = max_leistung
    aktor_map.Erstellt = erstellt
    return aktor_map
# Copy Konstruktor
def AktorFromAktor(aktor=AktorMap()):
    if aktor is None: return None
    ret_aktor = AktorMap()
    ret_aktor.ID = 0
    ret_aktor.Name = aktor.Name
    ret_aktor.Typ = aktor.Typ
    ret_aktor.Zelt_ID = aktor.Zelt_ID
    ret_aktor.RaspberryPort = 0
    ret_aktor.VersorgungsSpannung = aktor.VersorgungsSpannung
    ret_aktor.MaxLeistungsaufnahme = aktor.MaxLeistungsaufnahme
    ret_aktor.Erstellt = datetime.now()
    return ret_aktor



# Tabellen anlegen, falls nicht vorhanden
inspector = SQL.inspect(db_engine)
if inspector.has_table("Aktoren") and inspector.has_table("Ausgaben") and inspector.has_table("Zelte"):
    print("entities_DB.py --> 'Inspector: Alle Tabelle bereits angelegt!'")
else:
    try :
        Base.metadata.create_all(db_engine)
        print("entities_DB.py --> Tabellen erfolgreich erstellt!")
    except Exception as ex :
        print("entities_DB.py --> Fehler beim Erstellen der Tabellen: " + str(ex))
Session = sessionmaker(bind = db_engine)
session = Session()

def ExecuteScript(path=''):
    if not path or path == '':
        return False

    # Überprüfen, ob path existiert und eine Datei ist
    try:
        with open(path, 'r') as file:
            sql_script = file.read()
    except FileNotFoundError:
        print(f'Die Datei {path} wurde nicht gefunden.')
        return False
    except IsADirectoryError:
        print(f'{path} ist ein Verzeichnis, keine Datei.')
        return False

    try:
        session.begin()
        for statement in sql_script.split(';'):
            session.execute(SQL.text(statement))
        session.commit()
    except Exception as ex:
        session.rollback()
        print(f'Fehler beim Ausführen des Skripts: {ex}')
        return False

    return True


# Speichert oder updatet einen Aktor mit gegebener ID. Bei ID = 0, wird immer ein Save ausgeführt und eine ID vergeben. Zu speicherndes Objekt muss Return UND Parameter sein!!! Sonst sessionAbhängigkeit
# Returns:      > 0:    ID des gespeicherten Aktors
#               0:      Not Implemented
#               < 0:    Error     
def SaveOrUpdateAktor(aktor = None):
    if aktor is None: return None
    retAktor = AktorMap()
    with session.begin():
        if aktor.ID == 0:
            # Manuell inkrementieren
            i = 0
            while(aktor.ID == 0):
                i+=1
                if not len(session.query(AktorMap).filter(AktorMap.ID == i).all()) > 0: aktor.ID = i

        # Überprüfe, ob es ID bereits gibt
        if len(session.query(AktorMap).filter(AktorMap.ID == aktor.ID).all()) > 0:
            # Falls ja, Update
            try:
                db_entry = session.query(AktorMap).filter(AktorMap.ID == aktor.ID).first()
                if db_entry.Name != aktor.Name: db_entry.Name = aktor.Name
                if db_entry.Typ != aktor.Typ: db_entry.Typ = aktor.Typ
                if db_entry.Zelt_ID != aktor.Zelt_ID: db_entry.Zelt_ID = aktor.Zelt_ID
                if db_entry.RaspberryPort != aktor.RaspberryPort: db_entry.RaspberryPort = aktor.RaspberryPort
                if db_entry.VersorgungsSpannung != aktor.VersorgungsSpannung: db_entry.VersorgungsSpannung = aktor.VersorgungsSpannung,
                if db_entry.MaxLeistungsaufnahme != aktor.MaxLeistungsaufnahme: db_entry.MaxLeistungsaufnahme = aktor.MaxLeistungsaufnahme,
                if db_entry.Erstellt != aktor.Erstellt: db_entry.Erstellt = aktor.Erstellt
                session.commit()
            except Exception as ex:
                print("There was an Error Updating Aktor '" + aktor.Name + "' to local DB: " + str(ex))
                session.rollback()
                session.close
                return None
        else:
            # Falls nicht, Save
            try:
                session.add(aktor)
                session.commit()
            except Exception as ex:
                print("There was an Error Saving Aktor '" + aktor.Name + "' to local DB: " + str(ex))
                session.rollback()
                session.close
                return None
        retAktor = Aktor(id=aktor.ID, name=aktor.Name, typ=aktor.Typ, zelt_id=aktor.Zelt_ID, raspberry_port=aktor.RaspberryPort, versorgungs_spannung=aktor.VersorgungsSpannung, max_leistung=aktor.MaxLeistungsaufnahme, erstellt=aktor.Erstellt)
        session.close()
    return retAktor

def DeleteAktor(aktor=AktorMap()):
    if aktor is None: return True
    with session.begin():
        del_aktor = session.query(AktorMap).filter(AktorMap.ID == aktor.ID).first()
        if del_aktor == None: return False
        try:    
            session.delete(del_aktor)
            session.commit()
        except Exception as ex:
            print(str(ex))
            session.rollback()
            session.close()
            return False 
        session.close
    return True

def LoadAktoren():
    myAktoren = list()
    with session.begin():
        aktoren_query = session.query(AktorMap).all()
        if aktoren_query is None:
            return None
        elif  len(aktoren_query) < 1:
            return [AktorMap()] * 1
        for result in aktoren_query:
            myAktoren.append(Aktor(id=result.ID, name=result.Name, typ=result.Typ, zelt_id=result.Zelt_ID, raspberry_port=result.RaspberryPort, versorgungs_spannung=result.VersorgungsSpannung, erstellt=result.Erstellt, max_leistung=result.MaxLeistungsaufnahme))
        session.close()
    return myAktoren



# Test Routine as main of this file!
aktoren_query = session.query(AktorMap).all()
if aktoren_query is None or len(aktoren_query) < 1:
    print(f"Fehler beim erstellen des Testquerys...\n...")
else:
    print("Testquery erfolgreich erstellt...\n...")   
session.close()
print("Successfully imported 'entities_db.py\n----------------------------------")
