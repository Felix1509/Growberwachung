import entities_db as DB
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

# region 'Set Up Window'
# Hauptfenster instanziieren 
mainWindow = tk.Tk()
mainWindow.title("Penis")
windowSizeX = mainWindow.winfo_screenwidth()    # Get Pixels X, window should reach over whole screan
windowSizeY = mainWindow.winfo_screenheight()
mainWindow.overrideredirect(True)   # Window without "X"- or minimize option (drag-bar).
mainWindow.geometry("{0}x{1}".format(windowSizeX, windowSizeY)) # Pass Size to window.
# Bild Laden und Größe auf Fenstergröße setzen
nonusablebackgroundImage = Image.open("E:\\Projekte\\Growberwachung\\Resources\\Bilder\\Hintergrund.jpg").resize((int(windowSizeX), int(windowSizeY)))
usableBackgroundImage = ImageTk.PhotoImage(nonusablebackgroundImage)
# endregion

# Funktion zum Erzeugen der Labels mit Grid-Layout
def erstelle_labels():
    i = 0
    myAktoren = DB.LoadAktoren()
    if myAktoren is not None:
        for aktor in myAktoren:
            label = ttk.Label(mainWindow, name="label"+str(i) ,text=aktor.Name + " Nr.: " + str(aktor.ID))
            label.grid(row=i+1, column=0, padx=10, pady=10)
            i += 1

# Define all GUI-Widgets needed for Program
#   Labels
#   Label für den Hintergrund
labelBackground = ttk.Label(mainWindow, image = usableBackgroundImage) 
# Pack all Labels to their final position
labelBackground.grid(column = 0, row = 0)

# Ein Button zum Erzeugen der Labels aufrufen
button = tk.Button(mainWindow, text="Labels erstellen", command=erstelle_labels)
button.grid(row=0, column=0, pady=10)
# Main Event-Handler-Schleife des Hauptfensters starten
mainWindow.mainloop()

print("Ich bin ein Hurensohn!")