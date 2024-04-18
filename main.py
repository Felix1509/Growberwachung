import entities_db as DB
import entities_zeitplan as ZP
import entities_camera as CAM
from picamera import PiCamera
import time
from datetime import datetime
import RPi.GPIO as GPIO

# GPIO.setmode(GPIO.BCM)
# aktoren = DB.LoadAktoren()
# print ("Successfully loaded Aktoren...\nCount: " + str(len(aktoren)))
# aktoren = list(filter(lambda x: x.Zelt_ID == 3, aktoren))
# zeitplaene = [ZP.create_schedule('')] * len(aktoren)
# i = 0
# for a in aktoren:
#     # Zeitpläne einlesen und GPIO konfigurieren
#     zeitplaene[i] = (ZP.load_schedule_from_file(a.Zelt_ID, a.ID))
#     GPIO.setup(a.RaspberryPort, GPIO.OUT)
#     i += 1

current_hour = datetime.now().hour
current_minute = datetime.now().minute
current_checked = False 

cam = PiCamera()
cam.led = False
cam.resolution=(3280, 2464)
try:
    while True:
        if not current_checked:
            strOutput = "---------------------------------------------------------------------\nMain Thread: Writing digital Outputs at time " + str(datetime.now()) + "\n.......................................\n\n"
            current_checked = True

            # Check itself starts here
            # i = 0
            # for aktor in aktoren:
                # Zeitpläne einlesen und Ausgänge schalten
                
            #     if zeitplaene[i][current_hour * 60 + current_minute]:
            #         GPIO.output(aktor.RaspberryPort, GPIO.HIGH)
            #         strOutput += f"{str(i).zfill(2)}: Set '{str(aktor.Name)}' at GPIO <{str(aktor.RaspberryPort).zfill(2)}> to HIGH\n"
            #     else:
            #         GPIO.output(aktor.RaspberryPort, GPIO.LOW)
            #         strOutput += f"{str(i).zfill(2)}: Set '{str(aktor.Name)}' at GPIO <{str(aktor.RaspberryPort).zfill(2)}> to LOW\n"
            #     i += 1
            # strOutput += "---------------------------------------------------------------------"
            # print(strOutput)

            # Zeitrafferaufnahme machen - alle 15 Minuten, wenn Licht an
            # i = 0
            # licht_an = False
            # for aktor in aktoren:
            #     if (aktor.Typ == DB.TypenEnum.HAUPTLICHT or aktor.Typ == DB.TypenEnum.IR_LEUCHTE) and zeitplaene[i][current_hour * 60 + current_minute]:
            #         licht_an = True
            #     i += 1
                    
            if (current_minute % 1 == 0):
                print("Penis")
                CAM.TakeFoto(420, cam)
                first_run = False

        else:
            # Überprüfe, ob schon nächste Minute ist, alle 5 Sekunden
            jetzt = datetime.now()
            if jetzt.hour > current_hour or jetzt.minute > current_minute:
                # Start new Check
                current_hour = jetzt.hour
                current_minute = jetzt.minute
                current_checked = False
            else:
                time.sleep(5)
except KeyboardInterrupt: 
    print("Growberwachung: Shut down main program...")
    GPIO.cleanup()