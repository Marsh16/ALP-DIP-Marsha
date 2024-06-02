import pygame
import sys
from Model.LinearGrayLevel import LinearGrayLevel
import numpy as np
from pygame.locals import *
from constants import DROPDOWN_POS_X, DROPDOWN_POS_Y, BUTTON_WIDTH,BUTTON_HEIGHT,OPTION_HEIGHT, clock, screen
from color import color
from dropdown import draw_dropdown
from PIL import Image

pygame.init()

transformation = ["Linear gray level transformation", "Piece-wise gray level transformation", "Logarithmic transformation", "Gamma transformation", "Global histogram equalization (GHE)", "Adaptive histogram equalization (AHE)", "CLAHE", "Single-scale Retinex (SSR)"]
selected_option = "Linear gray level transformation"
show_options = False
pygame.display.set_caption('ALP DIP Marsha')
font = pygame.font.Font('freesansbold.ttf', 32)
input_font = pygame.font.Font('freesansbold.ttf', 26)
user_text = ""
text_surface = input_font.render(user_text,True, color["dropdown_text"])
textRect = text_surface.get_rect()
textRect.center = (1200 // 2, 50)
input_rect = pygame.Rect(DROPDOWN_POS_X,DROPDOWN_POS_Y*5,BUTTON_WIDTH,BUTTON_HEIGHT)
text_type = font.render(selected_option, True,  color["text"])
textRecttype = text_type.get_rect()
textRecttype.center = (1200 // 2, 50)
imp2 = pygame.image.load("/Users/marshalikorawung/Documents/Semester 6/Digital Image Processing/ALP/Lenna.png").convert()
imp = Image.open("/Users/marshalikorawung/Documents/Semester 6/Digital Image Processing/ALP/Lenna.png") 
mode = imp.mode 
size = imp.size 
data = imp.tobytes() 

# Main loop
game_running = True
while game_running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if show_options:
                    for i, option in enumerate(transformation):
                        option_rect = pygame.Rect(DROPDOWN_POS_X, DROPDOWN_POS_Y + BUTTON_HEIGHT + i * OPTION_HEIGHT, BUTTON_WIDTH, OPTION_HEIGHT)
                        if option_rect.collidepoint(mouse_pos):
                            selected_option = option
                            show_options = False
                            text_type = font.render(selected_option, True,  color["text"])
                            textRecttype = text_type.get_rect()
                            textRecttype.center = (1200 // 2, 50)
                            if selected_option == "Linear gray level transformation":
                                imp2 = LinearGrayLevel.LinearGrayLevelImage(imp,mode, size, data)
                            else:
                                imp2 = LinearGrayLevel.scale(imp,mode, size, data)
                            break
                else:
                    if pygame.Rect(DROPDOWN_POS_X, DROPDOWN_POS_Y, BUTTON_WIDTH, BUTTON_HEIGHT).collidepoint(mouse_pos):
                        show_options = not show_options
        elif event.type == KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                user_text = user_text[:-1]
                text_surface = input_font.render(user_text,True, color["text"])
                textRect = text_surface.get_rect()
                textRect.center = (1200 // 2, 80)
            else:
                user_text += event. unicode
                text_surface = input_font.render(user_text,True, color["text"])
                textRect = text_surface.get_rect()
                textRect.center = (1200 // 2, 80)
    
    screen.fill(color["white"])
    screen.blit(text_surface, textRect)
    screen.blit(text_type, textRecttype)
    screen.blit(imp2, (1200 // 3, 600 // 6))
    pygame.draw.rect(screen, color["dropdown_text"], input_rect, 2)
    text_surface = input_font.render(user_text,True, color["text"])
    screen.blit (text_surface, (25,DROPDOWN_POS_Y*6))
    draw_dropdown(screen, selected_option, show_options, transformation)

    pygame.display.update()



   