from color import color
from constants import DROPDOWN_POS_X, DROPDOWN_POS_Y, BUTTON_WIDTH,BUTTON_HEIGHT,FONT_SIZE,OPTION_HEIGHT,FONT_SMALL_SIZE
import pygame
from pygame.locals import *

def draw_dropdown(screen, selected_option, show_options, options):
    button_color = color["button_hover"] if show_options else color["button_bg"]
    pygame.draw.rect(screen, button_color, (DROPDOWN_POS_X, DROPDOWN_POS_Y, BUTTON_WIDTH, BUTTON_HEIGHT))
    pygame.draw.rect(screen, color["button_border"], (DROPDOWN_POS_X, DROPDOWN_POS_Y, BUTTON_WIDTH, BUTTON_HEIGHT), 2)
    font = pygame.font.Font('freesansbold.ttf', FONT_SIZE)
    text_surface = font.render(selected_option, True, color["text"])
    text_rect = text_surface.get_rect(center=(DROPDOWN_POS_X + BUTTON_WIDTH / 2, DROPDOWN_POS_Y + BUTTON_HEIGHT / 2))
    screen.blit(text_surface, text_rect)
    if show_options:
        for i, option in enumerate(options):
            option_y = DROPDOWN_POS_Y + BUTTON_HEIGHT + i * OPTION_HEIGHT
            option_rect = pygame.Rect(DROPDOWN_POS_X, option_y, BUTTON_WIDTH, OPTION_HEIGHT)
            option_color = color["dropdown_hover"] if option_rect.collidepoint(pygame.mouse.get_pos()) else color["dropdown_bg"]
            pygame.draw.rect(screen, option_color, option_rect)
            pygame.draw.rect(screen, color["dropdown_border"], option_rect, 2)
            option_font = pygame.font.Font(None, FONT_SMALL_SIZE)
            option_surface = option_font.render(option, True, color["dropdown_text"])
            option_rect = option_surface.get_rect(center=(DROPDOWN_POS_X + BUTTON_WIDTH / 2, option_y + OPTION_HEIGHT / 2))
            screen.blit(option_surface, option_rect)
