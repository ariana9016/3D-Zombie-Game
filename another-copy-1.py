import random
import math
import time
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

player_pos = [0, 0, 0]
gun_rotation_y = 0
gun_rotation_x = 0
player_health = 10
player_score = 0
bullets_missed = 0
consecutive_kills = 0
total_kills = 0
cheat_mode_activated_once = False
game_over = False
is_night = False
player_bombs = 0

multi_shot_available = False
MULTI_SHOT_COUNT = 10
MULTI_SHOT_SPREAD = 15

boss_active = False
boss_zombie = None
boss_health = 25
BOSS_SIZE_FACTOR = 2.0

third_person_camera_pos = [300, 300, 400]
camera_height_offset = 0
camera_angle_offset = 0

cheat_mode_active = False

zombies = []
bullets = []
health_packs = []
dead_bodies = []
trees = []
bombs = []
explosions = []

GROUND_SIZE = 500
GROUND_HEIGHT = 0
GROUND_COLOR = (0.2, 0.4, 0.1)

sky_color = [0.1, 0.1, 0.3]
sky_color_target = [0.7, 0.8, 1.0]
sky_color_speed = 0.0005
sky_to_dark = False

NUM_ZOMBIES_DAY = 5
NUM_ZOMBIES_NIGHT = 8
NUM_ZOMBIES = NUM_ZOMBIES_DAY
ZOMBIE_SPEED = 0.2
BOSS_ZOMBIE_SPEED = 0.15
BULLET_SPEED = 25
COLLISION_DAMAGE_ZOMBIE = 1
COLLISION_DAMAGE_BOSS = 3
HEALTH_GAIN_PACK = 2
CONSECUTIVE_KILLS_FOR_CHEAT = 5
KILLS_FOR_BOSS = 10

NUM_HEALTH_PACKS = 3
HEALTH_PACK_SIZE = 20

ZOMBIE_SCALE_SPEED = 0.015
ZOMBIE_SCALE_MIN = 0.7
ZOMBIE_SCALE_MAX = 1.3

HUMAN_BODY_HEIGHT = 60
HUMAN_BODY_WIDTH = 20
HUMAN_BODY_DEPTH = 15
HUMAN_LIMB_THICKNESS = 8

ZOMBIE_BODY_HEIGHT = 70
ZOMBIE_BODY_WIDTH = 25
ZOMBIE_BODY_DEPTH = 20
ZOMBIE_LIMB_THICKNESS = 10
BULLET_SIZE = 10
PLAYER_COLLISION_SIZE = HUMAN_BODY_WIDTH * 0.8

DEAD_BODY_SIZE_FACTOR = 0.8
BLOOD_COLOR = (0.5, 0.0, 0.0)
DEAD_BODY_COLLISION_SIZE = ZOMBIE_BODY_WIDTH * DEAD_BODY_SIZE_FACTOR

TREE_TRUNK_COLOR = (0.5, 0.35, 0.0)
TREE_LEAF_COLOR = (0.1, 0.5, 0.1)
TREE_SIZE = 80
NUM_TREES = 10
TREE_COLLISION_SIZE = TREE_SIZE * 0.3

NUM_BOMBS = 2
BOMB_SIZE = 15
BOMB_EXPLOSION_RADIUS = 150
BOMB_EXPLOSION_DURATION = 30
BOMB_DAMAGE_ZOMBIE = 5
BOMB_DAMAGE_BOSS = 5


def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18, color=(1, 1, 1)):
    glColor3f(*color)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()

    gluOrtho2D(0, 1000, 0, 800)

    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))

    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def draw_cube(size, color):
    glColor3f(*color)
    glutSolidCube(size)

def draw_sphere(radius, color):
    glColor3f(*color)
    gluSphere(gluNewQuadric(), radius, 15, 15)

def draw_cylinder(base_radius, top_radius, height, color):
    glColor3f(*color)
    gluCylinder(gluNewQuadric(), base_radius, top_radius, height, 15, 15)

def draw_human_player(x, y, z):
    glPushMatrix()
    glTranslatef(x, y, z)

    if game_over:
        glRotatef(90, 1, 0, 0)

    glRotatef(gun_rotation_y, 0, 0, 1)

    glPushMatrix()
    glColor3f(0.1, 0.1, 0.5)
    glScalef(HUMAN_BODY_WIDTH, HUMAN_BODY_DEPTH, HUMAN_BODY_HEIGHT)
    glutSolidCube(1)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0, 0, HUMAN_BODY_HEIGHT * 0.6)
    glColor3f(0.9, 0.7, 0.6)
    draw_sphere(HUMAN_BODY_WIDTH * 0.5, (0.9, 0.7, 0.6))
    glPopMatrix()

    glPushMatrix()
    glTranslatef(-HUMAN_BODY_WIDTH * 0.3, 0, -HUMAN_BODY_HEIGHT * 0.5)
    glColor3f(0.1, 0.1, 0.5)
    glRotatef(90, 1, 0, 0)
    draw_cylinder(HUMAN_LIMB_THICKNESS * 0.5, HUMAN_LIMB_THICKNESS * 0.5, HUMAN_BODY_HEIGHT * 0.4, (0.1, 0.1, 0.5))
    glPopMatrix()

    glPushMatrix()
    glTranslatef(HUMAN_BODY_WIDTH * 0.3, 0, -HUMAN_BODY_HEIGHT * 0.5)
    glColor3f(0.1, 0.1, 0.5)
    glRotatef(90, 1, 0, 0)
    draw_cylinder(HUMAN_LIMB_THICKNESS * 0.5, HUMAN_LIMB_THICKNESS * 0.5, HUMAN_BODY_HEIGHT * 0.4, (0.1, 0.1, 0.5))
    glPopMatrix()

    glPushMatrix()
    glTranslatef(-HUMAN_BODY_WIDTH * 0.4, HUMAN_BODY_DEPTH * 0.4, HUMAN_BODY_HEIGHT * 0.2)
    glColor3f(0.9, 0.7, 0.6)
    glRotatef(-90, 1, 0, 0)
    draw_cylinder(HUMAN_LIMB_THICKNESS * 0.4, HUMAN_LIMB_THICKNESS * 0.4, HUMAN_BODY_WIDTH * 1.2, (0.9, 0.7, 0.6))
    glPopMatrix()

    glPushMatrix()
    glTranslatef(HUMAN_BODY_WIDTH * 0.4, HUMAN_BODY_DEPTH * 0.4, HUMAN_BODY_HEIGHT * 0.2)
    glColor3f(0.9, 0.7, 0.6)
    glRotatef(-90, 1, 0, 0)
    draw_cylinder(HUMAN_LIMB_THICKNESS * 0.4, HUMAN_LIMB_THICKNESS * 0.4, HUMAN_BODY_WIDTH * 1.2, (0.9, 0.7, 0.6))
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0, HUMAN_BODY_DEPTH * 0.8, HUMAN_BODY_HEIGHT * 0.1)
    glColor3f(0.3, 0.3, 0.3)
    glScalef(HUMAN_BODY_WIDTH * 0.2, HUMAN_BODY_DEPTH * 0.8, HUMAN_BODY_HEIGHT * 0.15)
    glutSolidCube(1)
    glPopMatrix()

    glPopMatrix()

