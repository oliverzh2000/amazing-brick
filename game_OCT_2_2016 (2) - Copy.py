# Amazing Brick
# Oliver Zhang
# Sep 25 2016
"""
Features and problems history:

Sep 20 2016:
    Now uses pygame.update() calls only on changed portions of the screen and not the entire screen.

Sep 25 2016:
    Added level generation which creates new levels and deletes old ones continuously.
    Need to incorporate delta time to prevent temporal aliasing between frames.

Sep 25 2016 (2):
    Added brick including
    Added camera pan down when brick higher than half of screen
    Added delta time functionality making movement speed independent of refresh rate
    Need to make it run smoother
    Need to add effect when brick collides with obstacles - possibly explode
    and reverse velocities and add drag...?

Sep 30 2016:
    Added crude brick & shape collision detection using "approximating rect" around brick
    Now Handles collision/game over by expanding brick until it covers entire screen
    Need mathematically precise brick and shape collision

Oct 2 2016:
    Now handles brick and shape collision mathematically precisely, which plays much "cleaner".
    The algorithm first takes the AABB test of the brick and each shape, then checks if
    either of the line segments formed by the sides of the brick and shape intersect.
    Need to turn shapes into a list of dictionaries containing 'shape', 'colour', and 'passed' info.
"""
import pygame, sys
from random import randint, seed
from pygame import *

pygame.init()
width, height, = 800, 600
back_colour = (240, 240, 240)
game_over_colour = (255, 255, 255)
clock = pygame.time.Clock()
screen = display.set_mode((width, height))

level_sep = 400
level_height = 50
level_width = 200
level_margin = 150
block_size = 30
brick_size = 20
brick_side_speed = 0.09 # pixels * ms ^-1
brick_hit_speed = -0.6
brick_accel = 0.0013  # pixels * ms^-2

score = 0
game_started = False
game_over = False
prev_level_coords = (None, None)
level_list = []
colours = [(255, 100, 100), (106, 255, 30), (255,219,88), (0, 15, 137)]
shape_colour = (0, 15, 137)# (106, 255, 30)
brick = (brk_px, brk_py, brk_vx, brk_vy) = (width/2, height/2 + 1, 0.0, 0.0)
brick_colour = [0, 0, 0]
brick_collided = False


def add_to_shapes(shapes):
    level_list.append({"shapes": shapes, "colour": shape_colour, "passed": False})

def brick_pointlist(px, py, size):
    return [(px + size, py), (px, py - size), (px - size, py), (px, py + size)]

def get_sides(s):
    if type(s) == Rect:
        return ((s.topleft, s.topright), (s.topright, s.bottomright),
                (s.bottomright, s.bottomleft), (s.bottomleft, s.topleft))
    elif type(s) == list:
        return (s[0], s[1]), (s[1], s[2]), (s[2], s[3]), (s[3], s[0])

def do_lines_intersect(((ax1, ay1), (ax2, ay2)), ((bx1, by1), (bx2, by2))):
    """
    This function assumes line a to be vertical or horizontal,
    and that line b is diagonal (has slope 1 or -1)
    """
    # line a is vertical
    m = 1 if float(by1 - by2)/(bx1 - bx2) > 0 else -1 # m is slope of line b
    if ax1 == ax2:
        intx, inty = ax1, m * ax1 + by1 - m * bx1
        if (min(by1, by2) <= inty <= max(ay1, ay2) and min(ay1, ay2) <= inty <= max(by1, by2)
                and min(bx1, bx2) <= intx <= max(bx1, bx2)):
            return True
    # line a is horizontal
    else:
        intx, inty = (ay1 - by1 + m * bx1) / m, ay1
        if (min(bx1, bx2) <= intx <= max(ax1, ax2) and min(ax1, ax2) <= intx <= max(bx1, bx2)
                and min(by1, by2) <= inty <= max(by1, by2)):
            return True
    return False

def does_brick_collide(shape):
    # initial AABB
    px, py = int(brk_px), int(brk_py)
    if Rect(px - brick_size, py - brick_size, brick_size * 2, brick_size * 2).colliderect(shape):
        for shape_side in get_sides(shape):
            for brick_side in get_sides(brick_pointlist(px, py, brick_size)):
                if do_lines_intersect(shape_side, brick_side):
                    return True
    return False

