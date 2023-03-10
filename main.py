import pygame
import os
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))      #resolução do pygame
pygame.display.set_caption("First Game!")

BLACK = (0, 0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

BORDER = pygame.Rect(WIDTH//2-5, 0, 10, HEIGHT)



BULLET_HIT_SOUND = pygame.mixer.Sound('spaceship_game/Assets/spaceship_broken.wav')
BULLET_FIRE_SOUND = pygame.mixer.Sound('spaceship_game/Assets/spaceship_shot.wav')


HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

FPS = 144
VEL = 3
BULLET_VEL = 7
MAX_BULLETS = 3
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 48

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2


YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('spaceship_game/Assets', 'spaceship_yellow.png'))  #os,.path.join serve para que o caminho da png seja reconhecido por todos os sitemas operacionais.

YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)           #ROTACIONANDO E REDIMENSIONANDO IMAGEM

RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('spaceship_game/Assets', 'spaceship_red.png'))

RED_SPACESHIP =  pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE,(SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)                 #REDIMENSIONANDO IMAGEM

SPACE = pygame.transform.scale(pygame.image.load(os.path.join('spaceship_game/Assets', 'space.png')), (WIDTH, HEIGHT))

def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    WIN.blit(SPACE, (0,0))
    pygame.draw.rect(WIN, BLACK, BORDER)

    red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), 1, WHITE)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() -10, 10))
    WIN.blit(yellow_health_text, (10,10))

    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))       #blitz para renderizar img na tela, parametro imagem e xy
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)
    
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    pygame.display.update()               #atualizar a tela para as coisas aparecerem



def yellow_handle_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0: #LEFT
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width - 15< BORDER.x: #RIGHT
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y > 0: #UP
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + yellow.height + VEL < HEIGHT -10: #DOWN
        yellow.y += VEL

def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL - BORDER.x - 10 > 0: #LEFT
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + red.width - 15 < WIDTH: #RIGHT
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y > 0: #UP
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + red.height + VEL < HEIGHT -10: #DOWN
        red.y += VEL

def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)



def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text,(WIDTH//2 - draw_text.get_width()//2, HEIGHT//2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(3500)


def main():
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    red_bullets = []
    yellow_bullets = []

    red_health = 10
    yellow_health = 10
    
    clock = pygame.time.Clock()
    run = True
    while run:                   #while para poder verificar quando clicar no X e fechar o jogo
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + yellow.width - 35, yellow.y + yellow.height//2 + 5, 10,5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x + red.width -35, red.y + red.height//2 + 5, 10,5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()

            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()

        winner_text = ""
        if red_health <= 0:
            winner_text = "Yellow Wins!"
        

        if yellow_health <= 0:
            winner_text = "Red Wins!"
        
        if winner_text != "":
            draw_winner(winner_text)
            break



        print(f"red_bullet: {red_bullets} yellow bullets: {yellow_bullets}")
        keys_pressed = pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)
        handle_bullets(yellow_bullets, red_bullets, yellow, red)
        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)
    
    main()

if __name__ == "__main__":     #essa linha serve para que esse arquivo não seja executado diretamente quando importado.
    main()