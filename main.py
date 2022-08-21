import pygame
import os
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("First Game!")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

BORDER_WIDTH = 10
BORDER = pygame.Rect(WIDTH//2-BORDER_WIDTH//2, 0, BORDER_WIDTH, HEIGHT)

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Grenade+1.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(
    os.path.join('Assets', 'Gun+Silencer.mp3'))

HEALTH_FONT = pygame.font.SysFont('impact', 40)
WINNER_FONT = pygame.font.SysFont('impact', 100)

FPS = 60
VEL = 5
BULLET_VEL = 10
MAX_BULLETS = 7
MAX_HEALTH = 3


SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 40, 55

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

YELLOW_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.scale(
    YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))

RED_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 180)

SPACE = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))

SHIELD_WIDTH, SHIELD_HEIGHT = 10, 10

YELLOW_SHIELD = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'shield_yellow.png')), (SHIELD_WIDTH, SHIELD_HEIGHT))
RED_SHIELD = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'shield_red.png')), (SHIELD_WIDTH, SHIELD_HEIGHT))

EXPLOSION_WIDTH, EXPLOSION_HEIGHT = 70, 70
EXPLOSION = pygame.transform.scale(pygame.image.load(os.path.join(
    'Assets', 'explosion.png')), (EXPLOSION_WIDTH, EXPLOSION_HEIGHT))

EXPLOSION_TIMEOUT = 5


def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health, red_explosion, yellow_explosion):
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)

    red_health_text = HEALTH_FONT.render(
        "Health: " + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render(
        "Health: " + str(yellow_health), 1, WHITE)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))

    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    # Render flying bullets
    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    # Render available bullets
    for pos, slot in enumerate(range(MAX_BULLETS - len(red_bullets))):
        slot_width = red.width//MAX_BULLETS-2
        slot_height = 10
        pygame.draw.rect(WIN, RED, pygame.Rect(
            red.x + (slot_width + 2)*pos, red.y-slot_height, slot_width, slot_height))

    for pos, slot in enumerate(range(MAX_BULLETS - len(yellow_bullets))):
        slot_width = yellow.width//MAX_BULLETS-2
        slot_height = 10
        pygame.draw.rect(WIN, YELLOW, pygame.Rect(
            yellow.x + (slot_width + 2)*pos, yellow.y-slot_height, slot_width, slot_height))

    # Render shields
    for pos, slot in enumerate(range(red_health)):
        WIN.blit(RED_SHIELD, (red.x + 10*pos, red.y + red.height))

    for pos, slot in enumerate(range(yellow_health)):
        WIN.blit(YELLOW_SHIELD, (yellow.x + 10*pos, yellow.y + yellow.height))

    # Render explosion
    if red_explosion:
        WIN.blit(EXPLOSION, (red.x + red.width//2 - EXPLOSION_WIDTH //
                 2, red.y + red.height//2 - EXPLOSION_HEIGHT//2))

    if yellow_explosion:
        WIN.blit(EXPLOSION, (yellow.x + yellow.width//2 - EXPLOSION_WIDTH //
                 2, yellow.y + yellow.height//2 - EXPLOSION_HEIGHT//2))

    pygame.display.update()


def handle_yellow_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0:  # LEFT
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + yellow.width + VEL < BORDER.x:  # RIGHT
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0:  # UP
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + yellow.height + VEL < HEIGHT:  # DOWN
        yellow.y += VEL


def handle_red_movement(keys_pressed, red):
    # LEFT
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > (BORDER.x + BORDER_WIDTH):
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + red.width + VEL < WIDTH:  # RIGHT
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0:  # UP
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT:  # DOWN
        red.y += VEL


def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            yellow_bullets.remove(bullet)
            pygame.event.post(pygame.event.Event(RED_HIT))
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            red_bullets.remove(bullet)
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
        elif bullet.x < 0:
            red_bullets.remove(bullet)


def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH//2 - draw_text.get_width() //
             2, HEIGHT//2 - draw_text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(5000)


def main():
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH,
                      SPACESHIP_HEIGHT)  # x, y, width, height
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH,
                         SPACESHIP_HEIGHT)  # x, y, width, height

    red_bullets = []
    yellow_bullets = []

    red_health = MAX_HEALTH
    yellow_health = MAX_HEALTH

    red_explosion = 0
    yellow_explosion = 0

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)

        red_explosion = red_explosion - 1 if red_explosion > 0 else 0
        yellow_explosion = yellow_explosion - 1 if yellow_explosion > 0 else 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        yellow.x+yellow.width, yellow.y+yellow.height//2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y+red.height//2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == RED_HIT:
                red_health -= 1
                red_explosion = EXPLOSION_TIMEOUT
                BULLET_HIT_SOUND.play()

            if event.type == YELLOW_HIT:
                yellow_health -= 1
                yellow_explosion = EXPLOSION_TIMEOUT
                BULLET_HIT_SOUND.play()

        winner_text = ""
        if red_health <= 0:
            winner_text = "Yellow wins!"
        if yellow_health <= 0:
            winner_text = "Red wins!"

        if winner_text != "":
            draw_window(red, yellow, red_bullets, yellow_bullets,
                        red_health, yellow_health, red_explosion, yellow_explosion)
            draw_winner(winner_text)
            break

        keys_pressed = pygame.key.get_pressed()
        handle_yellow_movement(keys_pressed, yellow)
        handle_red_movement(keys_pressed, red)

        handle_bullets(yellow_bullets, red_bullets, yellow,
                       red)

        draw_window(red, yellow, red_bullets, yellow_bullets,
                    red_health, yellow_health, red_explosion > 0, yellow_explosion > 0)

    main()


if __name__ == "__main__":
    main()
