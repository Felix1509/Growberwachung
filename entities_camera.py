from time import sleep
from datetime import datetime
import os
from picamera import PiCamera

def TakeFoto(Zelt_ID, cam):
    
    jetzt = datetime.now()  
    
    fullpath = "Fotos"
    if not os.path.isdir(fullpath):
        os.mkdir(fullpath)  
    fullpath += "/Zeitraffer"
    if not os.path.isdir(fullpath):
        os.mkdir(fullpath)  
    fullpath += "/Zelt" + str(Zelt_ID).zfill(2)
    if not os.path.isdir(fullpath):
        os.mkdir(fullpath)        
    fullpath += "/" + str(jetzt.year).zfill(4)
    if not os.path.isdir(fullpath):
        os.mkdir(fullpath)
    fullpath += "/" + str(jetzt.month).zfill(2)
    if not os.path.isdir(fullpath):
        os.mkdir(fullpath)
    fullpath += "/" + str(jetzt.day).zfill(2)
    if not os.path.isdir(fullpath):
        os.mkdir(fullpath)
    filename = "Zeitraffer_Zelt" + str(Zelt_ID) + "_" + str(jetzt.year).zfill(4) + str(jetzt.month).zfill(2) + str(jetzt.day).zfill(2) + str(jetzt.hour).zfill(2) + str(jetzt.minute).zfill(2) + str(jetzt.second).zfill(2) + ".jpg"
    
    print("Timelapse: Begin capture to file:\n " + fullpath + "/" + filename)
    try:
        cam.start_preview()
        sleep(5)
        cam.annotate_text = str(jetzt)
        cam.capture(fullpath + "/" + filename)
        cam.stop_preview()
        print("Timelapse: Successfully took Foto for Zeitraffer!")
    except Exception as ex: 
        print("Timelapse: Error while taking Foto for Zeitraffer: " + str(ex))

# Kein Plan ob das geht, werden wir ja sehen...
# class LiveCameraFrame(ttk.Frame):
#     def __init__(self, master=None, **kwargs):
#         super().__init__(master, **kwargs)
#         self.camera = PiCamera()

#         self.label = ttk.Label(self)
#         self.label.pack()

#         self.start_button = ttk.Button(self, text="Start", command=self.start_camera)
#         self.start_button.pack()

#         self.stop_button = ttk.Button(self, text="Stop", command=self.stop_camera, state=tk.DISABLED)
#         self.stop_button.pack()

#     def start_camera(self):
#         self.camera.start_preview()
#         self.start_button.configure(state=tk.DISABLED)
#         self.stop_button.configure(state=tk.NORMAL)

#     def stop_camera(self):
#         self.camera.stop_preview()
#         self.start_button.configure(state=tk.NORMAL)
#         self.stop_button.configure(state=tk.DISABLED)

#     def close_camera(self):
#         self.camera.close()

print("Successfully imported 'entities_camera.py\n----------------------------------")