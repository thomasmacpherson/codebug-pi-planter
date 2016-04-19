import pygame
import os, sys
import pygame.locals
import random
import time
import codebug_tether
import codebug_tether.sprites
from codebug_tether import (IO_DIGITAL_INPUT, IO_ANALOGUE_INPUT, IO_PWM_OUTPUT, IO_DIGITAL_OUTPUT)
from numpy import interp

logo = pygame.image.load('codebug-logo.png')
image = pygame.image.load('plant-pot-with-resistor.png')

codebug = codebug_tether.CodeBug()
codebug.set_leg_io(0, IO_ANALOGUE_INPUT)

# if the reading goes below this threshold, the plant needs watering
water_threshold = 20

red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
yellow = (255,255,0)
white = (255,255,255)
black =(0,0,0)

size = screen_width, screen_height = 800, 700
#speed = [2, 2]


# paddle orientation
HORIZONTAL = 0
VERTICAL = 1


screen = pygame.display.set_mode(size,pygame.FULLSCREEN)

#score1 = 0
#score2 = 0

# Initialise pygame, needed for fonts
pygame.init()
# turn off cursor
pygame.mouse.set_visible(0)

font = pygame.font.Font(None,48)

big_font = pygame.font.Font(None, 100)


plant_text_display = big_font.render("Plant moisture",True , blue)
plant_text_rect = plant_text_display.get_rect()
plant_text_rect.centerx = screen_width/2
plant_text_rect.centery = screen_height/5

plant_warning_display = big_font.render("Water me please",True , red)
plant_warning_rect = plant_warning_display.get_rect()
plant_warning_rect.centerx = screen_width/2
plant_warning_rect.centery = screen_height/5 - (plant_text_display.get_height()+10)

def check_for_input():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.KEYDOWN:
            # if event.key == pygame.K_LEFT:
            #     paddles[0].x += 10
            if event.key == pygame.K_ESCAPE:
                sys.exit()

water_scale_height = 20
water_scale_outline_height = water_scale_height + 9
water_scale_outline_width = 255 + 10
water_scale_y = screen_height/5 + (plant_text_display.get_height())


while True:
    screen.fill(white)
    screen.blit(image,((screen_width-image.get_width())/2,screen_height-(image.get_height()+20)))
    an_value = codebug.read_analogue(0)
    print(an_value)
    number = interp(an_value,[90,108],[100,0])
    screen.blit(plant_text_display, plant_text_rect)

    plant_number_display = big_font.render(str(int(number)),True , blue)
    plant_number_rect = plant_number_display.get_rect()
    plant_number_rect.centerx = plant_text_rect.centerx + (plant_text_display.get_width() /2) + 20 + (plant_number_display.get_width()/2)
    plant_number_rect.centery = plant_text_rect.centery
    screen.blit(plant_number_display, plant_number_rect)


    water_scale = pygame.Rect(( screen_width - water_scale_outline_width)/2 + 5, water_scale_y - (water_scale_height/2), number*2.55, water_scale_height)
    pygame.draw.rect(screen, blue, water_scale, 0)

    water_scale_outline = pygame.Rect((screen_width - water_scale_outline_width)/2, water_scale_y - (water_scale_outline_height/2), water_scale_outline_width, water_scale_outline_height)
    pygame.draw.rect(screen, blue, water_scale_outline, 4)

    if number < water_threshold:
        #print("Water me")
        screen.blit(plant_warning_display, plant_warning_rect)

    screen.blit(logo,(10,screen_height-logo.get_height()-10))
    screen.blit(screen,(0,0))
    pygame.display.flip()
    time.sleep(1)
    check_for_input()

