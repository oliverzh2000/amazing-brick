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
import time

game_over = False
pygame.init()
width, height, = 800, 600
back_color = (240, 240, 240)
clock = pygame.time.Clock()
screen = display.set_mode((width, height))

movement_speed = 0.5  # pixels per ms
level_sep = 400
level_height = 50
level_width = 200
level_margin = 150
block_size = 30
brick_size = 20
brick_side_speed = 0.08  # pixels per ms
brick_hit_speed = -0.6
brick_accel = 0.0013  # pixels per ms per ms

score = 0
prev_level_coords = (None, None)
shapes = []
colours = []
brick = (brk_px, brk_py, brk_vx, brk_vy) = (width/2, height/2 + 1, 0.0, 0.0)

def brick_pointlist(px, py, size):
    return [(px + size, py), (px, py - size), (px - size, py), (px, py + size), ]


def generate_level((prev_hole_left, prev_hole_right)):
    # print prev_hole_left, prev_hole_right
    hole_left = randint(level_margin, width - level_margin - level_width)
    hole_right = hole_left + level_width

    left_side = Rect(0, -level_height - level_sep, hole_left, level_height)
    right_side = Rect(hole_right, -level_height - level_sep, width - hole_right, level_height)

    block1, block2 = Rect(0, 0, block_size, block_size), Rect(0, 0, block_size, block_size)
    block1.centerx = randint(min(prev_hole_left, hole_left), max(prev_hole_right, hole_right))
    block2.centerx = randint(min(prev_hole_left, hole_left), max(prev_hole_right, hole_right))
    block1.centery = -level_height - (level_sep - level_height) / 4
    block2.centery = -level_height - (level_sep - level_height) * 3 / 4

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


def logic(dt):
    global brk_px, brk_py, brk_vy
    brk_vy += brick_accel * dt
    brk_px += brk_vx * dt
    brk_py += brk_vy * dt
    if brk_py <= height/2:
        camera_vy = -brk_vy if brk_vy < 0 else 0
        for shape in shapes:
            shape.move_ip(0, camera_vy * dt)
        brk_py += camera_vy * dt
        shapes[:] = [shape for shape in shapes if shape.top <= height]
        if shapes[-1].bottom > 0:
            generate_level(prev_level_coords)


def events():
    for event in pygame.event.get():
        if event.type == QUIT:
            global game_over
            game_over = True
        if event.type == KEYDOWN:
            global brk_vy, brk_vx
            if event.key == K_LEFT:
                brk_vx = -brick_side_speed
                brk_vy = brick_hit_speed
            if event.key == K_RIGHT:
                brk_vx = brick_side_speed
                brk_vy = brick_hit_speed


def render():
    screen.fill(back_color)
    for shape in shapes:
        draw.rect(screen, (255, 0, 0), shape)
    # draw.rect(screen, (100, 100, 100), Rect(0, height/2, width, 2))
    draw.polygon(screen, (10, 10, 10), brick_pointlist(brk_px, brk_py, brick_size))
    # updates = [shape.inflate(0, frame_movement * 2) for shape in shapes]
    # updates.append(Rect(0, height - frame_movement, width, frame_movement)) # bottom edge
    # display.update(updates)
    display.update()

seed(7)
init()
frame = 0
while not game_over:
    dt = clock.tick(60)
    if dt > 50:
        dt = 0
    events()
    logic(dt)
    render()
    frame += 1
    # print frame

pygame.quit()
sys.exit()

'''start = time.time()
while loop...

elapsed = time.time() - start
print "time", elapsed
print "fps", frame/elapsed
print "spf", elapsed/frame * 1000, "ms"'''