def draw_zombie(x, y, z, hand_asymmetry_factor, scale_factor, is_boss=False, boss_health=25):
    glPushMatrix()
    glTranslatef(x, y, z)

    arm_scale_modifier = 1.0
    if is_boss:
        edge_distance_x = min(GROUND_SIZE - abs(x), GROUND_SIZE + x if x < 0 else GROUND_SIZE - x)
        edge_distance_y = min(GROUND_SIZE - abs(y), GROUND_SIZE + y if y < 0 else GROUND_SIZE - y)
        min_edge_distance = min(edge_distance_x, edge_distance_y)

        if min_edge_distance < ZOMBIE_BODY_WIDTH * BOSS_SIZE_FACTOR * 2.0:
            arm_scale_modifier = 0.5

    if is_boss:
        glScalef(BOSS_SIZE_FACTOR, BOSS_SIZE_FACTOR, BOSS_SIZE_FACTOR)
    else:
        glScalef(scale_factor, scale_factor, scale_factor)

    glPushMatrix()
    if is_boss:
        glColor3f(0.5, 0.1, 0.1)
    else:
        glColor3f(0.6, 0.4, 0.2)
    glScalef(ZOMBIE_BODY_WIDTH, ZOMBIE_BODY_DEPTH, ZOMBIE_BODY_HEIGHT)
    glutSolidCube(1)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0, 0, ZOMBIE_BODY_HEIGHT * 0.6)

    if is_boss:
        glColor3f(0.8, 0.1, 0.1)
        glutSolidSphere(ZOMBIE_BODY_WIDTH * 0.4, 12, 12)

        glPushMatrix()
        glTranslatef(-ZOMBIE_BODY_WIDTH * 0.2, ZOMBIE_BODY_DEPTH * 0.3, 0)
        glColor3f(1.0, 1.0, 0.0)
        glutSolidSphere(ZOMBIE_BODY_WIDTH * 0.1, 8, 8)
        glPopMatrix()

        glPushMatrix()
        glTranslatef(ZOMBIE_BODY_WIDTH * 0.2, ZOMBIE_BODY_DEPTH * 0.3, 0)
        glColor3f(1.0, 1.0, 0.0)
        glutSolidSphere(ZOMBIE_BODY_WIDTH * 0.1, 8, 8)
        glPopMatrix()
    else:
        glColor3f(0.8, 0.2, 0.2)
        glBegin(GL_TRIANGLES)
        glVertex3f(-ZOMBIE_BODY_WIDTH * 0.4, -ZOMBIE_BODY_DEPTH * 0.4, 0)
        glVertex3f(ZOMBIE_BODY_WIDTH * 0.4, -ZOMBIE_BODY_DEPTH * 0.4, 0)
        glVertex3f(0, ZOMBIE_BODY_DEPTH * 0.4, 0)

        glVertex3f(-ZOMBIE_BODY_WIDTH * 0.4, -ZOMBIE_BODY_DEPTH * 0.4, 0)
        glVertex3f(0, ZOMBIE_BODY_DEPTH * 0.4, 0)
        glVertex3f(0, 0, ZOMBIE_BODY_HEIGHT * 0.2)

        glVertex3f(ZOMBIE_BODY_WIDTH * 0.4, -ZOMBIE_BODY_DEPTH * 0.4, 0)
        glVertex3f(-ZOMBIE_BODY_WIDTH * 0.4, -ZOMBIE_BODY_DEPTH * 0.4, 0)
        glVertex3f(0, 0, ZOMBIE_BODY_HEIGHT * 0.2)

        glVertex3f(0, ZOMBIE_BODY_DEPTH * 0.4, 0)
        glVertex3f(ZOMBIE_BODY_WIDTH * 0.4, -ZOMBIE_BODY_DEPTH * 0.4, 0)
        glVertex3f(0, 0, ZOMBIE_BODY_HEIGHT * 0.2)

        glEnd()

    glPopMatrix()

    glPushMatrix()
    glTranslatef(-ZOMBIE_BODY_WIDTH * 0.35, 0, -ZOMBIE_BODY_HEIGHT * 0.5)
    if is_boss:
        glColor3f(0.4, 0.1, 0.1)
    else:
        glColor3f(0.2, 0.1, 0.05)
    glRotatef(90, 1, 0, 0)
    draw_cylinder(ZOMBIE_LIMB_THICKNESS * 0.6, ZOMBIE_LIMB_THICKNESS * 0.6, ZOMBIE_BODY_HEIGHT * 0.45,
                 (0.4, 0.1, 0.1) if is_boss else (0.2, 0.1, 0.05))
    glPopMatrix()

    glPushMatrix()
    glTranslatef(ZOMBIE_BODY_WIDTH * 0.35, 0, -ZOMBIE_BODY_HEIGHT * 0.5)
    if is_boss:
        glColor3f(0.4, 0.1, 0.1)
    else:
        glColor3f(0.2, 0.1, 0.05)
    glRotatef(90, 1, 0, 0)
    draw_cylinder(ZOMBIE_LIMB_THICKNESS * 0.6, ZOMBIE_LIMB_THICKNESS * 0.6, ZOMBIE_BODY_HEIGHT * 0.45,
                 (0.4, 0.1, 0.1) if is_boss else (0.2, 0.1, 0.05))
    glPopMatrix()

    glPushMatrix()
    glTranslatef(-ZOMBIE_BODY_WIDTH * 0.6, 0, ZOMBIE_BODY_HEIGHT * 0.2)
    if is_boss:
        glColor3f(0.6, 0.1, 0.1)
    else:
        glColor3f(0.4, 0.3, 0.1)

    if is_boss and boss_health <= 5:
        glRotatef(130, 1, 0, 0)
    else:
        glRotatef(90, 1, 0, 0)

    asymmetry = hand_asymmetry_factor if not is_boss else 1.0
    arm_length = ZOMBIE_BODY_HEIGHT * 0.4 * asymmetry * arm_scale_modifier
    draw_cylinder(ZOMBIE_LIMB_THICKNESS * 0.6, ZOMBIE_LIMB_THICKNESS * 0.6, arm_length,
                 (0.6, 0.1, 0.1) if is_boss else (0.4, 0.3, 0.1))
    glPopMatrix()

    glPushMatrix()
    glTranslatef(ZOMBIE_BODY_WIDTH * 0.6, 0, ZOMBIE_BODY_HEIGHT * 0.2)
    if is_boss:
        glColor3f(0.6, 0.1, 0.1)
    else:
        glColor3f(0.4, 0.3, 0.1)

    if is_boss and boss_health <= 5:
        glRotatef(130, 1, 0, 0)
    else:
        glRotatef(90, 1, 0, 0)

    inverse_asymmetry = (2 - hand_asymmetry_factor) if not is_boss else 1.0
    arm_length = ZOMBIE_BODY_HEIGHT * 0.4 * inverse_asymmetry * arm_scale_modifier
    draw_cylinder(ZOMBIE_LIMB_THICKNESS * 0.6, ZOMBIE_LIMB_THICKNESS * 0.6, arm_length,
                 (0.6, 0.1, 0.1) if is_boss else (0.4, 0.3, 0.1))
    glPopMatrix()

    glPopMatrix()

