from tkinter import *
from PIL import ImageTk, Image

# Logic untuk transformasi
class Transformation():
    def greyLevelTransformation(var ,filename):
        image5 = Image.open(filename)
        r, g, b = image5.split()
        b = b.point(lambda i: 255)
        coloredimage = Image.merge("RGB", (r, g, b))
        coloredimage.getextrema()
        coloredimage = ImageTk.PhotoImage(coloredimage)
        return coloredimage