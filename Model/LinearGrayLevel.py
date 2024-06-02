from Model.Transformation import Transformation
import pygame
import numpy as np
import pygame.surfarray as surfarray
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
    
    def mask(image):
        im_np = np.array(image)
        gray_im_np = (0.299 * im_np[:,:,0]) + (0.587 * im_np[:,:,1]) + (0.114 * im_np[:,:,2])
        image_th = np.asarray(np.uint8(gray_im_np))
        red_mask = im_np[:, :, 0] < 180
        im_np[red_mask] = 0
        rgbarray = surfarray.make_surface(im_np)
        rgbarray = pygame.transform.rotate(rgbarray,270)
        rgbarray = pygame.transform.flip(rgbarray,True, False)
        return rgbarray
    
    def blue(image):
        im_np = np.array(image)
        gray_im_np = (0.299 * im_np[:,:,0]) + (0.587 * im_np[:,:,1]) + (0.114 * im_np[:,:,2])
        image_th = np.asarray(np.uint8(gray_im_np))
        blue_mask = im_np[:, :, 2] < 165
        im_np[blue_mask] = 0
        rgbarray = surfarray.make_surface(im_np)
        return rgbarray