def draw_bullet(x, y, z):
    """Draws a bullet (cube) at the specified position."""
    # Add a check for invalid coordinates
    if math.isnan(x) or math.isnan(y) or math.isnan(z) or \
       math.isinf(x) or math.isinf(y) or math.isinf(z):
        print(f"Skipping drawing bullet with invalid coordinates: x={x}, y={y}, z={z}")
        return # Skip drawing if coordinates are invalid

    glPushMatrix()
    glTranslatef(x, y, z)
    draw_cube(BULLET_SIZE, (1, 1, 0))
    glPopMatrix()

def draw_health_pack(x, y, z):
    glPushMatrix()
    glTranslatef(x, y, z + HEALTH_PACK_SIZE / 2)

    glColor3f(1.0, 0.0, 0.0)
    glutSolidCube(HEALTH_PACK_SIZE)

    plus_thickness = HEALTH_PACK_SIZE * 0.2
    plus_length = HEALTH_PACK_SIZE * 0.8

    glPushMatrix()
    glColor3f(1.0, 1.0, 1.0)
    glScalef(plus_length, plus_thickness, plus_thickness)
    glutSolidCube(1.0)
    glPopMatrix()

    glPushMatrix()
    glColor3f(1.0, 1.0, 1.0)
    glScalef(plus_thickness, plus_length, plus_thickness)
    glutSolidCube(1.0)
    glPopMatrix()

    glPopMatrix()

def draw_human_dead_body(x, y, z, rotation_y):
    glPushMatrix()
    glTranslatef(x, y, z)
    glRotatef(rotation_y, 0, 0, 1)
    glRotatef(90, 1, 0, 0)

    glPushMatrix()
    glColor3f(0.1 * DEAD_BODY_SIZE_FACTOR, 0.1 * DEAD_BODY_SIZE_FACTOR, 0.5 * DEAD_BODY_SIZE_FACTOR)
    glScalef(HUMAN_BODY_WIDTH * DEAD_BODY_SIZE_FACTOR, HUMAN_BODY_DEPTH * DEAD_BODY_SIZE_FACTOR, HUMAN_BODY_HEIGHT * DEAD_BODY_SIZE_FACTOR * 0.3)
    glutSolidCube(1)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0, 0, HUMAN_BODY_HEIGHT * DEAD_BODY_SIZE_FACTOR * 0.15)
    glColor3f(0.9 * DEAD_BODY_SIZE_FACTOR, 0.7 * DEAD_BODY_SIZE_FACTOR, 0.6 * DEAD_BODY_SIZE_FACTOR)
    glScalef(1.0, 1.0, 0.5)
    draw_sphere(HUMAN_BODY_WIDTH * DEAD_BODY_SIZE_FACTOR * 0.5, (0.9 * DEAD_BODY_SIZE_FACTOR, 0.7 * DEAD_BODY_SIZE_FACTOR, 0.6 * DEAD_BODY_SIZE_FACTOR))
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0, 0, 0.1)
    glColor3f(*BLOOD_COLOR)
    glScalef(1.5, 1.5, 0.1)
    draw_cylinder(HUMAN_BODY_WIDTH * DEAD_BODY_SIZE_FACTOR * 0.8, HUMAN_BODY_WIDTH * DEAD_BODY_SIZE_FACTOR * 0.8, 1.0, BLOOD_COLOR)
    glPopMatrix()

    glPopMatrix()

def draw_tree(x, y, z):
    glPushMatrix()
    glTranslatef(x, y, z)

    glPushMatrix()
    glColor3f(*TREE_TRUNK_COLOR)
    glRotatef(-90, 1, 0, 0)
    draw_cylinder(TREE_SIZE * 0.1, TREE_SIZE * 0.1, TREE_SIZE * 0.8, TREE_TRUNK_COLOR)
    glPopMatrix()

    glPushMatrix()
    glColor3f(*TREE_LEAF_COLOR)
    glTranslatef(0, 0, TREE_SIZE * 0.8)
    draw_sphere(TREE_SIZE * 0.5, TREE_LEAF_COLOR)
    glPopMatrix()

    glPopMatrix()

def draw_bomb(x, y, z):
    glPushMatrix()
    glTranslatef(x, y, z + BOMB_SIZE / 2)

    glColor3f(0.1, 0.1, 0.1)
    glutSolidSphere(BOMB_SIZE, 15, 15)

    glPushMatrix()
    glTranslatef(0, 0, BOMB_SIZE * 0.8)
    glColor3f(0.5, 0.3, 0.0)
    glRotatef(-90, 1, 0, 0)
    draw_cylinder(BOMB_SIZE * 0.1, BOMB_SIZE * 0.1, BOMB_SIZE * 0.5, (0.5, 0.3, 0.0))

    glTranslatef(0, 0, BOMB_SIZE * 0.5)
    glColor3f(1.0, 0.3, 0.0)
    glutSolidSphere(BOMB_SIZE * 0.15, 8, 8)
    glPopMatrix()

    glPopMatrix()

def draw_explosion(x, y, z, radius, time_remaining):
    glPushMatrix()
    glTranslatef(x, y, z)

    intensity = time_remaining / BOMB_EXPLOSION_DURATION
    glColor3f(1.0, 0.5 * intensity, 0.0)

    factor = 1.0 - (time_remaining / BOMB_EXPLOSION_DURATION * 0.5)
    glutSolidSphere(radius * factor, 20, 20)

    glPopMatrix()

def generate_bombs():
    global bombs
    bombs = []

    for _ in range(NUM_BOMBS):
        x = random.uniform(-GROUND_SIZE + BOMB_SIZE, GROUND_SIZE - BOMB_SIZE)
        y = random.uniform(-GROUND_SIZE + BOMB_SIZE, GROUND_SIZE - BOMB_SIZE)
        z = GROUND_HEIGHT

        too_close = True
        while too_close:
            too_close = False
            if math.dist([x, y, z], player_pos) < 100:
                too_close = True
            else:
                for pack in health_packs:
                    if math.dist([x, y, z], pack) < HEALTH_PACK_SIZE * 3:
                        too_close = True
                        break
                for bomb in bombs:
                    if math.dist([x, y, z], bomb) < BOMB_SIZE * 3:
                        too_close = True
                        break
            if too_close:
                x = random.uniform(-GROUND_SIZE + BOMB_SIZE, GROUND_SIZE - BOMB_SIZE)
                y = random.uniform(-GROUND_SIZE + BOMB_SIZE, GROUND_SIZE - BOMB_SIZE)

        bombs.append([x, y, z])

