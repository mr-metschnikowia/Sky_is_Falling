import pygame
import sys
import random

pygame.init()

WIDTH = 800
HEIGHT = 600
python_green = (121,230,144)
BLACK = (0,0,0)
PINK = (245,184,255)
RED = (255,0,0)
BLUE = (66,135,158)
enemy_list = []
player_size = 50
player_location = [400-player_size/2, 550]
score = 0

myFont = pygame.font.SysFont('monospace', 20)

screen = pygame.display.set_mode((WIDTH, HEIGHT))

game_over = False

def generate_enemy_list(enemy_list):
    delay = random.random()
    if len(enemy_list) < 10 and delay < 0.01:
        new_enemy_location = [random.randrange(70, WIDTH - 70), 0]
        enemy_list.append(new_enemy_location)

def generate_enemies(enemy_list):
    for enemy_location in enemy_list:
        pygame.draw.rect(screen, RED, (enemy_location[0], enemy_location[1], player_size, player_size))

def update_enemy_position(enemy_list, score):
    for index, enemy_location in enumerate(enemy_list):
        if enemy_location[1] < HEIGHT:
            enemy_location[1] += SPEED
        else:
            enemy_list.pop(index)
            score += 1
    return score

def detect_collision_new(enemy_list, player_location):
    for enemy_location in enemy_list:
        p_x = player_location[0]
        p_y = player_location[1]
        e_x = enemy_location[0]
        e_y = enemy_location[1]
        if ((e_x >= p_x) and (e_x <= p_x + player_size)) or ((p_x > e_x) and (p_x <= e_x + player_size)):
            if ((e_y <= p_y) and (p_y <= e_y + player_size)) or ((e_y >= p_y) and (e_y <= p_y + player_size)):
                return True
            break
    return False

def set_level(score):
    if score == 0:
        SPEED = 0.25
    else:
        SPEED = score/200 + 0.25
    return SPEED

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            x = player_location[0]
            y = player_location[1]
            if event.key == pygame.K_RIGHT:
                x += 50
            elif event.key == pygame.K_LEFT:
                x -= 50
            player_location = [x,y]
    if score >= 50:
        screen.fill(BLUE)
    else:
        screen.fill(BLACK)
    random_number = random.random()
    generate_enemy_list(enemy_list)
    generate_enemies(enemy_list)
    score = update_enemy_position(enemy_list, score)
    SPEED = set_level(score)
    text = 'Score:' + str(score)
    label = myFont.render(text, 1, PINK)
    screen.blit(label, (10, 10))
    if detect_collision_new(enemy_list,player_location):
        game_over = True
    pygame.draw.rect(screen, python_green, (player_location[0],player_location[1],player_size,player_size))
    pygame.display.update()
