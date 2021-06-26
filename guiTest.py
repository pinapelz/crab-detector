import tkinter as tk
import tkinter.font as tkFont
from tkinter.filedialog import askopenfilename, asksaveasfilename
from imageai.Detection.Custom import CustomObjectDetection
from imageai.Detection import ObjectDetection
from tkinter import *
import os
from PIL import ImageTk, Image

def open_file():
    filepath = askopenfilename(
        filetypes=[("JPEG", "*.jpg"), ("All Files", "*.*")]
    )
    if not filepath:
        return
    window.title(f"Is It Crab? - {filepath}")
    detector = CustomObjectDetection()
    detector.setModelTypeAsYOLOv3()
    detector.setModelPath("detectCrab.h5")
    detector.setJsonPath("detection_config.json")
    result = 0.0
    detector.loadModel()
    detections = detector.detectObjectsFromImage(input_image=filepath, output_image_path="newImage.jpg")
    for detection in detections:
        print(detection["name"], " : ", detection["percentage_probability"], " : ", detection["box_points"])
        result = detection["percentage_probability"]

        
    if result>=70.0:
        window.verdict.config(text="It's Crab")
        window.imagechange = ImageTk.PhotoImage(Image.open("dog.jpg"))
        label.configure(image=window.imagechange)
        print(result)
        
        
    else:
        window.verdict.config(text="It's Crap")
        newexecution_path = os.getcwd()
        newdetector = ObjectDetection()
        newdetector.setModelTypeAsRetinaNet()
        newdetector.setModelPath( os.path.join(newexecution_path , "resnet50_coco_best_v2.1.0.h5"))
        newdetector.loadModel()
        newdetections = newdetector.detectObjectsFromImage(input_image=os.path.join(newexecution_path , filepath), output_image_path=os.path.join(newexecution_path , "imagenew.jpg"))
        window.imagechange2 = ImageTk.PhotoImage(Image.open("imagenew.jpg"))
        label.configure(image=window.imagechange2)


window = tk.Tk()
labelFont = tkFont.Font(family="Lucida Grande", size=20)
window.verdict = Label(window, text="Select an Image",font=labelFont)
window.title("Is it crab?")
window.rowconfigure(0, minsize=800, weight=1)
window.columnconfigure(1, minsize=800, weight=1)
window.imageone = ImageTk.PhotoImage(Image.open("crab2.jpg"))
label = Label(image=window.imageone)
fr_buttons = tk.Frame(window, relief=tk.RAISED, bd=2)



btn_open = tk.Button(fr_buttons, text="Open", command=open_file)

btn_open.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
#verdict.grid(row=1,column=0,sticky="ns",padx=1,pady=1)

fr_buttons.grid(row=0, column=0, sticky="ns")
label.grid(row=0, column=2, sticky="nsew")
window.verdict.grid(row=0,column=1,stick="ns",padx=1,pady=1)


window.mainloop()

