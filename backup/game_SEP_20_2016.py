# Amazing Brick
# Oliver Zhang
# Sep 20 2016

import pygame, sys
from random import randint
from pygame import *

game_over = False
pygame.init()
width, height, = 800, 600
back_color = (240, 240, 240)
clock = pygame.time.Clock()
screen = display.set_mode((width, height))

level_sep = 400
level_height = 50
level_width = 200
level_margin = 100
block_size = 30
frame_movement = 3

score = 0
next_level_coords = (None, None)
shapes = []
colours = []

def generate_level((hole_left, hole_right)):
    if hole_left == None or hole_right == None:
        hole_left = randint(level_margin, width - level_margin - level_width)
        hole_right = hole_left + level_width
    next_hole_left = randint(level_margin, width - level_margin - level_width)
    next_hole_right = next_hole_left + level_width

    left_side = Rect(0, -level_height, hole_left, level_height)
    right_side = Rect(hole_right, -level_height, width - hole_right, level_height)

    block1, block2 = Rect(0, 0, block_size, block_size), Rect(0, 0, block_size, block_size)
    block1.centerx = randint(min(hole_left, next_hole_left), max(hole_right, next_hole_right))
    block2.centerx = randint(min(hole_left, next_hole_left), max(hole_right, next_hole_right))
    block1.centery = -level_height - (level_sep - level_height) / 3
    block2.centery = -level_height - (level_sep - level_height) * 2 / 3

    shapes.extend([left_side, right_side, block1, block2])
    global next_level_coords
    next_level_coords = (next_hole_left, next_hole_right)

def init():
    generate_level((None, None))
    print shapes
    screen.fill(back_color)
    display.update()


def logic():
    for shape in shapes:
        shape.move_ip(0, frame_movement)
    shapes[:] = [shape for shape in shapes if shape.top <= height]
    # if shapes[0].top >= level_sep:
        # generate_level(next_level_coords)

def events():
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()


def render():
    screen.fill(back_color)
    for shape in shapes:
        print shape
        draw.rect(screen, (255, 0, 0), shape)
    updates = [shape.inflate(0, frame_movement * 2) for shape in shapes]
    updates.append(Rect(0, height - frame_movement, width, frame_movement))
    display.update(updates)

init()
frame = 0
while not game_over:
    events()
    logic()
    render()
    clock.tick(60)
    frame += 1
    print frame
pygame.quit()
sys.exit()