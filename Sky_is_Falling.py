import pygame
import sys
import random
import time
# importing prerequisites


pygame.init()
# initialising game

WIDTH = 800
HEIGHT = 600
# creating GUI

pygame.mixer.music.load(r'music/unravel.wav')
pygame.mixer.music.play(loops=-1)

python_green = (121,230,144)
PURPLE = (0,0,102)
BLACK = (0,0,0)
PINK = (245,184,255)
RED = (255,0,0)
LIGHT_BLUE = (66,135,158)
DARK_BLUE = (0,0,255)
YELLOW = (255,255,0)
# defining colours

player_speed = 50
enemy_list = []
brick_colours = []
player_size = 50
enemy_size = 50
player_location = [400-player_size/2, 550]
score = 0
start = 0
# defining key variables

with open(r'high_score\stats.txt','r') as f:
    high_score = int(f.read())
myFont = pygame.font.SysFont('monospace', 20)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
game_over = False
# grabbing high score

def generate_colour_list(brick_colours):
    colour_roulette = random.random()
    if len(brick_colours) < 10:
        if colour_roulette <= 0.05:
            brick_colour = YELLOW
        elif colour_roulette >= 0.95:
            brick_colour = DARK_BLUE
        else:
            brick_colour = RED
        brick_colours.append(brick_colour)
# generates colours of blocks

def generate_enemy_list(enemy_list):
    delay = random.random()
    if len(enemy_list) < 10 and delay < 0.01:
        new_enemy_location = [random.randrange(0, WIDTH - enemy_size), 0]
        enemy_list.append(new_enemy_location)
# generates coordinates of blocks

def generate_enemies(enemy_list, brick_colours):
    for index,enemy_location in enumerate(enemy_list):
        pygame.draw.rect(screen, brick_colours[index], (enemy_location[0], enemy_location[1], enemy_size, enemy_size))
# creates blocks on canvas

def update_enemy_position(enemy_list, brick_colours, score):
    for index, enemy_location in enumerate(enemy_list):
        if enemy_location[1] < HEIGHT:
            enemy_location[1] += SPEED
        else:
            enemy_list.pop(index)
            brick_colours.pop(index)
            score += 1
    return score
# block movement

def detect_collision(enemy_list, player_location, brick_colours, colour):
    for idx, enemy_location in enumerate(enemy_list):
        p_x = player_location[0]
        p_y = player_location[1]
        e_x = enemy_location[0]
        e_y = enemy_location[1]
        if ((e_x >= p_x) and (e_x <= p_x + player_size)) or ((p_x > e_x) and (p_x <= e_x + enemy_size)):
            if ((e_y <= p_y) and (p_y <= e_y + enemy_size)) or ((e_y >= p_y) and (e_y <= p_y + player_size)):
                if brick_colours[idx] == colour:
                    enemy_list.pop(idx)
                    brick_colours.pop(idx)
                    return True
            break
    return False
# hit box

def set_level(score):
    if score == 0:
        SPEED = 0.25
    else:
        SPEED = score/200 + 0.25
    return SPEED
# sets level difficulty

def border(player_location):
    if player_location[0] < 0:
        player_location[0] = 0
    elif player_location[0] + player_size > 800:
        player_location[0] = 800 - player_size
# defining map borders

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            x = player_location[0]
            y = player_location[1]
            if event.key == pygame.K_RIGHT:
                x += player_speed
            elif event.key == pygame.K_LEFT:
                x -= player_speed
            player_location = [x,y]
            # control
    if score >= 100:
        screen.fill(PURPLE)
    elif score >= 50:
        screen.fill(LIGHT_BLUE)
    else:
        screen.fill(BLACK)
    random_number = random.random()
    generate_colour_list(brick_colours)
    generate_enemy_list(enemy_list)
    generate_enemies(enemy_list, brick_colours)
    score = update_enemy_position(enemy_list, brick_colours, score)
    SPEED = set_level(score)
    text = 'Score:' + str(score)
    high_score_text = 'High Score:' + str(high_score)
    label = myFont.render(text, 1, PINK)
    high_score_label = myFont.render(high_score_text, 1, PINK)
    screen.blit(high_score_label, (10,30))
    screen.blit(label, (10, 10))
    if detect_collision(enemy_list, player_location, brick_colours, RED):
        if score > high_score:
            with open(r'high_score/stats.txt', 'w') as f:
                f.write(str(score))
        game_over = True
    if detect_collision(enemy_list, player_location, brick_colours, YELLOW):
        player_size = 10
        start = time.clock()
    if detect_collision(enemy_list, player_location, brick_colours, DARK_BLUE):
        player_speed = 100
        start = time.clock()
    if time.clock() - start > 5:
        player_size, player_speed = 50, 50
    pygame.draw.rect(screen, python_green, (player_location[0],player_location[1],player_size,player_size))
    border(player_location)
    pygame.display.update()
    # game loop
