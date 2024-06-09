# Import library
from Transformation import Transformation
import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
from tkinter import filedialog
import os

# Ukuran window, class tranformasi dan lain lain
window = Tk()
transform = Transformation()
window.title("Pictures transformer")
window.geometry("900x600+100+100")
window.configure(bg="#e2f9b8")

# Inisialisasi variable untuk dropdown
transformation = ["Linear gray level transformation", "Piece-wise gray level transformation", "Logarithmic transformation", "Gamma transformation", "Global histogram equalization (GHE)", "Adaptive histogram equalization (AHE)", "CLAHE", "Single-scale Retinex (SSR)"]
variable = StringVar(window)
variable.set(transformation[0]) # default value

# Menampilkan image picker
def showimage():
    global filename
    global importedimage
    filename = filedialog.askopenfilename(initialdir=os.getcwd(),
                                          title="Select image file", filetypes=(("PNG file", "*.png"),
                                                                                ("JPG file", "*.jpg"),
                                                                                ("JPEG file", "*.jpeg"),
                                                                                ("ALL file", "*.txt")))
    importedimage = Image.open(filename)
    importedimage = ImageTk.PhotoImage(importedimage)
    lbl.configure(image=importedimage, width=380, height=320)
    lbl.image = importedimage

# Pilihan logic dari dropdown untuk hasil transformasi
def transformations(var):
        if variable.get() == transformation[0]:
            colorimage = transform.greyLevelTransformation(filename)
            lbl.configure(image= colorimage, width=380, height=320)
            lbl.image = colorimage
        elif variable.get() == transformation[1]:
            colorimage = transform.pieceWiseGreyLevelTransformation(filename)
            lbl.configure(image= colorimage, width=380, height=320)
            lbl.image = colorimage
        elif variable.get() == transformation[2]:
            colorimage = transform.logaritmicTransformation(filename)
            lbl.configure(image= colorimage, width=380, height=320)
            lbl.image = colorimage
        elif variable.get() == transformation[3]:
            colorimage = transform.gammaTransformation(filename)
            lbl.configure(image= colorimage, width=380, height=320)
            lbl.image = colorimage
        elif variable.get() == transformation[4]:
            colorimage = transform.global_histogram_equalization(filename)
            lbl.configure(image= colorimage, width=380, height=320)
            lbl.image = colorimage
        elif variable.get() == transformation[5]:
            colorimage = transform.adaptive_histogram_equalization(filename)
            lbl.configure(image= colorimage, width=380, height=320)
            lbl.image = colorimage
        elif variable.get() == transformation[6]:
            colorimage = transform.adaptive_histogram_equalization_clahe(filename)
            lbl.configure(image= colorimage, width=380, height=320)
            lbl.image = colorimage
        elif variable.get() == transformation[7]:
            colorimage = transform.SSR(filename)
            lbl.configure(image= colorimage, width=380, height=320)
            lbl.image = colorimage
        else:
            lbl.configure(image=importedimage, width=380, height=320)
            lbl.image = importedimage

# Tampilan GUI
dropdown = OptionMenu(window, variable, *transformation, command=transformations)
dropdown.pack(pady=80,fill=BOTH, padx=300)

Label(text=variable.get(), font="arial 30 bold", fg="#313715", bg="#e2f9b8").place(x=250, y=20)

selectimage = Frame(width=400, height=400, bg="#939f5c")
selectimage.place(x=280, y=120)

f = Frame(selectimage, bg="black", width=380, height=320)
f.place(x=10, y=10)

lbl = Label(f, bg="black")
lbl.place(x=0, y=0)

Button(selectimage, text="Select image", width=12, height=2, font="arial 14 bold", command=showimage).place(x=130, y=340)

window.mainloop()