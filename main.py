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
# ACC = 2  # px/frame^2
# MAX_VEL = 10  # px/frame
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


class Bullet(pygame.Rect):
    def __init__(self, x, y, width, height, color, owner):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.owner = owner  # owner is immune to damage from this Bullet

    def handle_movement(self, spaceships):
        if self.color == YELLOW:
            self.x += BULLET_VEL
        elif self.color == RED:
            self.x -= BULLET_VEL
        else:
            raise ValueError

        for collision in self.collidelistall(spaceships):
            print(id(self.owner))
            print(collision, id(spaceships[collision]))
            if spaceships[collision] != self.owner:
                self.owner.bullets.remove(self)
                pygame.event.post(pygame.event.Event(
                    spaceships[collision].hit_event))

        if self.x > WIDTH:
            self.owner.bullets.remove(self)
            # TODO: destruct Bullet

    def draw(self, win):
        pass


class Spaceship(pygame.Rect):
    def __init__(self, x, y, width, height, color, key_up, key_down, key_left, key_right, key_shoot, hit_event):
        # self.rect = pygame.Rect(x, y, width, height)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.vel = 5  # (0,0)
        self.max_health = 5
        self.health = self.max_health
        self.max_bullets = 3
        self.bullets = []
        self.bullet_vel = 10
        self.key_up = key_up
        self.key_down = key_down
        self.key_right = key_right
        self.key_left = key_left
        self.key_shoot = key_shoot
        self.hit_event = hit_event

    def handle_movement(self, keys_pressed):
        if keys_pressed[self.key_left] and self.x - self.vel > 0:  # LEFT
            self.x -= self.vel
        if keys_pressed[self.key_right] and self.x + self.width + self.vel < BORDER.x:  # RIGHT
            self.x += self.vel
        if keys_pressed[self.key_up] and self.y - self.vel > 0:  # UP
            self.y -= self.vel
        if keys_pressed[self.key_down] and self.y + self.height + self.vel < HEIGHT:  # DOWN
            self.y += self.vel

    def draw(self, win):
        # Render spaceship
        if self.color == YELLOW:
            win.blit(YELLOW_SPACESHIP, (self.x, self.y))
        elif self.color == RED:
            win.blit(RED_SPACESHIP, (self.x, self.y))
        else:
            raise ValueError

        # Render flying bullets
        for bullet in self.bullets:
            pygame.draw.rect(win, self.color, bullet)

        # Render available bullets
        for pos, slot in enumerate(range(self.max_bullets - len(self.bullets))):
            slot_width = self.width//self.max_bullets-2
            slot_height = 10
            pygame.draw.rect(WIN, self.color, pygame.Rect(
                self.x + (slot_width + 2)*pos, self.y-slot_height, slot_width, slot_height))

        # Render shields
        for pos, slot in enumerate(range(self.health)):
            if self.color == YELLOW:
                win.blit(YELLOW_SHIELD, (self.x + 10*pos,
                                         self.y + self.height))
            elif self.color == RED:
                win.blit(RED_SHIELD, (self.x + 10*pos,
                                      self.y + self.height))


def draw_window(red, yellow,  red_explosion, yellow_explosion):
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)

    red_health_text = HEALTH_FONT.render(
        "Health: " + str(red.health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render(
        "Health: " + str(yellow.health), 1, WHITE)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))

    # WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    yellow.draw(WIN)
    red.draw(WIN)

    # Render explosion
    if red_explosion:
        WIN.blit(EXPLOSION, (red.x + red.width//2 - EXPLOSION_WIDTH //
                 2, red.y + red.height//2 - EXPLOSION_HEIGHT//2))

    if yellow_explosion:
        WIN.blit(EXPLOSION, (yellow.x + yellow.width//2 - EXPLOSION_WIDTH //
                 2, yellow.y + yellow.height//2 - EXPLOSION_HEIGHT//2))

    pygame.display.update()


# def handle_yellow_acceleration(keys_pressed, yellow):
#     # TODO: To keep track of acceleration, make spaceships to objects
#     # Velocity as 2D vector
#     # key press accelerates spaceship into some direction
#     # Add some attenuation so the ships come to a stand still again
#     pass


def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH//2 - draw_text.get_width() //
             2, HEIGHT//2 - draw_text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(5000)


def main():
    red = Spaceship(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT, RED,
                    pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_RCTRL, RED_HIT)
    yellow = Spaceship(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT, YELLOW,
                       pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d, pygame.K_LCTRL, YELLOW_HIT)

    spaceships = [yellow, red]

    bullets = []

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
                for spaceship in spaceships:
                    if event.key == spaceship.key_shoot and len(spaceship.bullets) < spaceship.max_bullets:
                        bullet = Bullet(spaceship.x+spaceship.width, spaceship.y +
                                        spaceship.height//2 - 2, 10, 5, spaceship.color, spaceship)
                        spaceship.bullets.append(bullet)
                        BULLET_FIRE_SOUND.play()

            if event.type == RED_HIT:
                red.health -= 1
                red_explosion = EXPLOSION_TIMEOUT
                BULLET_HIT_SOUND.play()

            if event.type == YELLOW_HIT:
                yellow.health -= 1
                yellow_explosion = EXPLOSION_TIMEOUT
                BULLET_HIT_SOUND.play()

        winner_text = ""
        if red.health <= 0:
            winner_text = "Yellow wins!"
        if yellow.health <= 0:
            winner_text = "Red wins!"

        if winner_text != "":
            draw_window(red, yellow, red_explosion, yellow_explosion)
            draw_winner(winner_text)
            break

        keys_pressed = pygame.key.get_pressed()
        yellow.handle_movement(keys_pressed)
        red.handle_movement(keys_pressed)

        for bullet in yellow.bullets:
            bullet.handle_movement(spaceships)
        for bullet in red.bullets:
            bullet.handle_movement(spaceships)

        # handle_bullets(yellow_bullets, red_bullets, yellow,
        #                red)

        draw_window(red, yellow, red_explosion > 0, yellow_explosion > 0)

    main()


if __name__ == "__main__":
    main()