def get_final_colour(colour):
    return [255 if channel == max(colour) else 220 for channel in colour]

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

    add_to_shapes([block1, block2, left_side, right_side])
    global prev_level_coords
    prev_level_coords = (hole_left, hole_right)


def init():
    hole_left = randint(level_margin, width - level_margin - level_width)
    hole_right = hole_left + level_width
    add_to_shapes([Rect(0, -level_height, hole_left, level_height), # left
                   Rect(hole_right, -level_height, width - hole_right, level_height)]) # right
    global prev_level_coords
    prev_level_coords = (hole_left, hole_right)

    screen.fill(back_colour)
    display.update()

def logic(dt):
    global brick_collided, brick_size, game_over, brick_colour, score
    if not game_started or game_over:
        return
    if not brick_collided:
        global brk_px, brk_py, brk_vy
        brk_vy += brick_accel * dt
        brk_px += brk_vx * dt
        brk_py += brk_vy * dt
    if brk_py <= height/2: # pans camera down
        camera_vy = -brk_vy if brk_vy < 0 else 0
        for level in level_list:
            for shape in level["shapes"]:
                shape.move_ip(0, camera_vy * dt)
        brk_py += camera_vy * dt
    for level in level_list:
        # removes shapes outside of screen
        level["shapes"][:] = [shape for shape in level["shapes"] if shape.top <= height]
    level_list[:] = [level for level in level_list if level["shapes"] != []]
    if level_list[-1]["shapes"][-1].bottom > 0:
        generate_level(prev_level_coords)

    if brk_px < brick_size or brk_px > width - brick_size or brk_py < brick_size or brk_py > height - brick_size:
        brick_collided = True
    if not brick_collided:
        for level in level_list:
            for shape in level["shapes"]:
                if does_brick_collide(shape):
                    brick_collided = True
            if level["shapes"][-1].bottom >= brk_py and not level["passed"]:
                level["passed"] = True
                score += 1


    if brick_collided:
        final_colour = get_final_colour(shape_colour)
        if brick_colour != final_colour:
            for ch in range(3):
                diff = final_colour[ch] - brick_colour[ch]
                if diff >= 20:
                    brick_colour[ch] += 20
                else:
                    brick_colour[ch] += diff
        elif brick_size < max(width - brk_px, brk_px) + max(height - brk_py, brk_py):
            brick_size += 0.007 * brick_size * dt
        else:
            game_over = True
            f = pygame.font.SysFont("segoeui", 32)
            screen.blit(f.render("Game Over", 1, (100, 100, 100)), Rect(200, 300, 100, 100))
            screen.blit(f.render(str(score), 1, (100, 100, 100)), Rect(width - 32, 0, 100, 32))
            display.update()


def events():
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            global brk_vy, brk_vx, game_started
            game_started = True if game_started == False else True
            if event.key == K_LEFT:
                brk_vx = -brick_side_speed
                brk_vy = brick_hit_speed
            if event.key == K_RIGHT:
                brk_vx = brick_side_speed
                brk_vy = brick_hit_speed


def render():
    if not game_over:
        screen.fill(back_colour)
        for level in level_list:
            for shape in level["shapes"]:
                draw.rect(screen, level["colour"], shape)
        draw.polygon(screen, brick_colour, brick_pointlist(brk_px, brk_py, brick_size))
        f = pygame.font.SysFont("segoeui", 32)
        screen.blit(f.render(str(score), 1, (100, 100, 100)), Rect(width - 32, 0, 100, 32))
        # updates = [shape.inflate(0, frame_movement * 2) for shape in shapes]
        # updates.append(Rect(0, height - frame_movement, width, frame_movement)) # bottom edge
        # display.update(updates)
        display.update()

seed(7)
init()
frame = 0
while True:
    dt = clock.tick(60)
    # if dt > 50:
        # dt = 0
    events()
    logic(dt)
    render()
    frame += 1
    # print frame

pygame.quit()
sys.exit()