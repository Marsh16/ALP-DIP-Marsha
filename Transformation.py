from tkinter import *
from PIL import ImageTk, Image, ImageEnhance
import math
import numpy as np
from scipy.ndimage import gaussian_filter
from skimage import exposure

# Logic untuk transformasi
class Transformation():
    def greyLevelTransformation(var ,filename, a=2.0, b=1.0):
        img = Image.open(filename).convert("L")
        # Apply linear transformation (s = a * r + b)
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(a) 
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(1.0 + b)
        img.getextrema() 
        image = ImageTk.PhotoImage(img)        
        return image
    
    def pieceWiseGreyLevelTransformation(var ,filename, thresholds=[0, 100, 255], output_levels =[0, 200, 255]):
        img = Image.open(filename).convert("L")
        pixels = img.load()
        width, height = img.size
        for x in range(width):
            for y in range(height):
                gray_level = pixels[x, y]
                new_level = 0 

                for i in range(len(thresholds)):
                    if gray_level <= thresholds[i]:
                        new_level = output_levels[i - 1]
                        break 
                pixels[x, y] = new_level
        img.getextrema() 
        image = ImageTk.PhotoImage(img)        
        return image
    
    def logaritmicTransformation(var ,filename, c=1.0):
        img = Image.open(filename).convert("L")
        log_img = img.point(lambda p: c * math.log(1 + p, 2)) 
        min_val = min(log_img.getdata())
        max_val = max(log_img.getdata())
        if min_val != max_val:  
            log_img = log_img.point(lambda p: int((p - min_val) * 255 / (max_val - min_val)))
        log_img.getextrema()
        image = ImageTk.PhotoImage(log_img)        
        return image
    
    def gammaTransformation(var ,filename, gamma=0.5):
        img = Image.open(filename).convert("L")
        pixels = img.load()
        width, height = img.size
        for x in range(width):
            for y in range(height):
                gray_level = pixels[x, y]

                # Apply gamma transformation (new_level = (gray_level / 255) ** gamma * 255)
                new_level = int((gray_level / 255) ** gamma * 255)  # Ensure integer output

                # Clamp new_level to valid grayscale range (0-255)
                new_level = max(0, min(new_level, 255))

                pixels[x, y] = new_level
        img.getextrema() 
        image = ImageTk.PhotoImage(img)        
        return image
    
    def global_histogram_equalization(var ,filename):
        img = Image.open(filename).convert("L")
        pixels = img.load()
        width, height = img.size
        # Calculate histogram (frequency of each gray level)
        histogram = [0] * 256  # Initialize histogram with zeros
        for x in range(width):
            for y in range(height):
                gray_level = pixels[x, y]
                histogram[gray_level] += 1

        # Calculate cumulative distribution function (CDF)
        cdf = [0] * 256
        cdf[0] = histogram[0]
        for i in range(1, 256):
            cdf[i] = cdf[i - 1] + histogram[i]

        # Normalize CDF (scale to range 0-255)
        cdf_normalized = [int(val * 255 / (width * height)) for val in cdf]

        # Apply histogram equalization (map each pixel to its new gray level based on CDF)
        for x in range(width):
            for y in range(height):
                gray_level = pixels[x, y]
                new_level = cdf_normalized[gray_level]
                pixels[x, y] = new_level
        img.getextrema() 
        image = ImageTk.PhotoImage(img)        
        return image
    
    def hist_equalization(img):
        array = np.asarray(img)
        bin_cont = np.bincount(array.flatten(), minlength=256)
        pixels = np.sum(bin_cont)
        bin_cont = bin_cont / pixels
        cumulative_sumhist = np.cumsum(bin_cont)
        map = np.floor(255 * cumulative_sumhist).astype(np.uint8)
        arr_list = list(array.flatten())
        eq_arr = [map[p] for p in arr_list]
        arr_back = np.reshape(np.asarray(eq_arr), array.shape)
        return arr_back


    def adaptive_histogram_equalization(var, filename, rx=136, ry=185):
        img = Image.open(filename).convert("L") # Load and convert to grayscale
        im_np = np.array(img)
        v = im_np
        img_eq = np.empty((v.shape[0], v.shape[1]), dtype=np.uint8)
        for i in range(0, v.shape[1], rx):
            for j in range(0, v.shape[0], ry):
                t = v[j:j + ry, i:i + rx]
                c = Transformation.hist_equalization(t)
                img_eq[j:j + ry, i:i + rx] = c
        pil_image = Image.fromarray(img_eq)
        pil_image.getextrema() 
        image = ImageTk.PhotoImage(pil_image)        
        return image
    

    def adaptive_histogram_equalization_clahe(var, filename):
        img = Image.open(filename).convert("L") # Load and convert to grayscale
        im_np = np.array(img)
        clahe = exposure.equalize_adapthist(im_np,clip_limit=0.3)
        pil_image = Image.fromarray(clahe*200)
        pil_image.getextrema() 
        image = ImageTk.PhotoImage(pil_image)        
        return image
    
    def SSR(var, filename, variance=100):
        img = Image.open(filename)
        img = np.float64(img) + 1.0
        img_retinex = Transformation.singleScaleRetinex(img, variance)
        if len(img_retinex.shape) == 2:
            pass
        else:
            for i in range(img_retinex.shape[2]):
                unique, count = np.unique(np.int32(img_retinex[:, :, i] * 100), return_counts=True)
                for u, c in zip(unique, count):
                    if u == 0:
                        zero_count = c
                        break            
                low_val = unique[0] / 100.0
                high_val = unique[-1] / 100.0
                for u, c in zip(unique, count):
                    if u < 0 and c < zero_count * 0.1:
                        low_val = u / 100.0
                    if u > 0 and c < zero_count * 0.1:
                        high_val = u / 100.0
                        break            
                img_retinex[:, :, i] = np.maximum(np.minimum(img_retinex[:, :, i], high_val), low_val)
                
                img_retinex[:, :, i] = (img_retinex[:, :, i] - np.min(img_retinex[:, :, i])) / \
                                    (np.max(img_retinex[:, :, i]) - np.min(img_retinex[:, :, i])) \
                                    * 255
        img_retinex = np.uint8(img_retinex)        
        enhanced_img = Image.fromarray(img_retinex)
        enhanced_img.getextrema()
        image = ImageTk.PhotoImage(enhanced_img)        
        return image    
    
    def singleScaleRetinex(img, variance):
        blurred = gaussian_filter(img, variance)
        retinex = np.log10(img) - np.log10(blurred)
        return retinex