def detonate_bomb():
    global player_bombs, explosions, zombies, boss_health, boss_active, boss_zombie
    global player_score, consecutive_kills, total_kills, NUM_ZOMBIES

    if player_bombs <= 0 or game_over:
        return

    player_bombs -= 1

    explosions.append([player_pos[0], player_pos[1], player_pos[2], BOMB_EXPLOSION_RADIUS, BOMB_EXPLOSION_DURATION])

    new_zombies = []
    for zombie in zombies:
        dist = math.dist(zombie[:3], player_pos)
        if dist <= BOMB_EXPLOSION_RADIUS:
            dead_bodies.append([zombie[0], zombie[1], GROUND_HEIGHT, random.uniform(0, 360)])
            player_score += 5
            total_kills += 1
        else:
            new_zombies.append(zombie)

    zombies = new_zombies

    if boss_active and boss_zombie:
        dist = math.dist(boss_zombie[:3], player_pos)
        if dist <= BOMB_EXPLOSION_RADIUS:
            boss_health -= BOMB_DAMAGE_BOSS
            player_score += 20

            if boss_health <= 0:
                player_score += 100
                consecutive_kills += 3
                total_kills += 1
                print("Boss defeated by bomb! +100 points!")

                dead_bodies.append([boss_zombie[0], boss_zombie[1], GROUND_HEIGHT, random.uniform(0, 360)])

                boss_active = False
                boss_zombie = None

                boss_health = 25

                NUM_ZOMBIES += 3
                for _ in range(3):
                    x = random.uniform(-GROUND_SIZE * 0.8, GROUND_SIZE * 0.8)
                    y = random.uniform(-GROUND_SIZE * 0.8, GROUND_SIZE * 0.8)
                    z = GROUND_HEIGHT

                    while math.dist([x, y, z], player_pos) < 150:
                        x = random.uniform(-GROUND_SIZE * 0.8, GROUND_SIZE * 0.8)
                        y = random.uniform(-GROUND_SIZE * 0.8, GROUND_SIZE * 0.8)

                    hand_asymmetry_factor = random.uniform(0.7, 1.3)
                    scale_factor = random.uniform(ZOMBIE_SCALE_MIN, ZOMBIE_SCALE_MAX)
                    scale_direction = 1 if random.random() > 0.5 else -1

                    zombies.append([x, y, z, hand_asymmetry_factor, scale_factor, scale_direction])

                print(f"Boss defeat triggered 3 new zombies! Total zombies now: {len(zombies)}")

    print(f"Bomb detonated! {player_bombs} bombs remaining.")

def generate_zombies():
    global zombies
    zombies = []

    for _ in range(NUM_ZOMBIES):
        x = random.uniform(-GROUND_SIZE + ZOMBIE_BODY_WIDTH, GROUND_SIZE - ZOMBIE_BODY_WIDTH)
        y = random.uniform(-GROUND_SIZE + ZOMBIE_BODY_WIDTH, GROUND_SIZE - ZOMBIE_BODY_WIDTH)
        z = GROUND_HEIGHT

        while math.dist([x, y, z], player_pos) < 150:
             x = random.uniform(-GROUND_SIZE + ZOMBIE_BODY_WIDTH, GROUND_SIZE - ZOMBIE_BODY_WIDTH)
             y = random.uniform(-GROUND_SIZE + ZOMBIE_BODY_WIDTH, GROUND_SIZE - ZOMBIE_BODY_WIDTH)

        hand_asymmetry_factor = random.uniform(0.7, 1.3)
        scale_factor = random.uniform(ZOMBIE_SCALE_MIN, ZOMBIE_SCALE_MAX)
        scale_direction = 1 if random.random() > 0.5 else -1

        zombies.append([x, y, z, hand_asymmetry_factor, scale_factor, scale_direction])

def generate_health_packs():
    global health_packs
    health_packs = []

    for _ in range(NUM_HEALTH_PACKS):
        x = random.uniform(-GROUND_SIZE + HEALTH_PACK_SIZE, GROUND_SIZE - HEALTH_PACK_SIZE)
        y = random.uniform(-GROUND_SIZE + HEALTH_PACK_SIZE, GROUND_SIZE - HEALTH_PACK_SIZE)
        z = GROUND_HEIGHT

        too_close = True
        while too_close:
            too_close = False
            if math.dist([x, y, z], player_pos) < 100:
                too_close = True
            else:
                for pack in health_packs:
                    if math.dist([x, y, z], pack) < HEALTH_PACK_SIZE * 2:
                        too_close = True
                        break
                for bomb in bombs:
                    if math.dist([x, y, z], bomb) < BOMB_SIZE * 3:
                        too_close = True
                        break
            if too_close:
                x = random.uniform(-GROUND_SIZE + HEALTH_PACK_SIZE, GROUND_SIZE - HEALTH_PACK_SIZE)
                y = random.uniform(-GROUND_SIZE + HEALTH_PACK_SIZE, GROUND_SIZE - HEALTH_PACK_SIZE)

        health_packs.append([x, y, z])

def generate_trees():
    global trees
    trees = []

    for _ in range(NUM_TREES):
        x = random.uniform(-GROUND_SIZE + TREE_SIZE, GROUND_SIZE - TREE_SIZE)
        y = random.uniform(-GROUND_SIZE + TREE_SIZE, GROUND_SIZE - TREE_SIZE)
        z = GROUND_HEIGHT

        too_close = True
        while too_close:
            too_close = False
            if math.dist([x, y, z], player_pos) < 200:
                too_close = True
            else:
                for tree in trees:
                    if math.dist([x, y, z], tree) < TREE_SIZE * 1.5:
                        too_close = True
                        break
            if too_close:
                x = random.uniform(-GROUND_SIZE + TREE_SIZE, GROUND_SIZE - TREE_SIZE)
                y = random.uniform(-GROUND_SIZE + TREE_SIZE, GROUND_SIZE - TREE_SIZE)

        trees.append([x, y, z])

def draw_ground():
    glBegin(GL_QUADS)
    glColor3f(*GROUND_COLOR)
    glVertex3f(-GROUND_SIZE, -GROUND_SIZE, GROUND_HEIGHT)
    glVertex3f(GROUND_SIZE, -GROUND_SIZE, GROUND_HEIGHT)
    glVertex3f(GROUND_SIZE, GROUND_SIZE, GROUND_HEIGHT)
    glVertex3f(-GROUND_SIZE, GROUND_SIZE, GROUND_HEIGHT)
    glEnd()

def draw_game_objects():
    for zombie in zombies:
        draw_zombie(zombie[0], zombie[1], zombie[2], zombie[3], zombie[4])

    if boss_active and boss_zombie:
        draw_zombie(boss_zombie[0], boss_zombie[1], boss_zombie[2], boss_zombie[3], boss_zombie[4], is_boss=True, boss_health=boss_health)

        if boss_health > 0:
            glPushMatrix()
            glTranslatef(boss_zombie[0], boss_zombie[1], boss_zombie[2] + ZOMBIE_BODY_HEIGHT * BOSS_SIZE_FACTOR * 1.5)

            glColor3f(0.0, 0.0, 0.0)
            glScalef(ZOMBIE_BODY_WIDTH * BOSS_SIZE_FACTOR * 1.5, 10, 5)
            glutSolidCube(1)

            glTranslatef(-(ZOMBIE_BODY_WIDTH * BOSS_SIZE_FACTOR * 1.5 * (1 - boss_health/25))/2, 0, 0.1)
            glColor3f(1.0, 0.0, 0.0)
            glScalef(boss_health/25, 0.8, 1)
            glutSolidCube(1)

            glPopMatrix()

    for bullet in bullets:
        draw_bullet(bullet[0], bullet[1], bullet[2])

    for pack in health_packs:
        draw_health_pack(pack[0], pack[1], pack[2])

    for bomb in bombs:
        draw_bomb(bomb[0], bomb[1], bomb[2])

    for explosion in explosions:
        draw_explosion(explosion[0], explosion[1], explosion[2], explosion[3], explosion[4])

    for body in dead_bodies:
        draw_human_dead_body(body[0], body[1], body[2], body[3])

    for tree in trees:
        draw_tree(tree[0], tree[1], tree[2])

