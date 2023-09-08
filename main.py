import tkinter as tk
import threading as Task
import time

iami = 0
root = tk.Tk()
Label1 = tk.Label(root, text="This is a test window")
Button1 = tk.Button(root, text="Button")


def printShit():
    global iami
    while True:
        iami += 1
        print(str(iami))
        time.sleep(0.1)
def button1_click():
    Button1.config(text="[ " + Button1.cget("text") + " ]")
        
def runTkinter():
    global root
    Label1.pack()
    Button1.pack()
    
    def on_closing():
        root.destroy()
    
    # Verbinde die Funktion mit dem Schließen-Event
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

b = Task.Thread(name="Calculator", target=printShit)
f = Task.Thread(name="GUI", target=runTkinter)

b.start()
f.start()
