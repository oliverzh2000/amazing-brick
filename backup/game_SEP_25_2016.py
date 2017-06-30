# Amazing Brick
# Oliver Zhang
# Sep 25 2016
"""
Features and problems history:

Sep 20 2016:
    Can use update calls done using dirty rect and not the entire screen.

Sep 25 2016:
    level generation creates new levels and deletes old ones continuously.
    Need to incorporate delta time to prevent temporal aliasing between frames.
"""
import pygame, sys
from random import randint, seed
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
prev_level_coords = (None, None)
shapes = []
colours = []


def generate_level((prev_hole_left, prev_hole_right)):
    # print prev_hole_left, prev_hole_right
    hole_left = randint(level_margin, width - level_margin - level_width)
    hole_right = hole_left + level_width

    left_side = Rect(0, -level_height - level_sep, hole_left, level_height)
    right_side = Rect(hole_right, -level_height - level_sep, width - hole_right, level_height)

    block1, block2 = Rect(0, 0, block_size, block_size), Rect(0, 0, block_size, block_size)
    block1.centerx = randint(min(prev_hole_left, hole_left), max(prev_hole_right, hole_right))
    block2.centerx = randint(min(prev_hole_left, hole_left), max(prev_hole_right, hole_right))
    block1.centery = -level_height - (level_sep - level_height) / 3
    block2.centery = -level_height - (level_sep - level_height) * 2 / 3

    shapes.extend([block1, block2, left_side, right_side])
    global prev_level_coords
    prev_level_coords = (hole_left, hole_right)


def init():
    hole_left = randint(level_margin, width - level_margin - level_width)
    hole_right = hole_left + level_width
    shapes.append(Rect(0, -level_height, hole_left, level_height))  # left
    shapes.append(Rect(hole_right, -level_height, width - hole_right, level_height))  # right
    global prev_level_coords
    prev_level_coords = (hole_left, hole_right)

    screen.fill(back_color)
    display.update()


def logic():
    for shape in shapes:
        shape.move_ip(0, frame_movement)
    shapes[:] = [shape for shape in shapes if shape.top <= height]
    if shapes[-1].bottom > 0:
        generate_level(prev_level_coords)


def events():
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()


def render():
    screen.fill(back_color)
    for shape in shapes:
        draw.rect(screen, (255, 0, 0), shape)
    updates = [shape.inflate(0, frame_movement * 2) for shape in shapes]
    updates.append(Rect(0, height - frame_movement, width, frame_movement))
    display.update(updates)


seed(7)
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