def update_objects():
    global zombies, bullets, game_over, boss_active, boss_zombie, boss_health
    global sky_color, sky_color_target, sky_color_speed, sky_to_dark
    global is_night, NUM_ZOMBIES, total_kills
    global explosions, bombs

    old_is_night = is_night
    is_night = sky_color[0] < 0.3 and sky_color[1] < 0.4 and sky_color[2] < 0.5

    if is_night and not old_is_night:
        NUM_ZOMBIES = NUM_ZOMBIES_NIGHT
        print("Night has fallen! More zombies are appearing.")
    elif not is_night and old_is_night:
        NUM_ZOMBIES = NUM_ZOMBIES_DAY
        print("Dawn breaks! Fewer zombies now.")

    if is_night and total_kills >= KILLS_FOR_BOSS and not boss_active:
        spawn_boss_zombie()
        print("WARNING: A powerful boss zombie has appeared!")

    new_zombies = []
    for zombie in zombies:
        dir_x = player_pos[0] - zombie[0]
        dir_y = player_pos[1] - zombie[1]
        dir_z = player_pos[2] - zombie[2]
        dist = math.dist(zombie[:3], player_pos)
        move_speed = ZOMBIE_SPEED
        if dist > move_speed:
            new_x = zombie[0] + dir_x / dist * move_speed
            new_y = zombie[1] + dir_y / dist * move_speed
            new_z = zombie[2] + dir_z / dist * move_speed

            new_x = max(-GROUND_SIZE + ZOMBIE_BODY_WIDTH, min(GROUND_SIZE - ZOMBIE_BODY_WIDTH, new_x))
            new_y = max(-GROUND_SIZE + ZOMBIE_BODY_WIDTH, min(GROUND_SIZE - ZOMBIE_BODY_WIDTH, new_y))

            zombie[0] = new_x
            zombie[1] = new_y
            zombie[2] = new_z
        else:
             pass
        new_zombies.append(zombie)

    zombies = new_zombies

    for zombie in zombies:
        zombie[4] += zombie[5] * ZOMBIE_SCALE_SPEED
        if zombie[4] > ZOMBIE_SCALE_MAX:
            zombie[5] = -1
        elif zombie[4] < ZOMBIE_SCALE_MIN:
            zombie[5] = 1

    if boss_active and boss_zombie:
        dir_x = player_pos[0] - boss_zombie[0]
        dir_y = player_pos[1] - boss_zombie[1]
        dir_z = player_pos[2] - boss_zombie[2]
        dist = math.dist(boss_zombie[:3], player_pos)
        if dist > BOSS_ZOMBIE_SPEED:
            new_x = boss_zombie[0] + dir_x / dist * BOSS_ZOMBIE_SPEED
            new_y = boss_zombie[1] + dir_y / dist * BOSS_ZOMBIE_SPEED
            new_z = boss_zombie[2] + dir_z / dist * BOSS_ZOMBIE_SPEED

            boss_margin = ZOMBIE_BODY_WIDTH * BOSS_SIZE_FACTOR * 2.0
            new_x = max(-GROUND_SIZE + boss_margin, min(GROUND_SIZE - boss_margin, new_x))
            new_y = max(-GROUND_SIZE + boss_margin, min(GROUND_SIZE - boss_margin, new_y))

            boss_zombie[0] = new_x
            boss_zombie[1] = new_y
            boss_zombie[2] = new_z

        boss_zombie[4] += boss_zombie[5] * ZOMBIE_SCALE_SPEED * 0.5
        if boss_zombie[4] > ZOMBIE_SCALE_MAX:
            boss_zombie[5] = -1
        elif boss_zombie[4] < ZOMBIE_SCALE_MIN:
            boss_zombie[5] = 1

    new_bullets = []
    for bullet in bullets:
        new_x = bullet[0] + bullet[3] * BULLET_SPEED
        new_y = bullet[1] + bullet[4] * BULLET_SPEED
        new_z = bullet[2] + bullet[5] * BULLET_SPEED

        if abs(new_x) > GROUND_SIZE:
            pass
        elif abs(new_y) > GROUND_SIZE:
            pass
        elif new_z < GROUND_HEIGHT or new_z > 500:
            pass
        else:
            bullet[0] = new_x
            bullet[1] = new_y
            bullet[2] = new_z
            new_bullets.append(bullet)
    bullets = new_bullets

    while len(zombies) < NUM_ZOMBIES:
        x = random.uniform(-GROUND_SIZE + ZOMBIE_BODY_WIDTH, GROUND_SIZE - ZOMBIE_BODY_WIDTH)
        y = random.uniform(-GROUND_SIZE + ZOMBIE_BODY_WIDTH, GROUND_SIZE - ZOMBIE_BODY_WIDTH)
        z = GROUND_HEIGHT

        while math.dist([x, y, z], player_pos) < 150:
             x = random.uniform(-GROUND_SIZE + ZOMBIE_BODY_WIDTH, GROUND_SIZE - ZOMBIE_BODY_WIDTH)
             y = random.uniform(-GROUND_SIZE + ZOMBIE_BODY_WIDTH, GROUND_SIZE - ZOMBIE_BODY_WIDTH)

        hand_asymmetry_factor = random.uniform(0.7, 1.3)
        scale_factor = random.uniform(ZOMBIE_SCALE_MIN, ZOMBIE_SCALE_MAX)
        scale_direction = 1 if random.random() > 0.5 else -1

        zombies.append([x, y, z, hand_asymmetry_factor, scale_factor, scale_direction])
        print(f"Spawned a new zombie. Total zombies: {len(zombies)}")

    current_target = sky_color_target if not sky_to_dark else [0.1, 0.1, 0.3]
    transition_complete = True

    for i in range(3):
        if abs(sky_color[i] - current_target[i]) > sky_color_speed:
            if sky_color[i] < current_target[i]:
                sky_color[i] += sky_color_speed
                transition_complete = False
            elif sky_color[i] > current_target[i]:
                sky_color[i] -= sky_color_speed
                transition_complete = False

    if transition_complete:
        sky_to_dark = not sky_to_dark
        time.sleep(0.01)

    new_explosions = []
    for explosion in explosions:
        explosion[4] -= 1
        if explosion[4] > 0:
            new_explosions.append(explosion)
    explosions = new_explosions

    while len(bombs) < NUM_BOMBS:
        x = random.uniform(-GROUND_SIZE + BOMB_SIZE, GROUND_SIZE - BOMB_SIZE)
        y = random.uniform(-GROUND_SIZE + BOMB_SIZE, GROUND_SIZE - BOMB_SIZE)
        z = GROUND_HEIGHT

        too_close = True
        while too_close:
            too_close = False
            if math.dist([x, y, z], player_pos) < 100:
                too_close = True
            else:
                for pack in health_packs:
                    if math.dist([x, y, z], pack) < HEALTH_PACK_SIZE * 3:
                        too_close = True
                        break
                for bomb in bombs:
                    if math.dist([x, y, z], bomb) < BOMB_SIZE * 3:
                        too_close = True
                        break
            if too_close:
                x = random.uniform(-GROUND_SIZE + BOMB_SIZE, GROUND_SIZE - BOMB_SIZE)
                y = random.uniform(-GROUND_SIZE + BOMB_SIZE, GROUND_SIZE - BOMB_SIZE)

        bombs.append([x, y, z])
        print(f"Spawned a new bomb. Total bombs: {len(bombs)}")


