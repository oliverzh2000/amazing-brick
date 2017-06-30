import pygame
from pygame import *
import sys

pygame.init()
width, height, = 800, 600
back_color = (240, 240, 240)
clock = pygame.time.Clock()
screen = display.set_mode((width, height), RESIZABLE)


def events():
    global done, width, height
    for event in pygame.event.get():
        if event.type == QUIT:
            done = True
        if event.type == VIDEORESIZE:
            width, height = event.size
            screen = display.set_mode((width, height), RESIZABLE)
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                done = True


def render():
    screen.fill(back_color)
    display.update()


done = False
while not done:
    clock.tick(60)
    events()
    render()
pygame.quit()
sys.exit()