from Model.Transformation import Transformation
import pygame
import numpy as np
from PIL import Image, ImageOps 

class LinearGrayLevel(Transformation):        
    def LinearGrayLevelImage(image,mode, size, data):
        py_image = pygame.image.fromstring(data, size, mode) 
        image = pygame.transform.grayscale(py_image)
        return image
    
    def scale(image,mode, size, data):
        py_image = pygame.image.fromstring(data, size, mode) 
        image = pygame.transform.scale(py_image, (200, 200))
        return image