def check_collisions():
    global player_health, player_score, consecutive_kills, total_kills, cheat_mode_active, game_over, bullets_missed
    global cheat_mode_activated_once, multi_shot_available, boss_active, boss_zombie, boss_health, NUM_ZOMBIES
    global zombies, bullets, health_packs, dead_bodies, player_bombs, bombs

    def is_colliding(obj1_pos, obj1_size, obj2_pos, obj2_size):
        distance = math.dist(obj1_pos, obj2_pos)
        return distance < (obj1_size / 2 + obj2_size / 2)

    player_collision_pos = player_pos

    if boss_active and boss_zombie:
        new_bullets = []
        boss_hit = False
        boss_size = ZOMBIE_BODY_WIDTH * BOSS_SIZE_FACTOR

        for bullet in bullets:
            if is_colliding(bullet[:3], BULLET_SIZE, boss_zombie[:3], boss_size):
                boss_health -= 1
                boss_hit = True
                player_score += 5
                print(f"Boss hit! Health remaining: {boss_health}")

                if boss_health <= 0:
                    player_score += 100
                    consecutive_kills += 3
                    total_kills += 1
                    print("Boss defeated! +100 points!")

                    dead_bodies.append([boss_zombie[0], boss_zombie[1], GROUND_HEIGHT, random.uniform(0, 360)])

                    boss_active = False
                    boss_zombie = None

                    boss_health = 25

                    NUM_ZOMBIES += 3
                    for _ in range(3):
                        x = random.uniform(-GROUND_SIZE * 0.8, GROUND_SIZE * 0.8)
                        y = random.uniform(-GROUND_SIZE * 0.8, GROUND_SIZE * 0.8)
                        z = GROUND_HEIGHT

                        while math.dist([x, y, z], player_pos) < 150:
                            x = random.uniform(-GROUND_SIZE * 0.8, GROUND_SIZE * 0.8)
                            y = random.uniform(-GROUND_SIZE * 0.8, GROUND_SIZE * 0.8)

                        hand_asymmetry_factor = random.uniform(0.7, 1.3)
                        scale_factor = random.uniform(ZOMBIE_SCALE_MIN, ZOMBIE_SCALE_MAX)
                        scale_direction = 1 if random.random() > 0.5 else -1

                        zombies.append([x, y, z, hand_asymmetry_factor, scale_factor, scale_direction])

                    print(f"Boss defeat triggered 3 new zombies! Total zombies now: {len(zombies)}")
                else:
                    new_bullets.append(bullet)
            else:
                new_bullets.append(bullet)

        if boss_hit:
            bullets = new_bullets

    new_bullets = []
    hit_zombies = []
    for bullet in bullets:
        hit_zombie = False
        for i, zombie in enumerate(zombies):
            if is_colliding(bullet[:3], BULLET_SIZE, zombie[:3], ZOMBIE_BODY_WIDTH):
                player_score += 10
                consecutive_kills += 1
                total_kills += 1
                print(f"Zombie hit! Consecutive kills: {consecutive_kills}, Total kills: {total_kills}")
                hit_zombie = True
                hit_zombies.append(zombie)
                print(f"Adding dead body at: {zombie[0]}, {zombie[1]}, {zombie[2]}")
                break
        if not hit_zombie:
            new_bullets.append(bullet)
    bullets = new_bullets

    new_zombies = []
    for zombie in zombies:
        if zombie not in hit_zombies:
            new_zombies.append(zombie)
        else:
            dead_bodies.append([zombie[0], zombie[1], GROUND_HEIGHT, random.uniform(0, 360)])
    zombies = new_zombies

    if consecutive_kills >= CONSECUTIVE_KILLS_FOR_CHEAT:
        multi_shot_available = True
        print(f"Multi-shot mode available! Press 'M' to fire 10 bullets at once.")

    if consecutive_kills >= CONSECUTIVE_KILLS_FOR_CHEAT and not cheat_mode_activated_once:
        cheat_mode_activated_once = True
        print(f"Cheat mode unlock requirement met! Press 'C' to toggle cheat mode.")

    if boss_active and boss_zombie:
        boss_size = ZOMBIE_BODY_WIDTH * BOSS_SIZE_FACTOR
        if is_colliding(player_collision_pos, PLAYER_COLLISION_SIZE, boss_zombie[:3], boss_size):
            player_health -= COLLISION_DAMAGE_BOSS
            consecutive_kills = 0
            multi_shot_available = False
            print(f"Player hit by BOSS! Health: {player_health}, Consecutive kills reset.")

            dir_x = player_pos[0] - boss_zombie[0]
            dir_y = player_pos[1] - boss_zombie[1]
            dist = math.sqrt(dir_x**2 + dir_y**2)
            if dist > 0:
                knockback = 20
                player_pos[0] += (dir_x / dist) * knockback
                player_pos[1] += (dir_y / dist) * knockback

                player_pos[0] = max(-GROUND_SIZE + HUMAN_BODY_WIDTH/2, min(GROUND_SIZE - HUMAN_BODY_WIDTH/2, player_pos[0]))
                player_pos[1] = max(-GROUND_SIZE + HUMAN_BODY_DEPTH/2, min(GROUND_SIZE - HUMAN_BODY_DEPTH/2, player_pos[1]))

    new_zombies = []
    for zombie in zombies:
        if is_colliding(player_collision_pos, PLAYER_COLLISION_SIZE, zombie[:3], ZOMBIE_BODY_WIDTH):
            player_health -= COLLISION_DAMAGE_ZOMBIE
            consecutive_kills = 0
            multi_shot_available = False
            print(f"Player hit! Health: {player_health}, Consecutive kills reset.")
        else:
            new_zombies.append(zombie)
    zombies = new_zombies

    new_health_packs = []
    for pack in health_packs:
        if is_colliding(player_collision_pos, PLAYER_COLLISION_SIZE, pack, HEALTH_PACK_SIZE):
            player_health += HEALTH_GAIN_PACK
            print(f"Health pack collected! Health: {player_health}")
        else:
            new_health_packs.append(pack)
    health_packs = new_health_packs

    new_bombs = []
    for bomb in bombs:
        if is_colliding(player_collision_pos, PLAYER_COLLISION_SIZE, bomb, BOMB_SIZE):
            player_bombs += 1
            print(f"Bomb collected! Bombs: {player_bombs}")
        else:
            new_bombs.append(bomb)
    bombs = new_bombs

    if player_health <= 0:
        game_over = True
        print("Game Over!")

def get_gun_direction():
    direction = [0, 1, 0]

    rad_y = math.radians(gun_rotation_y)
    temp_x = direction[0] * math.cos(rad_y) - direction[1] * math.sin(rad_y)
    temp_y = direction[0] * math.sin(rad_y) + direction[1] * math.cos(rad_y)
    direction[0] = temp_x
    direction[1] = temp_y

    magnitude = math.sqrt(direction[0]**2 + direction[1]**2 + direction[2]**2)
    if magnitude > 0:
        direction = [d / magnitude for d in direction]

    return direction

