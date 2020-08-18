import pygame
import random
import math
from PIL import Image

# Initialize the pygame
pygame.init()
# creating screen
screen = pygame.display.set_mode((800, 600))
# title and icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

background = pygame.image.load('background.png')
# player
playerimg = pygame.image.load('spaceship.png')
playerimg = pygame.transform.scale(playerimg, (50, 50))
playerx = 400
playery = 530
player_x_vel = 0
# Enemy
enemyimg = []
enemyx = []
enemyy = []
enemy_x_vel = []
enemy_y_vel = []
num_of_enemies = 5
for i in range(num_of_enemies):
    x = pygame.image.load('enemy.png')
    x = pygame.transform.scale(x, (45, 45))
    enemyimg.append(x)
    enemyx.append(random.randint(0, 800))
    enemyy.append(random.randint(50, 200))
    enemy_x_vel.append(1)
    enemy_y_vel.append(40)

# bullet
bulletimg = pygame.image.load('bullet.png')
bulletimg = pygame.transform.scale(bulletimg, (40, 40))
bulletx = 0
bullety = 530
bullet_y_vel = 5
bullet_state = "ready"

score = 0
font = pygame.font.Font("C:\Windows\Fonts\segoepr.ttf",32)
x_cord = 10
y_cord = 10
def show_score(x, y):
    scr = font.render("Score: "+str(score),True,(255,255,255))
    screen.blit(scr,(x, y))

def player(x, y):
    screen.blit(playerimg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyimg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletimg, (x + 16, y + 10))


def iscollision(enemyx, enemyy, bulletx, bullety):
    distance = math.sqrt((math.pow(enemyx-bulletx, 2)) + (math.pow(enemyy-bullety, 2)))
    if distance < 25:
        return True
    else:
        return False


# game loop
running = True
while running:
    screen.fill((0, 0, 0))                  #fill the screen with some color using(R,G,B)
    screen.blit(background, (0, 0))         #no need of the above line if we use this
    for event in pygame.event.get():
        if event.type == pygame.QUIT:       #exit when clicked on close
            running = False
        # if keystroke is pressed, check whether right arrow or left arrow or spacebar
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_vel = -3
            if event.key == pygame.K_RIGHT:
                player_x_vel = 3
            if event.key == pygame.K_SPACE and bullet_state == "ready":
                bullet_x_vel = playerx
                fire_bullet(bullet_x_vel, bullety)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player_x_vel = 0
            if event.key == pygame.K_RIGHT:
                player_x_vel = 0

    playerx += player_x_vel
    if playerx <= 0:
        playerx = 0
    elif playerx >= 740:
        playerx = 740
    for i in range(num_of_enemies):
        enemyx[i] += enemy_x_vel[i]
        if enemyx[i] <= 0:                                      #change direction when boundaries are hit
            enemy_x_vel[i] = 1
            enemyy[i] += enemy_y_vel[i]
        elif enemyx[i] >= 740:
            enemy_x_vel[i] = -1
            enemyy[i] += enemy_y_vel[i]
        collision = iscollision(enemyx[i], enemyy[i], bulletx, bullety)
        if bullet_state == "fire" and collision:
            bullety = 530
            bullet_state = "ready"
            score += 1
            enemyx[i] = random.randint(0, 740)                      #respawn
            enemyy[i] = random.randint(50, 150)
            print(score)
        enemy(enemyx[i], enemyy[i], i)
    if bullet_state == "fire":
        fire_bullet(bullet_x_vel, bullety)
        bullety -= bullet_y_vel
    if bullety <= 0:
        bullety = 530
        bullet_state = "ready"
    player(playerx, playery)            #makes the player surface to persist on the screen continously
    show_score(x_cord,y_cord)
    pygame.display.update()             #effects frame rate, better to specify with specific rects to update as parameters
