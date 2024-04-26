import pygame 
import os
import random
pygame.font.init()

WIDTH = 900
HEIGHT  = 500

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("ReClick")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

FPS = 60
SPACESHIP_WIDTH = 55    # szerokosc
SPACESHIP_HEIGHT = 40   # wysokosc
ENEMY_WIDTH = 30
ENEMY_HEIGHT = 30

YELLOW_HIT = pygame.USEREVENT + 1
POINT = pygame.USEREVENT + 2
SPAWN_ENEMY = pygame.USEREVENT + 3
ENEMY_BLAST = pygame.USEREVENT + 4

#BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

VEL = 5
BULLET_VEL = 7
ENEMY_VEL = 2
MAX_BULLETS = 3

YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)
#RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_red.png'))
#RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))

def draw_window(yellow, yellow_bullets, yellow_health, enemies, score, enemy_bullets):

    WIN.blit(SPACE, (0, 0))
    #pygame.draw.rect(WIN, BLACK, BORDER)

    score_text = HEALTH_FONT.render("SCORE:" + str(score), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render("Health:" + str(yellow_health), 1, WHITE)
    WIN.blit(score_text, (WIDTH - score_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))

    #WIN.blit(RED_SPACESHIP, (red.x, red.y))
    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))

    #for bullet in red_bullets:
        #pygame.draw.rect(WIN, RED, bullet)
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)
    for enemy in enemies:
        pygame.draw.rect(WIN, RED, enemy)
    for bullet in enemy_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    pygame.display.update()

def draw_winner(winner_text):
    draw_text = WINNER_FONT.render(winner_text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)

def yellow_movement(keys_pressed, yellow): # sterowanie yellow
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0:    # LEFT
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL < WIDTH - yellow.width:    # RIGHT
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0:    # UP
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL < HEIGHT - yellow.height - 15:    # DOWN
        yellow.y += VEL

def handle_bullets(yellow_bullets, yellow, enemies, enemy_bullets): # sterowanie pociskami i sprawdzanie kolizji z enemies
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL 
        for enemy in enemies:
            if enemy.colliderect(bullet):
                pygame.event.post(pygame.event.Event(POINT))
                yellow_bullets.remove(bullet)
                enemies.remove(enemy)
                break
        if bullet.x > WIDTH:
            yellow_bullets.remove(bullet)
    for enemy in enemies:
        if yellow.colliderect(enemy):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            enemies.remove(enemy)
    for bullet in enemy_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            enemy_bullets.remove(bullet)
    #for bullet in red_bullets:
    #    bullet.x -= BULLET_VEL 
    #    if yellow.colliderect(bullet):
    #        pygame.event.post(pygame.event.Event(YELLOW_HIT))
    #        red_bullets.remove(bullet)
    #    elif bullet.x < 0:
    #        red_bullets.remove(bullet)

def enemies_movement(enemies): 
    for enemy in enemies:
        opt = random.randint(1, 4)
        if opt == 1 and enemy.y - ENEMY_VEL > 10: # W -> góra
            enemy.y = enemy.y - ENEMY_VEL
        elif opt == 2 and enemy.y + ENEMY_VEL + ENEMY_HEIGHT < HEIGHT - 15: # S -> dół
            enemy.y = enemy.y + ENEMY_VEL
        elif opt == 3 and enemy.x - ENEMY_VEL > 0: # A -> lewo
            enemy.x = enemy.x - ENEMY_VEL
        elif opt == 4 and enemy.x + ENEMY_VEL + ENEMY_WIDTH < HEIGHT: # D => prawo
            enemy.x = enemy.x + ENEMY_VEL

def create_bullets(enemies, enemy_bullets):
    for enemy in enemies:
        bullet = pygame.Rect(enemy.x, enemy.y + enemy.height//2 - 2, 10, 5)
        enemy_bullets.append(bullet)       

def main():

    #red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100,300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    yellow_bullets = []
    enemy_bullets = []
    enemies = []

    spawn = 1 # za ile czasu zrespi się enemy
    blast = 1 # za ile czasi enemies strzela

    #red_bullets = []

    yellow_health = 10
    score = 0
    
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        spawn += 1
        blast += 1
        #print(spawn)
        if spawn == 100:
            pygame.event.post(pygame.event.Event(SPAWN_ENEMY))
            spawn = 1
        if blast == 250:
            pygame.event.post(pygame.event.Event(ENEMY_BLAST))
            blast = 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                #if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                #    bullet = pygame.Rect(red.x, red.y + red.height//2 - 2, 10, 5)
                #    red_bullets.append(bullet)

            #if event.type == RED_HIT:
            #    red_health -= 1
            if event.type == YELLOW_HIT:
                yellow_health -= 1
            
            if event.type == SPAWN_ENEMY:
                x = random.randint(10, 850)
                y = random.randint(60, 450)
                enemy = pygame.Rect(x, y, ENEMY_WIDTH, ENEMY_HEIGHT)
                if yellow.colliderect(enemy):
                    yellow_health += 1
                    #print("HIT")
                enemies.append(enemy)
            if event.type == POINT:
                score = score + 1
            if event.type == ENEMY_BLAST:
                create_bullets(enemies, enemy_bullets)


        winner_text = ""
        #if red_health <= 0:
        #    winner_text = "YELLOW WINS"
        if yellow_health <= 0:
            winner_text = "LOSER"
        if winner_text != "":
            draw_window(yellow, yellow_bullets, yellow_health, enemies, score)
            draw_winner(winner_text, yellow_health)
            break

        keys_pressed = pygame.key.get_pressed()
        yellow_movement(keys_pressed, yellow)
        #red_movement(keys_pressed, red)
          
        handle_bullets(yellow_bullets, yellow, enemies, enemy_bullets)
        enemies_movement(enemies)
        draw_window(yellow, yellow_bullets, yellow_health, enemies, score, enemy_bullets)
    
    main()

if __name__ == "__main__":
    main()