def fire_bullet():
    if game_over:
        return

    direction = get_gun_direction()

    gun_tip_offset_local = [0, HUMAN_BODY_DEPTH * 0.8 + HUMAN_BODY_DEPTH * 0.4, HUMAN_BODY_HEIGHT * 0.1]

    rad_y = math.radians(gun_rotation_y)
    rotated_offset_x = gun_tip_offset_local[0] * math.cos(rad_y) - gun_tip_offset_local[1] * math.sin(rad_y)
    rotated_offset_y = gun_tip_offset_local[0] * math.sin(rad_y) + gun_tip_offset_local[1] * math.cos(rad_y)
    rotated_offset_z = gun_tip_offset_local[2]

    start_pos = [
        player_pos[0] + rotated_offset_x,
        player_pos[1] + rotated_offset_y,
        player_pos[2] + rotated_offset_z
    ]

    bullets.append(start_pos + direction)
    print("Fired bullet")

def fire_multi_shot():
    if game_over:
        return

    base_direction = get_gun_direction()

    gun_tip_offset_local = [0, HUMAN_BODY_DEPTH * 0.8 + HUMAN_BODY_DEPTH * 0.4, HUMAN_BODY_HEIGHT * 0.1]

    rad_y = math.radians(gun_rotation_y)
    rotated_offset_x = gun_tip_offset_local[0] * math.cos(rad_y) - gun_tip_offset_local[1] * math.sin(rad_y)
    rotated_offset_y = gun_tip_offset_local[0] * math.sin(rad_y) + gun_tip_offset_local[1] * math.cos(rad_y)
    rotated_offset_z = gun_tip_offset_local[2]

    start_pos = [
        player_pos[0] + rotated_offset_x,
        player_pos[1] + rotated_offset_y,
        player_pos[2] + rotated_offset_z
    ]

    for i in range(MULTI_SHOT_COUNT):
        spread_angle = -MULTI_SHOT_SPREAD/2 + (MULTI_SHOT_SPREAD * i / (MULTI_SHOT_COUNT - 1))

        spread_rad = math.radians(spread_angle)
        spread_dir_x = base_direction[0] * math.cos(spread_rad) - base_direction[1] * math.sin(spread_rad)
        spread_dir_y = base_direction[0] * math.sin(spread_rad) + base_direction[1] * math.cos(spread_rad)
        spread_dir_z = base_direction[2]

        magnitude = math.sqrt(spread_dir_x**2 + spread_dir_y**2 + spread_dir_z**2)
        if magnitude > 0:
            spread_dir_x /= magnitude
            spread_dir_y /= magnitude
            spread_dir_z /= magnitude

        bullets.append(start_pos + [spread_dir_x, spread_dir_y, spread_dir_z])

    print(f"Fired multi-shot: {MULTI_SHOT_COUNT} bullets!")

def check_line_of_sight(start_pos, direction, target_pos, target_size):
    to_target = [target_pos[i] - start_pos[i] for i in range(3)]

    dot_product = sum(to_target[i] * direction[i] for i in range(3))
    magnitude_direction_sq = sum(d**2 for d in direction)
    if magnitude_direction_sq == 0:
        return False

    proj_length_sq = dot_product**2 / magnitude_direction_sq

    dist_to_line_sq = sum(to_target[i]**2 for i in range(3)) - proj_length_sq

    return dist_to_line_sq < (target_size / 2)**2 and dot_product > 0


def activate_cheat_mode():
    global cheat_mode_active, gun_rotation_y

    if not cheat_mode_active or game_over:
        return

    gun_rotation_y += 5
    if gun_rotation_y >= 360:
        gun_rotation_y -= 360

    gun_tip_offset_local = [0, HUMAN_BODY_DEPTH * 0.8 + HUMAN_BODY_DEPTH * 0.4, HUMAN_BODY_HEIGHT * 0.1]

    rad_y = math.radians(gun_rotation_y)
    rotated_offset_x = gun_tip_offset_local[0] * math.cos(rad_y) - gun_tip_offset_local[1] * math.sin(rad_y)
    rotated_offset_y = gun_tip_offset_local[0] * math.sin(rad_y) + gun_tip_offset_local[1] * math.cos(rad_y)
    rotated_offset_z = gun_tip_offset_local[2]

    gun_tip_pos = [
        player_pos[0] + rotated_offset_x,
        player_pos[1] + rotated_offset_y,
        player_pos[2] + rotated_offset_z
    ]

    gun_direction = get_gun_direction()

    if boss_active and boss_zombie:
        if check_line_of_sight(gun_tip_pos, gun_direction, boss_zombie[:3], ZOMBIE_BODY_WIDTH * BOSS_SIZE_FACTOR):
            fire_bullet()
            return

    for zombie in zombies:
        if check_line_of_sight(gun_tip_pos, gun_direction, zombie[:3], ZOMBIE_BODY_WIDTH):
            fire_bullet()
            break

def keyboardListener(key, x, y):
    global cheat_mode_active, player_pos, gun_rotation_y, gun_rotation_x, cheat_mode_activated_once, multi_shot_available

    if game_over:
        if key == b'r':
            reset_game()
            print("Attempting to restart game...")
        glutPostRedisplay()
        return

    move_speed = 5
    rotate_speed = 5

    new_player_pos = list(player_pos)

    angle_rad = math.radians(gun_rotation_y)

    if key == b's':
        new_player_pos[0] -= move_speed * math.sin(-angle_rad)
        new_player_pos[1] -= move_speed * math.cos(angle_rad)
    elif key == b'w':
        new_player_pos[0] += move_speed * math.sin(-angle_rad)
        new_player_pos[1] += move_speed * math.cos(angle_rad)

    new_player_pos[0] = max(-GROUND_SIZE + HUMAN_BODY_WIDTH/2, min(GROUND_SIZE - HUMAN_BODY_WIDTH/2, new_player_pos[0]))
    new_player_pos[1] = max(-GROUND_SIZE + HUMAN_BODY_DEPTH/2, min(GROUND_SIZE - HUMAN_BODY_DEPTH/2, new_player_pos[1]))

    colliding_with_tree = False
    for tree in trees:
        if math.dist(new_player_pos, tree) < PLAYER_COLLISION_SIZE / 2 + TREE_COLLISION_SIZE / 2:
            colliding_with_tree = True
            break

    colliding_with_dead_body = False
    for body in dead_bodies:
         if math.dist(new_player_pos[:2], body[:2]) < PLAYER_COLLISION_SIZE / 2 + DEAD_BODY_COLLISION_SIZE / 2:
             colliding_with_dead_body = True
             break

    if not colliding_with_tree and not colliding_with_dead_body:
        player_pos = new_player_pos

    if key == b'a':
        gun_rotation_y = (gun_rotation_y + rotate_speed) % 360
    elif key == b'd':
        gun_rotation_y = (gun_rotation_y - rotate_speed) % 360

    elif key == b'm':
        if multi_shot_available:
            fire_multi_shot()
            multi_shot_available = False
            print("Multi-shot activated! Need 5 consecutive kills to recharge.")
        else:
            print("Multi-shot not available. Need 5 consecutive kills to activate.")

    elif key == b'2':
        if player_bombs > 0:
            detonate_bomb()
        else:
            print("No bombs available! Find and collect bombs to use them.")

    elif key == b'c':
        print(f"C key pressed. Consecutive kills: {consecutive_kills}")
        if consecutive_kills >= CONSECUTIVE_KILLS_FOR_CHEAT:
             if cheat_mode_activated_once:
                cheat_mode_active = not cheat_mode_active

                if cheat_mode_active:
                     print("Cheat mode toggled ON - Auto-rotating and firing at enemies")
                else:
                     print("Cheat mode toggled OFF")
             else:
                 cheat_mode_activated_once = True
                 cheat_mode_active = True
                 print(f"Cheat mode unlocked and toggled ON due to {CONSECUTIVE_KILLS_FOR_CHEAT} consecutive kills!")
        else:
            print(f"Need {CONSECUTIVE_KILLS_FOR_CHEAT} consecutive kills to unlock cheat mode.")

    elif key == b'r':
        reset_game()
        print("Attempting to restart game...")

    glutPostRedisplay()

def specialKeyListener(key, x, y):
    global third_person_camera_pos, camera_height_offset, camera_angle_offset

    move_speed = 10
    rotate_speed = 2

    MAX_CAMERA_HEIGHT = 300
    MIN_CAMERA_HEIGHT = -100

    if key == GLUT_KEY_UP:
        camera_height_offset += move_speed
        if camera_height_offset > MAX_CAMERA_HEIGHT:
            camera_height_offset = MAX_CAMERA_HEIGHT
    elif key == GLUT_KEY_DOWN:
        camera_height_offset -= move_speed
        if camera_height_offset < MIN_CAMERA_HEIGHT:
            camera_height_offset = MIN_CAMERA_HEIGHT

    elif key == GLUT_KEY_LEFT:
        camera_angle_offset -= rotate_speed
    elif key == GLUT_KEY_RIGHT:
        camera_angle_offset += rotate_speed

    glutPostRedisplay()

def mouseListener(button, state, x, y):
    if game_over:
        return

    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        fire_bullet()

    glutPostRedisplay()

def setupCamera():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60, 1.25, 0.1, 1500)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    cam_dist = math.dist(third_person_camera_pos, [0, 0, 0])
    cam_x = cam_dist * math.cos(math.radians(camera_angle_offset))
    cam_y = cam_dist * math.sin(math.radians(camera_angle_offset))
    cam_z = third_person_camera_pos[2] + camera_height_offset

    gluLookAt(cam_x, cam_y, cam_z,
              player_pos[0], player_pos[1], player_pos[2] + HUMAN_BODY_HEIGHT * 0.5,
              0, 0, 1)

def idle():
    if not game_over:
        update_objects()
        check_collisions()
        if cheat_mode_active:
            activate_cheat_mode()

    glutPostRedisplay()

def showScreen():
    glClearColor(sky_color[0], sky_color[1], sky_color[2], 1.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glViewport(0, 0, 1000, 800)

    setupCamera()

    draw_ground()

    draw_human_player(player_pos[0], player_pos[1], player_pos[2])

    draw_game_objects()

    draw_text(10, 770, f"Health: {player_health}", color=(0, 1, 0) if player_health > 2 else (1, 0, 0))
    draw_text(10, 740, f"Score: {player_score}")
    draw_text(10, 710, f"Total Kills: {total_kills}")
    draw_text(10, 680, f"Consecutive Kills: {consecutive_kills}")
    draw_text(10, 650, f"Bombs: {player_bombs}", color=(1.0, 0.6, 0.0))

    time_of_day = "NIGHT" if is_night else "DAY"
    time_color = (0.5, 0.5, 1.0) if is_night else (1.0, 1.0, 0.5)
    draw_text(800, 770, f"Time: {time_of_day}", color=time_color)

    if boss_active and boss_zombie:
        draw_text(700, 740, f"BOSS HP: {boss_health}/25", color=(1.0, 0.0, 0.0))

    if is_night:
        draw_text(600, 710, "WARNING: MORE ZOMBIES AT NIGHT!", color=(1.0, 0.5, 0.5))
        if total_kills >= KILLS_FOR_BOSS and not boss_active:
            draw_text(550, 680, "BOSS ZOMBIE WILL APPEAR SOON!", color=(1.0, 0.0, 0.0))

    y_pos = 620
    if multi_shot_available:
        draw_text(10, y_pos, "MULTI-SHOT READY! Press 'M'", color=(1, 1, 0))
        y_pos -= 30
    if cheat_mode_active:
        draw_text(10, y_pos, "CHEAT MODE ACTIVE!", color=(0, 1, 1))
        y_pos -= 30

    if game_over:
        draw_text(400, 400, "GAME OVER!", font=GLUT_BITMAP_TIMES_ROMAN_24, color=(1, 0, 0))
        draw_text(350, 370, "Press 'R' to Restart", font=GLUT_BITMAP_HELVETICA_18, color=(1, 1, 1))

    glutSwapBuffers()

def spawn_boss_zombie():
    global boss_active, boss_zombie, boss_health

    boss_margin = ZOMBIE_BODY_WIDTH * BOSS_SIZE_FACTOR * 2.0
    x = random.uniform(-GROUND_SIZE + boss_margin, GROUND_SIZE - boss_margin)
    y = random.uniform(-GROUND_SIZE + boss_margin, GROUND_SIZE - boss_margin)
    z = GROUND_HEIGHT

    while math.dist([x, y, z], player_pos) < 300:
        x = random.uniform(-GROUND_SIZE + boss_margin, GROUND_SIZE - boss_margin)
        y = random.uniform(-GROUND_SIZE + boss_margin, GROUND_SIZE - boss_margin)

    hand_asymmetry_factor = random.uniform(0.8, 1.2)
    scale_factor = ZOMBIE_SCALE_MAX
    scale_direction = -1

    boss_zombie = [x, y, z, hand_asymmetry_factor, scale_factor, scale_direction]
    boss_active = True
    boss_health = 25

    print(f"Boss zombie spawned at position: {x}, {y}, {z}")

def reset_game():
    global player_health, player_score, bullets_missed, consecutive_kills, total_kills
    global cheat_mode_active, game_over, cheat_mode_activated_once, multi_shot_available
    global zombies, bullets, health_packs, dead_bodies, trees, player_pos, gun_rotation_y, gun_rotation_x
    global camera_height_offset, camera_angle_offset, sky_color, sky_to_dark
    global is_night, boss_active, boss_zombie, boss_health, NUM_ZOMBIES, player_bombs, bombs, explosions

    player_health = 10
    player_score = 0
    bullets_missed = 0
    consecutive_kills = 0
    total_kills = 0
    cheat_mode_active = False
    cheat_mode_activated_once = False
    multi_shot_available = False
    game_over = False
    is_night = False
    player_bombs = 0

    boss_active = False
    boss_zombie = None
    boss_health = 25

    NUM_ZOMBIES = NUM_ZOMBIES_DAY

    zombies.clear()
    bullets.clear()
    health_packs.clear()
    dead_bodies.clear()
    trees.clear()
    bombs.clear()
    explosions.clear()

    player_pos = [0, 0, 0]
    gun_rotation_y = 0
    gun_rotation_x = 0
    camera_height_offset = 0
    camera_angle_offset = 0

    sky_color = [0.1, 0.1, 0.3]
    sky_to_dark = False

    generate_zombies()
    generate_health_packs()
    generate_trees()
    generate_bombs()

    print("Game reset.")

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(1000, 800)
    glutInitWindowPosition(0, 0)
    wind = glutCreateWindow(b"Human vs Zombies")

    glEnable(GL_DEPTH_TEST)

    generate_zombies()
    generate_health_packs()
    generate_trees()
    generate_bombs()

    glutDisplayFunc(showScreen)
    glutKeyboardFunc(keyboardListener)
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle)

    reset_game()

    glutMainLoop()

if __name__ == "__main__":
    main()